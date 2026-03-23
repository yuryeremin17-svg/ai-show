#!/usr/bin/env python3
"""
AI_SHOW — Video Assembler v2.0
Собирает эпизод из: картинки/видеоклипы + голос + музыка → MP4

Использование:
  python3 scripts/assemble.py S01E01

Ожидаемая структура:
  assets/scenes/S01E01/       ← картинки (01.png) И/ИЛИ видеоклипы (01.mp4)
  assets/voice/S01E01/        ← озвучка (01.mp3, 02.mp3, ... или full.mp3)
  assets/music/               ← фоновая музыка (bg.mp3)
  assets/music/intro.mp3      ← джингл интро (опционально)
  episodes/                   ← выход (S01E01.mp4)

Сцены: если есть 01.mp4 — используется видеоклип (Kling/Runway img2vid),
        если нет — fallback на 01.png/jpg с Ken Burns эффектом.
        Можно миксовать: часть сцен видео, часть картинки.

Картинки: Midjourney или OpenAI DALL-E
Видеоклипы: Kling AI, Runway Gen-4, Seedance (img2vid)
Голос: ElevenLabs, gTTS, или записанный вручную
"""

import os
import sys
import math
import glob
import random
import re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ── Config ──────────────────────────────────────────────────────
W, H = 1080, 1920  # 9:16 vertical
FPS = 30
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Fonts (macOS)
FONT_TITLE = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_SUB = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"


def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()


def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


# ── Effects ─────────────────────────────────────────────────────

