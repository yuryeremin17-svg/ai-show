#!/usr/bin/env python3
"""
AI_SHOW — Voice Generator
Парсит раскадровку → генерирует голоса через ElevenLabs → timing.json + SRT.

Использование:
  python3 scripts/voice_gen.py S01E01 [--dry-run] [--skip-existing] [--character КЛОДИЩЕ]
"""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import (
    PROJECT_ROOT, VOICE_PROFILES, GENITIVE_TO_NOM, MODEL_ID, OUTPUT_FORMAT,
    episode_paths, get_audio_duration, normalize_character, load_env,
    parse_time_range,
)


# ── Data structures ──────────────────────────────────────────────

@dataclass
class VoiceLine:
    index: int
    shot: int
    character: str       # именительный падеж: ЮРИЙ, КЛОДИЩЕ
    text: str
    voice_type: str      # на камеру, закадровый, telegram, прямая речь
    source: str = "elevenlabs"   # elevenlabs | real_recording
    effect: str | None = None    # telegram | None


@dataclass
class Pause:
    after_index: int
    duration: float
    note: str = ""


@dataclass
class ShotInfo:
    number: int
    name: str
    type: str            # real | animated | transition
    time: str            # "0:00-0:10"
    description: str


# ── Parser ───────────────────────────────────────────────────────

def detect_voice_type(type_str: str) -> tuple[str, str | None]:
    """Определяет тип голоса и эффект из описания.
    Returns (voice_type, effect)
    """
    lower = type_str.lower() if type_str else ""
    if "telegram" in lower or "голосовое" in lower:
        return "telegram", "telegram"
    if "на камеру" in lower:
        return "на камеру", None
    if "закадр" in lower:
        return "закадровый", None
    if "прямая" in lower:
        return "прямая речь", None
    return type_str or "прямая речь", None


def detect_shot_type(type_str: str) -> str:
    """'реальное видео' → 'real', 'мультик' → 'animated', 'переход' → 'transition'."""
    lower = type_str.lower()
    if "реальн" in lower:
        return "real"
    # "переход (Seedance)" — но НЕ "мультик (Midjourney → Seedance)"
    if "переход" in lower:
        return "transition"
    if lower.startswith("seedance") and "мультик" not in lower and "midjourney" not in lower:
        return "transition"
    return "animated"


