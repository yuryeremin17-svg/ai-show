#!/usr/bin/env python3
"""
AI_SHOW — Animatic Builder
Строит черновой аниматик из timing.json + голосов: цветные плашки с текстом.
Проверяет ритм ДО генерации в Midjourney.

Использование:
  python3 scripts/animatic.py S01E01 [--dry-run] [--no-audio]
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from config import (
    W, H, FPS, FONT_TITLE, FONT_SUB,
    SCENE_COLORS, episode_paths, parse_time_range,
)


def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap_text(text: str, font, max_width: int, draw: ImageDraw.Draw) -> list[str]:
    """Word wrap для текста."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > max_width and current:
            lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)
    return lines


def make_placeholder_frame(
    shot_number: int,
    shot_name: str,
    shot_type: str,
    description: str,
    voice_text: str,
    character: str,
) -> np.ndarray:
    """Создаёт цветную плашку-placeholder для одного шота."""
    color = SCENE_COLORS.get(shot_type, SCENE_COLORS["animated"])
    img = Image.new("RGB", (W, H), color)
    draw = ImageDraw.Draw(img)

    font_big = get_font(FONT_TITLE, 56)
    font_mid = get_font(FONT_SUB, 38)
    font_sm = get_font(FONT_SUB, 32)

    max_w = W - 100
    y = 120

    # Бейдж типа шота
    badge_colors = {"real": (30, 70, 130), "animated": (170, 100, 20), "transition": (100, 40, 120)}
    badge_color = badge_colors.get(shot_type, (80, 80, 80))
    badge_text = {"real": "РЕАЛЬНОЕ ВИДЕО", "animated": "МУЛЬТИК", "transition": "ПЕРЕХОД"}.get(shot_type, shot_type)
    badge_font = get_font(FONT_SUB, 28)
    bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rounded_rectangle(
        [W - bw - 60, 40, W - 30, 40 + bh + 20],
        radius=10, fill=badge_color
    )
    draw.text((W - bw - 45, 47), badge_text, font=badge_font, fill=(255, 255, 255))

    # Заголовок шота
    header = f"ШОТ {shot_number}"
    draw.text((50, y), header, font=font_big, fill=(255, 255, 255))
    y += 70

    # Название
    draw.text((50, y), shot_name, font=font_mid, fill=(255, 255, 255, 200))
    y += 60

    # Разделитель
    draw.line([(50, y), (W - 50, y)], fill=(255, 255, 255, 100), width=2)
    y += 30

    # Описание (ВИЗУАЛ)
    if description:
        desc_lines = wrap_text(description, font_sm, max_w, draw)
        for dl in desc_lines[:6]:
            draw.text((50, y), dl, font=font_sm, fill=(220, 220, 220))
            y += 42
        y += 20

    # Нижняя часть: голос
    if voice_text:
        voice_y = H - 400
        draw.line([(50, voice_y - 20), (W - 50, voice_y - 20)], fill=(255, 255, 255, 100), width=2)

        # Персонаж
        char_font = get_font(FONT_TITLE, 36)
        draw.text((50, voice_y), character, font=char_font, fill=(255, 220, 50))
        voice_y += 50

        # Текст реплики
        voice_lines = wrap_text(voice_text, font_sm, max_w, draw)
        for vl in voice_lines[:5]:
            draw.text((50, voice_y), vl, font=font_sm, fill=(255, 255, 255))
            voice_y += 42

    return np.array(img)


def make_pause_frame(duration: float) -> np.ndarray:
    """Тёмная плашка для паузы."""
    img = Image.new("RGB", (W, H), (20, 20, 30))
    draw = ImageDraw.Draw(img)
    font = get_font(FONT_TITLE, 64)
    text = f"ПАУЗА {duration}с"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H // 2 - 40), text, font=font, fill=(120, 120, 140))
    return np.array(img)


