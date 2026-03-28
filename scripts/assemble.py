#!/usr/bin/env python3
"""
AI_SHOW — Video Assembler v3.0
Собирает эпизод: видеоклипы/картинки + mix.mp3 (или отдельные голоса) + SRT → MP4.

v3 vs v2:
- moviepy clip composition вместо покадрового PNG рендера
- SRT burn-in субтитры
- Dissolve (CrossFade) между шотами внутри одного мира
- mix.mp3 как основной аудио-вход (fallback на отдельные файлы)
- Обратная совместимость: без mix.mp3/SRT работает как v2

Использование:
  python3 scripts/assemble.py S01E01 [--srt file.srt] [--transition-duration 0.3] [--dry-run]
"""

import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from config import W, H, FPS, FONT_TITLE, FONT_SUB, FONT_IMPACT, episode_paths, parse_time_range


# ── Fonts ────────────────────────────────────────────────────────

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


# ── SRT Parser ───────────────────────────────────────────────────

def parse_srt(srt_path: str | Path) -> list[dict]:
    """Парсит SRT-файл. Returns list of {start, end, text}."""
    srt_path = Path(srt_path)
    if not srt_path.exists():
        return []

    content = srt_path.read_text(encoding="utf-8")
    entries = []
    blocks = re.split(r'\n\s*\n', content.strip())

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue
        # Line 1: index (skip)
        # Line 2: timestamp
        time_match = re.match(
            r'(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})',
            lines[1]
        )
        if not time_match:
            continue
        g = time_match.groups()
        start = int(g[0]) * 3600 + int(g[1]) * 60 + int(g[2]) + int(g[3]) / 1000
        end = int(g[4]) * 3600 + int(g[5]) * 60 + int(g[6]) + int(g[7]) / 1000
        text = '\n'.join(lines[2:])
        entries.append({"start": start, "end": end, "text": text})

    return entries


# ── Visual Effects ───────────────────────────────────────────────