def parse_storyboard(episode_id: str) -> tuple[list[VoiceLine], list[Pause], list[ShotInfo]]:
    """Парсит раскадровку. Приоритет: Карта голосов + Текст озвучки → inline ГОЛОС."""
    script_path = episode_paths(episode_id)["script"]
    if not script_path.exists():
        print(f"ОШИБКА: раскадровка не найдена: {script_path}")
        sys.exit(1)

    text = script_path.read_text(encoding="utf-8")
    lines_raw = text.split("\n")

    # ── Шаг 1: парсим шоты (заголовки + ТИП + ВИЗУАЛ) ────────
    shots = []
    current_shot_num = 0
    current_shot_name = ""
    current_shot_time = ""
    current_shot_type = "animated"
    current_shot_desc = ""

    for line in lines_raw:
        # ## ШОТ 2 — МИР АГЕНТОВ: ОТКАЗ [0:10-0:22]
        shot_match = re.match(
            r'^##\s+ШОТ\s+(\d+)\s*[—–-]\s*(.+?)\s*\[([0-9:.-]+)\]\s*$', line
        )
        if shot_match:
            # Сохраним предыдущий шот
            if current_shot_num > 0:
                shots.append(ShotInfo(
                    number=current_shot_num, name=current_shot_name,
                    type=current_shot_type, time=current_shot_time,
                    description=current_shot_desc.strip()
                ))
            current_shot_num = int(shot_match.group(1))
            current_shot_name = shot_match.group(2).strip()
            current_shot_time = shot_match.group(3).strip()
            current_shot_type = "animated"
            current_shot_desc = ""
            continue

        # **ТИП:** реальное видео  ИЛИ  ТИП: реальное видео
        type_match = re.match(r'^\*{0,2}ТИП:?\*{0,2}\s*(.+)$', line)
        if type_match and current_shot_num > 0:
            current_shot_type = detect_shot_type(type_match.group(1))
            continue

        # **ВИЗУАЛ:** описание  ИЛИ  ВИЗУАЛ: описание
        vis_match = re.match(r'^\*{0,2}ВИЗУАЛ:?\*{0,2}\s*(.+)$', line)
        if vis_match and current_shot_num > 0:
            current_shot_desc = vis_match.group(1).strip()

    # Последний шот
    if current_shot_num > 0:
        shots.append(ShotInfo(
            number=current_shot_num, name=current_shot_name,
            type=current_shot_type, time=current_shot_time,
            description=current_shot_desc.strip()
        ))

    # ── Шаг 2: парсим "Карта голосов" ────────────────────────
    voice_map_entries = []
    in_voice_map = False
    for line in lines_raw:
        if "Карта голосов" in line:
            in_voice_map = True
            continue
        if in_voice_map:
            if line.startswith("---") or (line.startswith("##") and "Карта" not in line):
                in_voice_map = False
                continue
            # | Шот 2 | Юрий | Закадровый (ElevenLabs клон) | 0:10-0:12 |
            row = re.match(
                r'\|\s*Шот\s+(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*([0-9:.-]+)\s*\|',
                line
            )
            if row:
                voice_map_entries.append({
                    "shot": int(row.group(1)),
                    "character": normalize_character(row.group(2).strip()),
                    "type_desc": row.group(3).strip(),
                    "time": row.group(4).strip(),
                })

    # ── Шаг 3: парсим "Текст озвучки" секции ─────────────────
    voice_texts = {}  # character -> [text1, text2, ...]
    current_char = None
    collecting = False
    for line in lines_raw:
        # ## Текст озвучки — ЮРИЙ (рассказчик)
        text_section = re.match(
            r'^##\s+Текст озвучки\s*[—–-]\s*(\w+)', line
        )
        if text_section:
            current_char = normalize_character(text_section.group(1))
            voice_texts.setdefault(current_char, [])
            collecting = True
            continue
        if collecting:
            if line.startswith("##"):
                collecting = False
                current_char = None
                continue
            if line.startswith("---"):
                collecting = False
                current_char = None
                continue
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("*") and stripped.endswith("*"):
                # *(без реплик — камео)* или *(Telegram-голосовое)*
                continue
            # Убираем кавычки если есть
            cleaned = stripped.strip('""\u201c\u201d')
            if cleaned:
                voice_texts[current_char].append(cleaned)

    # ── Шаг 4: собираем VoiceLines ───────────────────────────
    voice_lines = []
    pauses = []

    if voice_map_entries and voice_texts:
        # Основной путь: Карта голосов + Текст озвучки
        text_cursors = {char: 0 for char in voice_texts}

        for entry in voice_map_entries:
            char = entry["character"]
            voice_type, effect = detect_voice_type(entry["type_desc"])

            # Найти тип шота
            shot_info = next((s for s in shots if s.number == entry["shot"]), None)
            source = "real_recording" if (
                shot_info and shot_info.type == "real" and voice_type == "на камеру"
            ) else "elevenlabs"

            # Взять следующий текст для этого персонажа
            char_key = char
            if char_key == "ЮРИЙ" and char_key in voice_texts:
                pass
            elif char_key not in voice_texts:
                # Пропускаем если нет текста
                continue

            cursor = text_cursors.get(char_key, 0)
            if cursor < len(voice_texts.get(char_key, [])):
                line_text = voice_texts[char_key][cursor]
                text_cursors[char_key] = cursor + 1
            else:
                continue

            voice_lines.append(VoiceLine(
                index=len(voice_lines) + 1,
                shot=entry["shot"],
                character=char,
                text=line_text,
                voice_type=voice_type,
                source=source,
                effect=effect,
            ))
    else:
        # Fallback: inline ГОЛОС из шотов
        voice_lines, pauses = _parse_inline_voices(lines_raw, shots)

    # ── Шаг 5: парсим паузы (привязка к шоту) ────────────────
    current_pause_shot = 0
    for line in lines_raw:
        shot_match = re.match(r'^##\s+ШОТ\s+(\d+)', line)
        if shot_match:
            current_pause_shot = int(shot_match.group(1))
        pause_match = re.match(r'^\*{0,2}ПАУЗА\*{0,2}\s*\((\d+)\s*сек', line)
        if pause_match:
            duration = float(pause_match.group(1))
            # Найти последнюю реплику в этом шоте
            after_idx = 0
            for vl in voice_lines:
                if vl.shot == current_pause_shot:
                    after_idx = vl.index
            pauses.append(Pause(
                after_index=after_idx,
                duration=duration,
                note="из раскадровки",
            ))

    return voice_lines, pauses, shots


