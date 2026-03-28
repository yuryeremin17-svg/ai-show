#!/usr/bin/env python3
"""
AI_SHOW — Shared Configuration
Общие константы, голосовые профили, хелперы для всех скриптов пайплайна.
"""

import json
import subprocess
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
ASSETS_DIR = PROJECT_ROOT / "assets"
EPISODES_DIR = PROJECT_ROOT / "episodes"

# ── Video ────────────────────────────────────────────────────────
W, H = 1080, 1920  # 9:16 vertical
FPS = 30

# ── Fonts (macOS) ────────────────────────────────────────────────
FONT_TITLE = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_SUB = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"

# ── ElevenLabs ───────────────────────────────────────────────────
MODEL_ID = "eleven_multilingual_v2"
OUTPUT_FORMAT = "mp3_44100_128"

# ── Voice Profiles (источник: VOICE_DIRECTION_GUIDE.md секция 2.2) ──
# voice_id: None = не настроен, нужно выбрать из библиотеки
VOICE_PROFILES = {
    "ЮРИЙ": {
        "voice_id": "IIKFPiMReo9YmycfbMxL",  # my Dubai Agent Voice (cloned)
        "stability": 0.60, "similarity_boost": 0.85,
        "style": 0.20, "speed": 0.95,
        "speaker_boost": True,
    },
    "ЮРИЙ_TG": {
        "voice_id": "IIKFPiMReo9YmycfbMxL",  # тот же клон что ЮРИЙ
        "stability": 0.55, "similarity_boost": 0.80,
        "style": 0.15, "speed": 1.05,
        "speaker_boost": True,
    },
    "КЛОДИЩЕ": {
        "voice_id": "cjVigY5qzO86Huf0OWal",  # Eric - Smooth, Trustworthy
        "stability": 0.50, "similarity_boost": 0.75,
        "style": 0.30, "speed": 0.92,
        "speaker_boost": False,
    },
    "TODAY": {
        "voice_id": None,
        "stability": 0.65, "similarity_boost": 0.75,
        "style": 0.15, "speed": 0.90,
        "speaker_boost": False,
    },
    "АЛЕКС": {
        "voice_id": None,
        "stability": 0.35, "similarity_boost": 0.70,
        "style": 0.45, "speed": 1.12,
        "speaker_boost": False,
    },
    "УОРРЕН": {
        "voice_id": None,
        "stability": 0.60, "similarity_boost": 0.75,
        "style": 0.15, "speed": 0.95,
        "speaker_boost": False,
    },
    "БАЙРОН": {
        "voice_id": None,
        "stability": 0.40, "similarity_boost": 0.70,
        "style": 0.40, "speed": 0.88,
        "speaker_boost": False,
    },
    "ШЕРЛОК": {
        "voice_id": None,
        "stability": 0.65, "similarity_boost": 0.75,
        "style": 0.10, "speed": 1.0,
        "speaker_boost": False,
    },
}

# ── Маппинг родительный → именительный падеж ─────────────────────
GENITIVE_TO_NOM = {
    "ЮРИЯ": "ЮРИЙ",
    "КЛОДИЩА": "КЛОДИЩЕ",
    "КЛОДИЩЕ": "КЛОДИЩЕ",
    "АЛЕКСА": "АЛЕКС",
    "УОРРЕНА": "УОРРЕН",
    "БАЙРОНА": "БАЙРОН",
    "ШЕРЛОКА": "ШЕРЛОК",
    "АЛЬБЕРТА": "АЛЬБЕРТ",
    "ТЕСЛЫ": "ТЕСЛА",
    "ФРИДЫ": "ФРИДА",
    "ЛЮКА": "ЛЮК",
    "АРТУРА": "АРТУР",
    "СТЕЛЛЫ": "СТЕЛЛА",
    "НЕО": "НЕО",
    "TODAY": "TODAY",
}

# ── Audio Levels (источник: VOICE_DIRECTION_GUIDE.md секция 3.4) ──
LEVELS = {
    "voice":        0,     # reference
    "music_under": -18,    # музыка под голосом
    "music_alone":  -9,    # музыка в паузах
    "sfx_accent":   -6,    # Telegram-звонок, swoosh
    "sfx_ambient": -21,    # typing, coffee, room
    "silence":     -60,    # room tone
}

DUCKING = {
    "attack":    0.1,   # сек — как быстро музыка уходит вниз
    "release":   0.3,   # сек — как быстро возвращается
    "threshold": -30,   # dBFS
    "ratio":     -12,   # dB — на сколько музыка уходит
}

TARGET_LUFS = -14
TRUE_PEAK = -1.0  # dBTP

# ── Scene Colors (для animatic.py) ───────────────────────────────
SCENE_COLORS = {
    "real":       (41, 98, 168),     # синий
    "animated":   (214, 137, 42),    # оранжевый
    "transition": (128, 61, 153),    # фиолетовый
}


# ── Helpers ──────────────────────────────────────────────────────

def episode_paths(episode_id: str) -> dict:
    """Стандартные пути для эпизода."""
    return {
        "script":    SCRIPTS_DIR / f"{episode_id}_ru.md",
        "scenes":    ASSETS_DIR / "scenes" / episode_id,
        "voice":     ASSETS_DIR / "voice" / episode_id,
        "music":     ASSETS_DIR / "music",
        "sfx":       ASSETS_DIR / "sfx",
        "output":    EPISODES_DIR / f"{episode_id}.mp4",
        "animatic":  EPISODES_DIR / f"{episode_id}_animatic.mp4",
        "srt":       ASSETS_DIR / "voice" / episode_id / f"{episode_id}.srt",
        "timing":    ASSETS_DIR / "voice" / episode_id / "timing.json",
        "manifest":  ASSETS_DIR / "voice" / episode_id / "manifest.json",
        "mix":       ASSETS_DIR / "voice" / episode_id / "mix.mp3",
    }


def get_audio_duration(filepath: str | Path) -> float:
    """Длительность аудиофайла в секундах через ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", str(filepath)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def normalize_character(name: str) -> str:
    """Приводит имя персонажа к именительному падежу (uppercase)."""
    name = name.upper().strip()
    return GENITIVE_TO_NOM.get(name, name)


def parse_time_range(time_str: str) -> tuple[float, float]:
    """'0:10-0:22' → (10.0, 22.0) или '0:50-1:00' → (50.0, 60.0)"""
    def to_sec(s):
        parts = s.strip().split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        return float(s)
    start, end = time_str.split("-")
    return to_sec(start), to_sec(end)


def load_env():
    """Загружает .env файл из корня проекта."""
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        import os
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())
