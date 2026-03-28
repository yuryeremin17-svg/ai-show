#!/usr/bin/env python3
"""
AI_SHOW — Audio Mixer
Микширует голоса + музыку (с ducking) + SFX → единый mix.mp3.
Нормализация: -14 LUFS, -1.0 dBTP.

Использование:
  python3 scripts/audio_mix.py S01E01 [--dry-run] [--voice-only] [--no-sfx] [--no-music]
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import (
    LEVELS, DUCKING, TARGET_LUFS, TRUE_PEAK,
    episode_paths, get_audio_duration, parse_time_range,
)


# ── Voice Track Assembly ─────────────────────────────────────────

def build_voice_track(timing: dict, voice_dir: Path, output_path: Path) -> list[tuple[float, float]]:
    """Собирает голосовой трек из отдельных mp3 с правильными задержками.
    Returns list of (start, end) voice regions for ducking.
    """
    lines = timing["lines"]
    pauses = timing.get("pauses", [])
    voice_regions = []

    # Собираем список существующих файлов с задержками
    inputs = []
    for entry in lines:
        filepath = voice_dir / entry["file"]
        if not filepath.exists():
            continue
        start = entry["start"]
        duration = entry["duration"]
        inputs.append((str(filepath), start))
        voice_regions.append((start, start + duration))

    if not inputs:
        return voice_regions

    # ffmpeg: каждый файл с adelay, потом amix
    filter_parts = []
    input_args = []
    for i, (fpath, start_sec) in enumerate(inputs):
        input_args.extend(["-i", fpath])
        delay_ms = int(start_sec * 1000)
        if delay_ms > 0:
            filter_parts.append(f"[{i}]adelay={delay_ms}|{delay_ms}[v{i}]")
        else:
            filter_parts.append(f"[{i}]acopy[v{i}]")

    mix_inputs = "".join(f"[v{i}]" for i in range(len(inputs)))
    filter_parts.append(
        f"{mix_inputs}amix=inputs={len(inputs)}:duration=longest:normalize=0[voice]"
    )

    filter_complex = ";".join(filter_parts)

    cmd = [
        "ffmpeg", "-y",
        *input_args,
        "-filter_complex", filter_complex,
        "-map", "[voice]",
        "-ac", "1", "-ar", "44100",
        str(output_path),
    ]

    subprocess.run(cmd, capture_output=True, check=True)
    return voice_regions


def build_ducking_expression(voice_regions: list[tuple[float, float]]) -> str:
    """Строит ffmpeg volume expression для ducking музыки.
    Музыка тише когда голос есть, громче когда нет.
    """
    attack = DUCKING["attack"]
    release = DUCKING["release"]
    under_db = LEVELS["music_under"]  # -18
    alone_db = LEVELS["music_alone"]  # -9

    if not voice_regions:
        return f"volume={alone_db}dB"

    # Вложенная конструкция: if(between(...), under, if(..., under, alone))
    # С учётом attack/release для плавных переходов
    expr = f"{alone_db}"
    for start, end in reversed(voice_regions):
        expr = f"if(between(t,{start - attack:.2f},{end + release:.2f}),{under_db},{expr})"

    return f"volume='{expr}dB':eval=frame"


# ── SFX Detection ────────────────────────────────────────────────

def detect_sfx_cues(episode_id: str, timing: dict) -> list[dict]:
    """Извлекает SFX-подсказки из раскадровки."""
    script_path = episode_paths(episode_id)["script"]
    sfx_dir = episode_paths(episode_id)["sfx"]

    cues = []
    if not script_path.exists():
        return cues

    text = script_path.read_text(encoding="utf-8")
    shots = timing.get("shots", [])

    for shot in shots:
        # Ищем переходы — swoosh
        if shot["type"] == "transition":
            start, _ = parse_time_range(shot["time"])
            swoosh = sfx_dir / "swoosh.mp3"
            if swoosh.exists():
                cues.append({"file": str(swoosh), "start": start, "level": LEVELS["sfx_accent"]})

    # Telegram-звук перед telegram-репликами
    for line in timing["lines"]:
        if line.get("effect") == "telegram":
            tg_sound = sfx_dir / "telegram.mp3"
            if tg_sound.exists():
                # Telegram-звук за 0.5с до реплики
                cues.append({
                    "file": str(tg_sound),
                    "start": max(0, line["start"] - 0.5),
                    "level": LEVELS["sfx_accent"],
                })

    return cues


# ── Full Mix ─────────────────────────────────────────────────────

def build_mix_command(
    voice_path: Path,
    music_path: Path | None,
    sfx_cues: list[dict],
    voice_regions: list[tuple[float, float]],
    total_duration: float,
    output_path: Path,
) -> list[str]:
    """Строит ffmpeg-команду для финального микса."""
    input_args = ["-i", str(voice_path)]  # input 0 = voice
    filter_parts = []
    input_idx = 1

    # Музыка
    if music_path:
        input_args.extend(["-i", str(music_path)])
        ducking_expr = build_ducking_expression(voice_regions)
        filter_parts.append(f"[{input_idx}]{ducking_expr}[music]")
        input_idx += 1

    # SFX
    sfx_labels = []
    for cue in sfx_cues:
        input_args.extend(["-i", cue["file"]])
        delay_ms = int(cue["start"] * 1000)
        level_db = cue["level"]
        label = f"sfx{input_idx}"
        filter_parts.append(
            f"[{input_idx}]adelay={delay_ms}|{delay_ms},volume={level_db}dB[{label}]"
        )
        sfx_labels.append(f"[{label}]")
        input_idx += 1

    # Финальный микс
    mix_inputs = "[0]"  # voice
    mix_count = 1

    if music_path:
        mix_inputs += "[music]"
        mix_count += 1

    for label in sfx_labels:
        mix_inputs += label
        mix_count += 1

    if mix_count > 1:
        filter_parts.append(
            f"{mix_inputs}amix=inputs={mix_count}:duration=first:normalize=0[mixed]"
        )
        map_label = "[mixed]"
    else:
        map_label = "[0]"

    filter_complex = ";".join(filter_parts) if filter_parts else None

    cmd = ["ffmpeg", "-y", *input_args]
    if filter_complex:
        cmd.extend(["-filter_complex", filter_complex, "-map", map_label])
    cmd.extend(["-ac", "1", "-ar", "44100", "-t", str(total_duration), str(output_path)])

    return cmd


def normalize_lufs(input_path: Path, output_path: Path):
    """Два прохода loudnorm: измерение → применение."""
    # Pass 1: измерение
    cmd1 = [
        "ffmpeg", "-y", "-i", str(input_path), "-af",
        f"loudnorm=I={TARGET_LUFS}:TP={TRUE_PEAK}:LRA=11:print_format=json",
        "-f", "null", "-"
    ]
    result = subprocess.run(cmd1, capture_output=True, text=True)

    # Парсим JSON из stderr
    stderr = result.stderr
    json_start = stderr.rfind("{")
    json_end = stderr.rfind("}") + 1
    if json_start < 0:
        print("  [!] Не удалось измерить LUFS, копирую без нормализации")
        import shutil
        shutil.copy(input_path, output_path)
        return

    measurements = json.loads(stderr[json_start:json_end])

    # Pass 2: применение
    cmd2 = [
        "ffmpeg", "-y", "-i", str(input_path), "-af",
        f"loudnorm=I={TARGET_LUFS}:TP={TRUE_PEAK}:LRA=11"
        f":measured_I={measurements['input_i']}"
        f":measured_TP={measurements['input_tp']}"
        f":measured_LRA={measurements['input_lra']}"
        f":measured_thresh={measurements['input_thresh']}"
        f":offset={measurements['target_offset']}",
        str(output_path),
    ]
    subprocess.run(cmd2, capture_output=True, check=True)
    print(f"  Нормализация: {measurements['input_i']} → {TARGET_LUFS} LUFS")


# ── Main ─────────────────────────────────────────────────────────

def run_mix(
    episode_id: str,
    dry_run: bool = False,
    voice_only: bool = False,
    no_sfx: bool = False,
    no_music: bool = False,
):
    paths = episode_paths(episode_id)
    timing_path = paths["timing"]

    if not timing_path.exists():
        print(f"ОШИБКА: timing.json не найден: {timing_path}")
        sys.exit(1)

    timing = json.loads(timing_path.read_text())
    voice_dir = paths["voice"]
    total_duration = timing["total_duration"]

    # Голосовой трек
    voice_track = voice_dir / "_voice_track.mp3"
    print(f"  Сборка голосового трека...")

    # Проверяем наличие mp3 файлов
    voice_files = [voice_dir / e["file"] for e in timing["lines"] if (voice_dir / e["file"]).exists()]
    print(f"  Найдено голосовых файлов: {len(voice_files)} из {len(timing['lines'])}")

    if not voice_files:
        print("  [!] Голосовые файлы не найдены. Генерируй через voice_gen.py")
        if not dry_run:
            sys.exit(1)

    # Музыка
    music_path = None
    if not voice_only and not no_music:
        for name in ["bg.mp3", "background.mp3", "music.mp3"]:
            p = paths["music"] / name
            if p.exists():
                music_path = p
                break
        if music_path:
            print(f"  Музыка: {music_path}")
        else:
            print(f"  Музыка: не найдена в {paths['music']}")

    # SFX
    sfx_cues = []
    if not voice_only and not no_sfx:
        sfx_cues = detect_sfx_cues(episode_id, timing)
        if sfx_cues:
            print(f"  SFX: {len(sfx_cues)} подсказок")
            for c in sfx_cues:
                print(f"    {Path(c['file']).name} @ {c['start']:.1f}с ({c['level']}dB)")
        else:
            print(f"  SFX: нет (папка {paths['sfx']} пуста или не найдена)")

    # Voice regions для ducking
    voice_regions = [
        (e["start"], e["start"] + e["duration"])
        for e in timing["lines"]
    ]

    if dry_run:
        print(f"\n  === DRY RUN ===")
        print(f"  Голосовых регионов: {len(voice_regions)}")
        for start, end in voice_regions:
            print(f"    {start:.1f}с — {end:.1f}с")
        if music_path:
            expr = build_ducking_expression(voice_regions)
            print(f"\n  Ducking expression:\n    {expr[:200]}...")
        print(f"\n  Выход: {paths['mix']}")
        print(f"  Нормализация: {TARGET_LUFS} LUFS, {TRUE_PEAK} dBTP")
        return

    # Шаг 1: собираем голосовой трек
    if voice_files:
        voice_regions = build_voice_track(timing, voice_dir, voice_track)
        print(f"  Голосовой трек: {voice_track}")

    # Шаг 2: микс
    if voice_only or (not music_path and not sfx_cues):
        # Только голос — нормализуем и копируем
        mix_raw = voice_track
    else:
        mix_raw = voice_dir / "_mix_raw.mp3"
        cmd = build_mix_command(
            voice_track, music_path, sfx_cues,
            voice_regions, total_duration, mix_raw,
        )
        print(f"  Микширование...")
        subprocess.run(cmd, capture_output=True, check=True)

    # Шаг 3: нормализация LUFS
    output_path = paths["mix"]
    print(f"  Нормализация LUFS...")
    normalize_lufs(mix_raw, output_path)

    # Cleanup
    for tmp in [voice_dir / "_voice_track.mp3", voice_dir / "_mix_raw.mp3"]:
        if tmp.exists():
            tmp.unlink()

    duration = get_audio_duration(output_path)
    print(f"\n  === Микс готов: {output_path} ({duration:.1f}с) ===")


# ── CLI ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="AI_SHOW Audio Mixer")
    parser.add_argument("episode", help="Episode ID (e.g. S01E01)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Показать план микширования")
    parser.add_argument("--voice-only", action="store_true",
                        help="Только голосовой трек")
    parser.add_argument("--no-sfx", action="store_true",
                        help="Без SFX")
    parser.add_argument("--no-music", action="store_true",
                        help="Без музыки")
    args = parser.parse_args()

    print(f"=== Audio Mixer: {args.episode} ===\n")
    run_mix(
        args.episode,
        dry_run=args.dry_run,
        voice_only=args.voice_only,
        no_sfx=args.no_sfx,
        no_music=args.no_music,
    )


if __name__ == "__main__":
    main()