def _parse_inline_voices(lines_raw, shots) -> tuple[list[VoiceLine], list[Pause]]:
    """Fallback: парсит inline ГОЛОС из шотов."""
    voice_lines = []
    pauses = []
    current_shot = 0
    pending_voice_header = None  # (character, voice_type, effect)

    for line in lines_raw:
        # Детектим шот
        shot_match = re.match(r'^##\s+ШОТ\s+(\d+)', line)
        if shot_match:
            current_shot = int(shot_match.group(1))
            continue

        # Формат А: **ГОЛОС ЮРИЯ (закадровый):** "текст"
        # Формат Б: ГОЛОС ЮРИЙ (закадровый): "текст"
        voice_match = re.match(
            r'^\*{0,2}ГОЛОС\s+(\w+)\s*(?:\(([^)]*)\))?\s*:?\*{0,2}:?\s*(.*)',
            line
        )
        if voice_match:
            raw_name = voice_match.group(1)
            type_desc = voice_match.group(2) or ""
            rest = voice_match.group(3).strip()
            character = normalize_character(raw_name)
            voice_type, effect = detect_voice_type(type_desc)

            # Текст на этой же строке?
            text_match = re.search(r'["\u201c](.+?)["\u201d]', rest)
            if text_match:
                shot_info = next((s for s in shots if s.number == current_shot), None)
                source = "real_recording" if (
                    shot_info and shot_info.type == "real" and voice_type == "на камеру"
                ) else "elevenlabs"
                voice_lines.append(VoiceLine(
                    index=len(voice_lines) + 1,
                    shot=current_shot,
                    character=character,
                    text=text_match.group(1),
                    voice_type=voice_type,
                    source=source,
                    effect=effect,
                ))
                pending_voice_header = None
            else:
                # Текст на следующей строке
                pending_voice_header = (character, voice_type, effect)
            continue

        # Текст на следующей строке после заголовка ГОЛОС
        if pending_voice_header:
            text_match = re.search(r'["\u201c](.+?)["\u201d]', line)
            if text_match:
                char, vtype, eff = pending_voice_header
                shot_info = next((s for s in shots if s.number == current_shot), None)
                source = "real_recording" if (
                    shot_info and shot_info.type == "real" and vtype == "на камеру"
                ) else "elevenlabs"
                voice_lines.append(VoiceLine(
                    index=len(voice_lines) + 1,
                    shot=current_shot,
                    character=char,
                    text=text_match.group(1),
                    voice_type=vtype,
                    source=source,
                    effect=eff,
                ))
            pending_voice_header = None

    return voice_lines, pauses


# ── ElevenLabs Generation ────────────────────────────────────────