def ken_burns(img, t, direction="zoom_in"):
    """Ken Burns effect — slow zoom/pan on still image"""
    arr = np.array(img)
    ih, iw = arr.shape[:2]

    if direction == "zoom_in":
        scale = 1.0 + t * 0.15  # 1.0 → 1.15
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

    # Crop region
    crop_w = int(iw / scale)
    crop_h = int(ih / scale)
    x1 = max(0, cx - crop_w // 2)
    y1 = max(0, cy - crop_h // 2)
    x2 = min(iw, x1 + crop_w)
    y2 = min(ih, y1 + crop_h)

    cropped = img.crop((x1, y1, x2, y2))
    return cropped.resize((W, H), Image.LANCZOS)


def add_subtitles(img, text, font_size=42, y_pos=None, highlight_words=None):
    """Add subtitle text at bottom of frame"""
    draw = ImageDraw.Draw(img)
    font = get_font(FONT_SUB, font_size)

    # Word wrap
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

    # Semi-transparent background
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

        # Highlight keywords
        if highlight_words:
            # Draw word by word
            words_in_line = line.split()
            cur_x = x
            for word in words_in_line:
                ww, wh = text_size(draw, word + " ", font)
                clean_word = re.sub(r'[^\w]', '', word.lower())
                if any(clean_word == hw.lower() for hw in highlight_words):
                    draw.text((cur_x, y), word, font=font, fill=(255, 220, 50))
                else:
                    draw.text((cur_x, y), word, font=font, fill=(255, 255, 255))
                cur_x += ww
        else:
            draw.text((x, y), line, font=font, fill=(255, 255, 255))

    return img_rgba.convert("RGB")


def crossfade(img1, img2, t):
    """Crossfade between two images, t=0→img1, t=1→img2"""
    return Image.blend(img1, img2, t)


def add_vignette(img, strength=0.4):
    """Darken edges"""
    arr = np.array(img, dtype=np.float64)
    cy, cx = H / 2, W / 2
    Y, X = np.ogrid[:H, :W]
    dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    max_dist = np.sqrt(cx ** 2 + cy ** 2)
    vignette = 1.0 - strength * (dist / max_dist) ** 2
    arr *= vignette[:, :, np.newaxis]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


# ── Scene assembly ──────────────────────────────────────────────

def find_scene_assets(scenes_dir):
    """Find scene files — prefers .mp4 over .png/.jpg per scene number.
    Returns list of (number, path, type) sorted by number.
    type is 'video' or 'image'.
    """
    assets = {}  # number -> (path, type)

    # Scan for videos first (higher priority)
    for ext in ["mp4", "mov", "webm"]:
        for f in glob.glob(os.path.join(scenes_dir, f"*.{ext}")):
            name = os.path.splitext(os.path.basename(f))[0]
            num = name.lstrip("0") or "0"
            if num not in assets:  # video has priority
                assets[num] = (f, "video")

    # Then images (only if no video for that number)
    for ext in ["png", "jpg", "jpeg"]:
        for f in glob.glob(os.path.join(scenes_dir, f"*.{ext}")):
            name = os.path.splitext(os.path.basename(f))[0]
            num = name.lstrip("0") or "0"
            if num not in assets:
                assets[num] = (f, "image")

    # Sort by number
    sorted_assets = sorted(assets.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 0)
    return [(num, path, atype) for num, (path, atype) in sorted_assets]


def make_scene_frames(image_path, duration_sec, voice_text="",
                      kb_direction="zoom_in", transition="dissolve",
                      highlight_words=None):
    """Generate frames for one scene from a STILL IMAGE (Ken Burns)"""
    img = Image.open(image_path).convert("RGB")
    # Resize to fit 9:16
    img = img.resize((W, H), Image.LANCZOS)

    n_frames = int(duration_sec * FPS)
    fade_frames = int(0.5 * FPS)  # 0.5s crossfade
    frames = []

    for i in range(n_frames):
        t = i / max(n_frames - 1, 1)

        # Ken Burns
        frame = ken_burns(img, t, kb_direction)

        # Vignette
        frame = add_vignette(frame, 0.3)

        # Subtitles
        if voice_text:
            frame = add_subtitles(frame, voice_text,
                                  highlight_words=highlight_words)

        frames.append(frame)

    return frames, fade_frames


def make_video_scene_frames(video_path, voice_text="", highlight_words=None):
    """Extract frames from a VIDEO CLIP (Kling/Runway img2vid).
    Resizes to W×H, applies vignette and subtitles.
    Returns (frames, fade_frames).
    """
    from moviepy import VideoFileClip

    clip = VideoFileClip(video_path)

    # Resize to target resolution
    clip_resized = clip.resized((W, H))

    n_frames = int(clip.duration * FPS)
    fade_frames = int(0.5 * FPS)
    frames = []

    for i in range(n_frames):
        t = i / FPS
        if t >= clip.duration:
            break
        # Get frame as numpy array → PIL Image
        arr = clip_resized.get_frame(t)
        frame = Image.fromarray(arr)

        # Vignette (same as image scenes)
        frame = add_vignette(frame, 0.3)

        # Subtitles
        if voice_text:
            frame = add_subtitles(frame, voice_text,
                                  highlight_words=highlight_words)

        frames.append(frame)

    clip.close()
    return frames, fade_frames


def make_title_card(title, subtitle="", duration_sec=3.0):
    """Generate intro/title card frames"""
    n_frames = int(duration_sec * FPS)
    frames = []

    for i in range(n_frames):
        t = i / max(n_frames - 1, 1)
        # Fade in
        alpha = min(t * 3, 1.0)

        img = Image.new("RGB", (W, H), (10, 22, 40))
        draw = ImageDraw.Draw(img)

        # Title
        font_big = get_font(FONT_IMPACT, 100)
        tw, th = text_size(draw, title, font_big)
        x = (W - tw) // 2
        y = H // 2 - th - 20
        color = tuple(int(255 * alpha) for _ in range(3))
        draw.text((x, y), title, font=font_big, fill=color)

        # Subtitle
        if subtitle:
            font_sm = get_font(FONT_SUB, 40)
            tw2, th2 = text_size(draw, subtitle, font_sm)
            x2 = (W - tw2) // 2
            sub_color = tuple(int(180 * alpha) for _ in range(3))
            draw.text((x2, y + th + 30), subtitle, font=font_sm, fill=sub_color)

        frames.append(add_vignette(img, 0.5))

    return frames


# ── Main assembly ───────────────────────────────────────────────

def assemble_episode(episode_id):
    """Assemble a full episode from assets"""

    scenes_dir = os.path.join(PROJECT_ROOT, "assets", "scenes", episode_id)
    voice_dir = os.path.join(PROJECT_ROOT, "assets", "voice", episode_id)
    music_dir = os.path.join(PROJECT_ROOT, "assets", "music")
    output_path = os.path.join(PROJECT_ROOT, "episodes", f"{episode_id}.mp4")

    # Check scenes
    if not os.path.isdir(scenes_dir):
        print(f"ERROR: Папка со сценами не найдена: {scenes_dir}")
        print(f"Положи файлы как 01.mp4/01.png, 02.mp4/02.png, ... в {scenes_dir}")
        sys.exit(1)

    scene_assets = find_scene_assets(scenes_dir)
    if not scene_assets:
        print(f"ERROR: Нет файлов сцен (mp4/png/jpg) в {scenes_dir}")
        sys.exit(1)

    n_videos = sum(1 for _, _, t in scene_assets if t == "video")
    n_images = sum(1 for _, _, t in scene_assets if t == "image")
    print(f"Найдено {len(scene_assets)} сцен: {n_videos} видео + {n_images} картинок")

    # Check voice (optional)
    voice_files = []
    full_voice = None
    if os.path.isdir(voice_dir):
        voice_files = sorted(glob.glob(os.path.join(voice_dir, "*.mp3")))
        full_voice_path = os.path.join(voice_dir, "full.mp3")
        if os.path.exists(full_voice_path):
            full_voice = full_voice_path
            print(f"Озвучка: цельный файл (full.mp3)")
        elif voice_files:
            print(f"Озвучка: {len(voice_files)} файлов")
        else:
            print("Озвучка: нет файлов (видео без голоса)")
    else:
        print(f"Озвучка: папка {voice_dir} не найдена (видео без голоса)")

    # Check background music (optional)
    bg_music = None
    for name in ["bg.mp3", "background.mp3", "music.mp3"]:
        p = os.path.join(music_dir, name)
        if os.path.exists(p):
            bg_music = p
            break
    if bg_music:
        print(f"Фоновая музыка: {bg_music}")

    # Ken Burns directions — cycle through
    kb_directions = ["zoom_in", "zoom_out", "pan_left", "pan_right"]

    # Duration per scene (default: voice length or 5 sec)
    scene_duration = 5.0  # default per scene

    # Generate all frames
    all_frames = []

    # Title card
    print("Генерирую заставку...")
    title_frames = make_title_card(
        f"AI OFFICE",
        f"Серия {episode_id}",
        duration_sec=2.5
    )
    all_frames.extend(title_frames)

    # Scenes
    for idx, (num, scene_path, scene_type) in enumerate(scene_assets):
        basename = os.path.basename(scene_path)

        if scene_type == "video":
            print(f"  Кадр {idx+1}/{len(scene_assets)}: {basename} (видеоклип)")
            scene_frames, fade_n = make_video_scene_frames(scene_path)
        else:
            kb = kb_directions[idx % len(kb_directions)]
            print(f"  Кадр {idx+1}/{len(scene_assets)}: {basename} ({kb})")
            scene_frames, fade_n = make_scene_frames(
                scene_path,
                duration_sec=scene_duration,
                kb_direction=kb
            )

        # Crossfade with previous
        if all_frames and fade_n > 0:
            for fi in range(min(fade_n, len(all_frames), len(scene_frames))):
                t = fi / fade_n
                blended = crossfade(all_frames[-(fade_n - fi)], scene_frames[fi], t)
                all_frames[-(fade_n - fi)] = blended
            all_frames.extend(scene_frames[fade_n:])
        else:
            all_frames.extend(scene_frames)

    # End card
    end_frames = make_title_card("@rubelnick.ai", "AI Office", duration_sec=2.0)
    all_frames.extend(end_frames)

    total_frames = len(all_frames)
    total_duration = total_frames / FPS
    print(f"\nВсего: {total_frames} кадров, {total_duration:.1f} сек")

    # Save frames to temp
    import tempfile
    tmp_dir = tempfile.mkdtemp(prefix="aishow_")
    print(f"Сохраняю кадры в {tmp_dir}...")
    for i, frame in enumerate(all_frames):
        frame.save(os.path.join(tmp_dir, f"f_{i:05d}.png"))
        if (i + 1) % 100 == 0:
            print(f"  {i+1}/{total_frames}")

    # Assemble with moviepy
    print("Собираю видео...")
    from moviepy import ImageSequenceClip, AudioFileClip, CompositeAudioClip

    frame_paths = [os.path.join(tmp_dir, f"f_{i:05d}.png") for i in range(total_frames)]
    clip = ImageSequenceClip(frame_paths, fps=FPS)

    # Audio layers
    audio_clips = []

    if full_voice:
        voice_clip = AudioFileClip(full_voice)
        audio_clips.append(voice_clip)
    elif voice_files:
        # Per-scene voice files — concatenate
        from moviepy import concatenate_audioclips
        v_clips = [AudioFileClip(vf) for vf in voice_files]
        voice_clip = concatenate_audioclips(v_clips)
        audio_clips.append(voice_clip)

    if bg_music:
        music_clip = AudioFileClip(bg_music)
        # Loop if shorter than video
        if music_clip.duration < total_duration:
            loops = int(total_duration / music_clip.duration) + 1
            from moviepy import concatenate_audioclips
            music_clip = concatenate_audioclips([music_clip] * loops)
        music_clip = music_clip.subclipped(0, total_duration)
        # Lower volume for background
        music_clip = music_clip.with_volume_scaled(0.3 if audio_clips else 0.8)
        audio_clips.append(music_clip)

    if audio_clips:
        if len(audio_clips) > 1:
            final_audio = CompositeAudioClip(audio_clips)
        else:
            final_audio = audio_clips[0]
        clip = clip.with_audio(final_audio)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    clip.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        bitrate="5000k",
        preset="medium",
        logger="bar"
    )

    # Cleanup temp frames
    import shutil
    shutil.rmtree(tmp_dir, ignore_errors=True)

    print(f"\n{'='*50}")
    print(f"  ГОТОВО: {output_path}")
    print(f"  Длительность: {total_duration:.1f} сек")
    print(f"  Разрешение: {W}x{H}")
    print(f"{'='*50}")
    return output_path


# ── CLI ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 scripts/assemble.py S01E01")
        print("")
        print("Структура:")
        print("  assets/scenes/S01E01/  ← видео (01.mp4) и/или картинки (01.png)")
        print("                           видео приоритетнее: 01.mp4 > 01.png")
        print("  assets/voice/S01E01/   ← озвучка (01.mp3 или full.mp3)")
        print("  assets/music/bg.mp3    ← фоновая музыка")
        sys.exit(1)

    episode = sys.argv[1]
    assemble_episode(episode)