def build_animatic(episode_id: str, no_audio: bool = False, dry_run: bool = False):
    """Собирает аниматик из timing.json + голосов."""
    paths = episode_paths(episode_id)
    timing_path = paths["timing"]

    if not timing_path.exists():
        print(f"ОШИБКА: timing.json не найден: {timing_path}")
        print("Сначала запусти: python3 scripts/voice_gen.py S01E01 --dry-run")
        sys.exit(1)

    timing = json.loads(timing_path.read_text())
    voice_lines = timing["lines"]
    pauses = timing.get("pauses", [])
    shots_data = timing.get("shots", [])

    # Группируем реплики по шотам
    shots_voices = {}
    for vl in voice_lines:
        shots_voices.setdefault(vl["shot"], []).append(vl)

    # Собираем таймлайн шотов
    timeline = []
    for shot in shots_data:
        start, end = parse_time_range(shot["time"])
        shot_duration = end - start

        # Голоса в этом шоте
        shot_vls = shots_voices.get(shot["number"], [])
        voice_text = " | ".join(
            f'{vl["character"]}: "{vl["text"][:50]}"' for vl in shot_vls
        )
        character = ", ".join(set(vl["character"] for vl in shot_vls)) or "—"

        timeline.append({
            "type": "shot",
            "shot": shot,
            "duration": shot_duration,
            "voice_text": voice_text,
            "character": character,
            "voice_files": [
                (paths["voice"] / vl["file"], vl["start"])
                for vl in shot_vls
            ],
        })

        # Пауза после этого шота?
        for p in pauses:
            last_vl_in_shot = max(
                (vl["index"] for vl in shot_vls), default=0
            )
            if p["after_index"] == last_vl_in_shot:
                timeline.append({
                    "type": "pause",
                    "duration": p["duration"],
                })

    total_dur = sum(item["duration"] for item in timeline)

    print(f"  Таймлайн: {len(timeline)} блоков, {total_dur:.1f}с")
    for item in timeline:
        if item["type"] == "shot":
            s = item["shot"]
            print(f"    Шот {s['number']} [{s['type']}] {s['name']} — {item['duration']:.1f}с")
        else:
            print(f"    ПАУЗА — {item['duration']:.1f}с")

    if dry_run:
        print(f"\n  === DRY RUN — рендер не выполнялся ===")
        return

    # Рендер через moviepy
    from moviepy import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips

    clips = []
    audio_clips = []
    current_time = 0.0

    for item in timeline:
        dur = item["duration"]

        if item["type"] == "pause":
            frame = make_pause_frame(dur)
            clip = ImageClip(frame, duration=dur)
            clips.append(clip)

        elif item["type"] == "shot":
            shot = item["shot"]
            frame = make_placeholder_frame(
                shot_number=shot["number"],
                shot_name=shot["name"],
                shot_type=shot["type"],
                description=shot.get("description", ""),
                voice_text=item["voice_text"],
                character=item["character"],
            )
            clip = ImageClip(frame, duration=dur)
            clips.append(clip)

            # Аудио
            if not no_audio:
                for filepath, abs_start in item["voice_files"]:
                    if filepath.exists():
                        ac = AudioFileClip(str(filepath))
                        ac = ac.with_start(abs_start)
                        audio_clips.append(ac)

        current_time += dur

    # Склейка
    video = concatenate_videoclips(clips, method="chain")

    if audio_clips:
        audio = CompositeAudioClip(audio_clips)
        video = video.with_audio(audio)

    # Рендер
    output_path = paths["animatic"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"\n  Рендер → {output_path}")
    video.write_videofile(
        str(output_path),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        bitrate="3000k",
        preset="fast",
        logger="bar",
    )
    video.close()

    print(f"\n  === Аниматик готов: {output_path} ({total_dur:.1f}с) ===")


# ── CLI ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="AI_SHOW Animatic Builder")
    parser.add_argument("episode", help="Episode ID (e.g. S01E01)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Показать таймлайн без рендера")
    parser.add_argument("--no-audio", action="store_true",
                        help="Без голосов (только видео)")
    args = parser.parse_args()

    print(f"=== Animatic Builder: {args.episode} ===\n")
    build_animatic(args.episode, no_audio=args.no_audio, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