def apply_telegram_filter(input_path: Path) -> None:
    """Применяет эффект Telegram voice message (bandpass + compression)."""
    tmp_path = input_path.with_suffix(".tmp.mp3")
    cmd = [
        "ffmpeg", "-y", "-i", str(input_path), "-af",
        "highpass=f=300,"
        "lowpass=f=3400,"
        "acompressor=threshold=0.05:ratio=4:attack=5:release=50:makeup=3,"
        "equalizer=f=1000:t=q:w=0.5:g=3,"
        "volume=0.9",
        str(tmp_path)
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    tmp_path.rename(input_path)


def generate_voices(
    episode_id: str,
    voice_lines: list[VoiceLine],
    skip_existing: bool = False,
    character_filter: str | None = None,
):
    """Генерирует аудиофайлы через ElevenLabs API."""
    from elevenlabs import ElevenLabs, VoiceSettings

    load_env()
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("ОШИБКА: ELEVENLABS_API_KEY не найден. Добавь в .env")
        sys.exit(1)

    client = ElevenLabs(api_key=api_key)
    paths = episode_paths(episode_id)
    voice_dir = paths["voice"]
    voice_dir.mkdir(parents=True, exist_ok=True)

    for vl in voice_lines:
        if character_filter and vl.character != character_filter.upper():
            continue

        # Определяем профиль
        profile_key = "ЮРИЙ_TG" if vl.effect == "telegram" else vl.character
        profile = VOICE_PROFILES.get(profile_key) or VOICE_PROFILES.get(vl.character)
        if not profile:
            print(f"  [!] Нет профиля для {vl.character}, пропускаю")
            continue

        voice_id = profile["voice_id"]
        if not voice_id:
            print(f"  [!] voice_id не задан для {vl.character}. Задай в config.py")
            continue

        filename = f"{vl.index:02d}_{vl.character.lower()}_shot{vl.shot}.mp3"
        output_path = voice_dir / filename

        if skip_existing and output_path.exists():
            print(f"  [{vl.index}] {vl.character}: пропускаю (файл есть)")
            continue

        print(f"  [{vl.index}] {vl.character} ({vl.voice_type}): {vl.text[:60]}...")

        settings = VoiceSettings(
            stability=profile["stability"],
            similarity_boost=profile["similarity_boost"],
            style=profile["style"],
            speed=profile["speed"],
            use_speaker_boost=profile.get("speaker_boost", False),
        )

        audio_iter = client.text_to_speech.convert(
            voice_id=voice_id,
            text=vl.text,
            model_id=MODEL_ID,
            language_code="ru",
            output_format=OUTPUT_FORMAT,
            voice_settings=settings,
            apply_text_normalization="on",
        )

        audio_bytes = b"".join(audio_iter)
        output_path.write_bytes(audio_bytes)

        print(f"    → {filename} ({len(audio_bytes)} bytes)")

        # Telegram-фильтр
        if vl.effect == "telegram":
            apply_telegram_filter(output_path)
            print(f"    → telegram filter applied")

    print(f"\n  Голоса сохранены в {voice_dir}")


# ── Timing & SRT ─────────────────────────────────────────────────

def build_timing(
    episode_id: str,
    voice_lines: list[VoiceLine],
    pauses: list[Pause],
    shots: list[ShotInfo],
) -> dict:
    """Строит timing.json: измеряет длительности, расставляет start."""
    paths = episode_paths(episode_id)
    voice_dir = paths["voice"]

    timing_lines = []
    current_time = 0.0

    for vl in voice_lines:
        filename = f"{vl.index:02d}_{vl.character.lower()}_shot{vl.shot}.mp3"
        filepath = voice_dir / filename

        if filepath.exists():
            duration = get_audio_duration(filepath)
        else:
            # Для dry-run или если файл не создан — берём из раскадровки
            shot_info = next((s for s in shots if s.number == vl.shot), None)
            if shot_info:
                start, end = parse_time_range(shot_info.time)
                duration = (end - start) / max(
                    1, sum(1 for v in voice_lines if v.shot == vl.shot)
                )
            else:
                duration = 3.0  # fallback

        entry = {
            "index": vl.index,
            "file": filename,
            "shot": vl.shot,
            "character": vl.character,
            "voice_type": vl.voice_type,
            "source": vl.source,
            "text": vl.text,
            "duration": round(duration, 2),
            "start": round(current_time, 2),
        }
        if vl.effect:
            entry["effect"] = vl.effect

        timing_lines.append(entry)
        current_time += duration

        # Пауза после этой реплики?
        for p in pauses:
            if p.after_index == vl.index:
                current_time += p.duration

    timing = {
        "episode": episode_id,
        "total_duration": round(current_time, 2),
        "lines": timing_lines,
        "pauses": [asdict(p) for p in pauses],
        "shots": [asdict(s) for s in shots],
    }
    return timing


def save_timing(episode_id: str, timing: dict):
    """Сохраняет timing.json."""
    paths = episode_paths(episode_id)
    paths["voice"].mkdir(parents=True, exist_ok=True)
    timing_path = paths["timing"]
    timing_path.write_text(json.dumps(timing, ensure_ascii=False, indent=2))
    print(f"  timing.json → {timing_path}")


def save_srt(episode_id: str, timing: dict):
    """Генерирует SRT из timing.json."""
    paths = episode_paths(episode_id)
    srt_path = paths["srt"]

    def fmt_time(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        ms = int((sec % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    srt_lines = []
    for i, entry in enumerate(timing["lines"]):
        start = entry["start"]
        end = start + entry["duration"]
        srt_lines.append(f"{i + 1}")
        srt_lines.append(f"{fmt_time(start)} --> {fmt_time(end)}")
        srt_lines.append(entry["text"])
        srt_lines.append("")

    srt_path.write_text("\n".join(srt_lines), encoding="utf-8")
    print(f"  SRT → {srt_path}")


def save_manifest(episode_id: str, voice_lines: list[VoiceLine], timing: dict):
    """Сохраняет manifest.json."""
    paths = episode_paths(episode_id)
    manifest = {
        "episode": episode_id,
        "model": MODEL_ID,
        "total_duration": timing["total_duration"],
        "total_lines": len(voice_lines),
        "characters": list(set(vl.character for vl in voice_lines)),
        "files": [
            {
                "file": entry["file"],
                "shot": entry["shot"],
                "character": entry["character"],
                "text": entry["text"],
            }
            for entry in timing["lines"]
        ],
    }
    manifest_path = paths["manifest"]
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"  manifest.json → {manifest_path}")


# ── CLI ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="AI_SHOW Voice Generator")
    parser.add_argument("episode", help="Episode ID (e.g. S01E01)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Парсит раскадровку, показывает план, не генерирует")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Не перегенерировать существующие файлы")
    parser.add_argument("--character",
                        help="Генерировать только для указанного персонажа")
    args = parser.parse_args()

    print(f"=== Voice Generator: {args.episode} ===\n")

    # Парсинг
    voice_lines, pauses, shots = parse_storyboard(args.episode)
    print(f"  Шотов: {len(shots)}")
    print(f"  Реплик: {len(voice_lines)}")
    print(f"  Пауз: {len(pauses)}")

    if not voice_lines:
        print("\n  ОШИБКА: реплики не найдены. Проверь формат раскадровки.")
        sys.exit(1)

    print(f"\n  Реплики:")
    for vl in voice_lines:
        marker = "🎤" if vl.source == "real_recording" else "🤖"
        tg = " [TG]" if vl.effect == "telegram" else ""
        print(f"    {marker} [{vl.index}] Шот {vl.shot} | {vl.character} ({vl.voice_type}{tg})")
        print(f"       \"{vl.text[:80]}{'...' if len(vl.text) > 80 else ''}\"")

    if pauses:
        print(f"\n  Паузы:")
        for p in pauses:
            print(f"    После реплики {p.after_index}: {p.duration}с")

    print(f"\n  Шоты:")
    for s in shots:
        print(f"    Шот {s.number} [{s.type}] {s.name} ({s.time})")

    if args.dry_run:
        # Строим timing с оценочными длительностями из раскадровки
        timing = build_timing(args.episode, voice_lines, pauses, shots)
        print(f"\n  Оценочная длительность: {timing['total_duration']}с")
        print(f"\n  === DRY RUN — генерация не выполнялась ===")
        return

    # Генерация
    print(f"\n  Генерация голосов...")
    generate_voices(
        args.episode, voice_lines,
        skip_existing=args.skip_existing,
        character_filter=args.character,
    )

    # Timing + SRT + Manifest
    print(f"\n  Построение timing...")
    timing = build_timing(args.episode, voice_lines, pauses, shots)
    save_timing(args.episode, timing)
    save_srt(args.episode, timing)
    save_manifest(args.episode, voice_lines, timing)

    print(f"\n=== Готово: {timing['total_duration']}с, {len(voice_lines)} реплик ===")


if __name__ == "__main__":
    main()