def ken_burns(img, t, direction="zoom_in"):
    """Ken Burns effect — slow zoom/pan on still image."""
    arr = np.array(img)
    ih, iw = arr.shape[:2]

    if direction == "zoom_in":
        scale = 1.0 + t * 0.15
        cx, cy = iw // 2, ih // 2
    elif direction == "zoom_out":
        scale = 1.15 - t * 0.15
        cx, cy = iw // 2, ih // 2
    elif direction == "pan_left":
        scale = 1.1
        cx = int(iw * (0.55 - t * 0.1))
        cy = ih // 2
    elif direction == "pan_right":
        scale = 1.1
        cx = int(iw * (0.45 + t * 0.1))
        cy = ih // 2
    else:
        scale = 1.0
        cx, cy = iw // 2, ih // 2

    crop_w = int(iw / scale)
    crop_h = int(ih / scale)
    x1 = max(0, cx - crop_w // 2)
    y1 = max(0, cy - crop_h // 2)
    x2 = min(iw, x1 + crop_w)
    y2 = min(ih, y1 + crop_h)

    cropped = img.crop((x1, y1, x2, y2))
    return cropped.resize((W, H), Image.LANCZOS)


def add_vignette(img, strength=0.4):
    """Darken edges."""
    arr = np.array(img, dtype=np.float64)
    h, w = arr.shape[:2]
    cy, cx = h / 2, w / 2
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    max_dist = np.sqrt(cx ** 2 + cy ** 2)
    vignette = 1.0 - strength * (dist / max_dist) ** 2
    arr *= vignette[:, :, np.newaxis]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def add_subtitles(img, text, font_size=42, y_pos=None):
    """Burn-in subtitle at bottom of frame."""
    draw = ImageDraw.Draw(img)
    font = get_font(FONT_SUB, font_size)

    words = text.split()
    lines = []
    current = ""
    max_width = W - 120
    for word in words:
        test = current + " " + word if current else word
        tw, _ = text_size(draw, test, font)
        if tw > max_width and current:
            lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)

    if y_pos is None:
        y_pos = H - 100 - len(lines) * (font_size + 10)

    line_height = font_size + 10
    total_h = len(lines) * line_height + 20
    overlay = Image.new("RGBA", (W, total_h), (0, 0, 0, 160))
    img_rgba = img.convert("RGBA")
    img_rgba.paste(overlay, (0, y_pos - 10), overlay)
    draw = ImageDraw.Draw(img_rgba)

    for i, line in enumerate(lines):
        tw, th = text_size(draw, line, font)
        x = (W - tw) // 2
        y = y_pos + i * line_height
        draw.text((x, y), line, font=font, fill=(255, 255, 255))

    return img_rgba.convert("RGB")


# ── Scene Discovery ──────────────────────────────────────────────

def find_scene_assets(scenes_dir):
    """Find scene files — prefers .mp4 over .png/.jpg per scene number."""
    assets = {}

    for ext in ["mp4", "mov", "webm"]:
        for f in glob.glob(os.path.join(scenes_dir, f"*.{ext}")):
            name = os.path.splitext(os.path.basename(f))[0]
            num = name.lstrip("0") or "0"
            if num not in assets:
                assets[num] = (f, "video")

    for ext in ["png", "jpg", "jpeg"]:
        for f in glob.glob(os.path.join(scenes_dir, f"*.{ext}")):
            name = os.path.splitext(os.path.basename(f))[0]
            num = name.lstrip("0") or "0"
            if num not in assets:
                assets[num] = (f, "image")

    sorted_assets = sorted(assets.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 0)
    return [(num, path, atype) for num, (path, atype) in sorted_assets]


# ── Clip Builders ────────────────────────────────────────────────

def make_image_clip(image_path, duration, kb_direction, subtitles, vignette_strength=0.3):
    """Создаёт moviepy VideoClip из статичной картинки с Ken Burns."""
    from moviepy import VideoClip

    img = Image.open(image_path).convert("RGB").resize((W, H), Image.LANCZOS)

    def make_frame(t):
        progress = t / max(duration - 0.01, 0.01)
        frame = ken_burns(img, progress, kb_direction)
        frame = add_vignette(frame, vignette_strength)
        # Субтитры
        for sub in subtitles:
            if sub["start"] <= t < sub["end"]:
                # Сдвигаем время субтитра к локальному времени клипа
                frame = add_subtitles(frame, sub["text"])
                break
        return np.array(frame)

    return VideoClip(make_frame, duration=duration)


def make_video_clip(video_path, subtitles, vignette_strength=0.3):
    """Создаёт moviepy clip из видеофайла."""
    from moviepy import VideoFileClip

    clip = VideoFileClip(video_path).resized((W, H))

    if not subtitles:
        return clip

    def add_subs(get_frame, t):
        frame_arr = get_frame(t)
        for sub in subtitles:
            if sub["start"] <= t < sub["end"]:
                pil_img = Image.fromarray(frame_arr)
                pil_img = add_subtitles(pil_img, sub["text"])
                return np.array(pil_img)
        return frame_arr

    return clip.transform(add_subs)


def make_title_card(title, subtitle="", duration_sec=2.5):
    """Generate title card clip."""
    from moviepy import VideoClip

    def make_frame(t):
        alpha = min((t / max(duration_sec - 0.01, 0.01)) * 3, 1.0)
        img = Image.new("RGB", (W, H), (10, 22, 40))
        draw = ImageDraw.Draw(img)

        font_big = get_font(FONT_IMPACT, 100)
        tw, th = text_size(draw, title, font_big)
        x = (W - tw) // 2
        y = H // 2 - th - 20
        color = tuple(int(255 * alpha) for _ in range(3))
        draw.text((x, y), title, font=font_big, fill=color)

        if subtitle:
            font_sm = get_font(FONT_SUB, 40)
            tw2, _ = text_size(draw, subtitle, font_sm)
            x2 = (W - tw2) // 2
            sub_color = tuple(int(180 * alpha) for _ in range(3))
            draw.text((x2, y + th + 30), subtitle, font=font_sm, fill=sub_color)

        img = add_vignette(img, 0.5)
        return np.array(img)

    return VideoClip(make_frame, duration=duration_sec)


# ── Main Assembly ────────────────────────────────────────────────

def assemble_episode(episode_id, srt_path=None, transition_duration=0.3, dry_run=False):
    """Assemble a full episode from assets."""
    paths = episode_paths(episode_id)
    scenes_dir = str(paths["scenes"])
    output_path = str(paths["output"])

    # Scenes
    if not os.path.isdir(scenes_dir):
        print(f"ОШИБКА: папка со сценами не найдена: {scenes_dir}")
        print(f"Положи файлы в {scenes_dir}")
        sys.exit(1)

    scene_assets = find_scene_assets(scenes_dir)
    if not scene_assets:
        print(f"ОШИБКА: нет файлов (mp4/png/jpg) в {scenes_dir}")
        sys.exit(1)

    n_videos = sum(1 for _, _, t in scene_assets if t == "video")
    n_images = sum(1 for _, _, t in scene_assets if t == "image")
    print(f"  Сцены: {len(scene_assets)} ({n_videos} видео + {n_images} картинок)")

    # SRT Subtitles
    subtitles = []
    if srt_path:
        subtitles = parse_srt(srt_path)
    elif paths["srt"].exists():
        subtitles = parse_srt(paths["srt"])
    if subtitles:
        print(f"  Субтитры: {len(subtitles)} блоков (SRT)")

    # Audio: mix.mp3 > full.mp3 > individual files
    audio_source = None
    mix_path = paths["mix"]
    voice_dir = paths["voice"]

    if mix_path.exists():
        audio_source = ("mix", str(mix_path))
        print(f"  Аудио: mix.mp3 (pre-mixed)")
    elif (voice_dir / "full.mp3").exists():
        audio_source = ("full", str(voice_dir / "full.mp3"))
        print(f"  Аудио: full.mp3")
    else:
        voice_files = sorted(glob.glob(str(voice_dir / "*.mp3")))
        voice_files = [f for f in voice_files if not Path(f).name.startswith("_")]
        if voice_files:
            audio_source = ("individual", voice_files)
            print(f"  Аудио: {len(voice_files)} отдельных файлов")
        else:
            print(f"  Аудио: нет")

    # Background music (only if NOT using mix.mp3)
    bg_music = None
    if audio_source and audio_source[0] != "mix":
        music_dir = str(paths["music"])
        for name in ["bg.mp3", "background.mp3", "music.mp3"]:
            p = os.path.join(music_dir, name)
            if os.path.exists(p):
                bg_music = p
                break
        if bg_music:
            print(f"  Музыка: {bg_music}")

    print(f"  Transition: dissolve {transition_duration}с")

    if dry_run:
        print(f"\n  === DRY RUN — рендер не выполнялся ===")
        return

    # ── Build clips ──────────────────────────────────────────
    from moviepy import (
        VideoFileClip, AudioFileClip, CompositeAudioClip,
        concatenate_videoclips, concatenate_audioclips,
    )
    import moviepy.video.fx as vfx

    kb_directions = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
    scene_duration = 5.0  # default per scene if no timing info

    # Try to load timing for scene durations
    timing = None
    if paths["timing"].exists():
        timing = json.loads(paths["timing"].read_text())

    clips = []

    # Title card
    print("  Заставка...")
    title_clip = make_title_card("AI OFFICE", f"Серия {episode_id}", 2.5)
    clips.append(title_clip)

    # Scene clips
    for idx, (num, scene_path, scene_type) in enumerate(scene_assets):
        basename = os.path.basename(scene_path)

        # Duration from timing if available
        dur = scene_duration
        if timing:
            shot = next(
                (s for s in timing.get("shots", []) if str(s["number"]) == num),
                None
            )
            if shot:
                start, end = parse_time_range(shot["time"])
                dur = end - start

        # Subtitles for this clip
        # SRT тайминги начинаются с 0:00 (начало серии, без title card)
        # content_start = время начала этого клипа в серии (без title card)
        content_start = sum(c.duration for c in clips) - 2.5  # вычитаем title card
        clip_subs = []
        for sub in subtitles:
            if sub["start"] < content_start + dur and sub["end"] > content_start:
                clip_subs.append({
                    "start": max(0, sub["start"] - content_start),
                    "end": min(dur, sub["end"] - content_start),
                    "text": sub["text"],
                })

        if scene_type == "video":
            print(f"    Кадр {idx + 1}/{len(scene_assets)}: {basename} (видео)")
            clip = make_video_clip(scene_path, clip_subs)
        else:
            kb = kb_directions[idx % len(kb_directions)]
            print(f"    Кадр {idx + 1}/{len(scene_assets)}: {basename} ({kb})")
            clip = make_image_clip(scene_path, dur, kb, clip_subs)

        # Dissolve transitions
        if transition_duration > 0 and len(clips) > 0:
            clip = clip.with_effects([vfx.CrossFadeIn(transition_duration)])
            if idx < len(scene_assets) - 1:
                clip = clip.with_effects([vfx.CrossFadeOut(transition_duration)])

        clips.append(clip)

    # End card
    end_clip = make_title_card("@rubelnick.ai", "AI Office", 2.0)
    clips.append(end_clip)

    # Concatenate
    print("  Склейка...")
    video = concatenate_videoclips(clips, method="compose")
    total_duration = video.duration

    # ── Audio ────────────────────────────────────────────────
    if audio_source:
        print("  Аудио...")
        if audio_source[0] == "mix":
            audio = AudioFileClip(audio_source[1])
            # Offset: skip title card
            audio = audio.with_start(2.5)
            video = video.with_audio(CompositeAudioClip([audio]))

        elif audio_source[0] == "full":
            audio = AudioFileClip(audio_source[1])
            audio = audio.with_start(2.5)
            audio_clips = [audio]
            if bg_music:
                music = AudioFileClip(bg_music)
                if music.duration < total_duration:
                    loops = int(total_duration / music.duration) + 1
                    music = concatenate_audioclips([music] * loops)
                music = music.subclipped(0, total_duration)
                music = music.with_volume_scaled(0.3 if audio_clips else 0.8)
                audio_clips.append(music)
            video = video.with_audio(CompositeAudioClip(audio_clips))

        elif audio_source[0] == "individual":
            v_clips = [AudioFileClip(f) for f in audio_source[1]]
            voice = concatenate_audioclips(v_clips)
            voice = voice.with_start(2.5)
            audio_clips = [voice]
            if bg_music:
                music = AudioFileClip(bg_music)
                if music.duration < total_duration:
                    loops = int(total_duration / music.duration) + 1
                    music = concatenate_audioclips([music] * loops)
                music = music.subclipped(0, total_duration)
                music = music.with_volume_scaled(0.3)
                audio_clips.append(music)
            video = video.with_audio(CompositeAudioClip(audio_clips))

    # ── Render ───────────────────────────────────────────────
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"  Рендер → {output_path}")
    video.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        bitrate="5000k",
        preset="medium",
        logger="bar",
    )
    video.close()

    print(f"\n{'=' * 50}")
    print(f"  ГОТОВО: {output_path}")
    print(f"  Длительность: {total_duration:.1f} сек")
    print(f"  Разрешение: {W}x{H}")
    print(f"{'=' * 50}")


# ── CLI ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="AI_SHOW Video Assembler v3")
    parser.add_argument("episode", help="Episode ID (e.g. S01E01)")
    parser.add_argument("--srt", help="Path to SRT subtitle file")
    parser.add_argument("--transition-duration", type=float, default=0.3,
                        help="Dissolve transition duration (default: 0.3s)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Показать план сборки без рендера")
    args = parser.parse_args()

    print(f"=== Video Assembler v3: {args.episode} ===\n")
    assemble_episode(
        args.episode,
        srt_path=args.srt,
        transition_duration=args.transition_duration,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
