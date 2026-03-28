# ElevenLabs Voice Guide — AI Office Series

> Практическое руководство по озвучке мультсериала с 3-5 голосами на серию.
> SDK: elevenlabs v2.40.0 (установлен в .venv)

---

## 1. Параметры Voice Settings — что крутить

Все параметры принимают float 0.0-1.0 (кроме speed: 0.7-1.3).

### stability (стабильность)
**Что делает:** Контролирует случайность между генерациями. Низкие значения = широкий эмоциональный диапазон, но результат менее предсказуем. Высокие = монотонно, но стабильно.

| Значение | Эффект | Для кого |
|----------|--------|----------|
| 0.25-0.40 | Очень эмоционально, может "плыть" | Байрон (фантазёр), Алекс (энтузиаст) |
| 0.45-0.55 | Живой, с вариациями | Клодище, Фрида, Стелла |
| 0.60-0.75 | Стабильный, уверенный | Юрий, Today, Уоррен |
| 0.80-1.00 | Монотонный, роботизированный | Не использовать |

### similarity_boost (сходство с оригиналом)
**Что делает:** Насколько точно повторять характеристики исходного голоса. Высокие значения — ближе к оригиналу, но могут воспроизводить артефакты из плохих сэмплов.

| Значение | Эффект | Когда |
|----------|--------|-------|
| 0.50-0.65 | Свободная интерпретация | Библиотечные голоса (можно варьировать) |
| 0.70-0.80 | Баланс | Рекомендуемый диапазон для большинства |
| 0.85-1.00 | Максимальное сходство | Клон голоса Юрия (чтобы звучал как он) |

### style (стиль)
**Что делает:** Усиливает стилевые особенности голоса. Потребляет больше ресурсов, увеличивает задержку. При 0 — отключён.

| Значение | Эффект | Когда |
|----------|--------|-------|
| 0.00 | Нейтральный | По умолчанию, быстрее |
| 0.03-0.05 | Чуть живее | Рекомендуемый минимум для озвучки |
| 0.10-0.25 | Заметно стилизованный | Персонажи с ярким характером |
| 0.30+ | Утрированно | Комедийные моменты, осторожно |

### speed (скорость)
**Что делает:** Ускорение/замедление речи. 1.0 = нормальная скорость.

| Значение | Эффект | Для кого |
|----------|--------|----------|
| 0.85-0.90 | Спокойный, размеренный | Юрий (задумчивые моменты), Today |
| 0.95-1.00 | Нормальный | Клодище, Уоррен, Шерлок |
| 1.05-1.10 | Бодрый | Алекс (возбуждённый), Нео |
| 1.15-1.20 | Тараторит | Алекс в момент "Босс, OpenAI выкатили!" |

### use_speaker_boost
**Что делает:** Усиливает сходство с оригинальным спикером. Увеличивает задержку.
**Рекомендация:** `True` для клона Юрия, `False` для библиотечных голосов.

---

## 2. Рекомендуемые профили голосов по архетипам

### Юрий — Босс (клон голоса)
```python
YURI_SETTINGS = VoiceSettings(
    stability=0.65,
    similarity_boost=0.90,
    style=0.05,
    speed=0.92,
    use_speaker_boost=True
)
```
Уверенный, спокойный, с лёгкой иронией. Не торопится. Голос — клон реального Юрия.

### Клодище — Зам (библиотечный голос)
```python
CLAUDE_SETTINGS = VoiceSettings(
    stability=0.50,
    similarity_boost=0.75,
    style=0.10,
    speed=0.97,
    use_speaker_boost=False
)
```
Интеллигентный, чуть занудный. Мужской, средний регистр. Из Voice Library — искать с тегами: "intellectual", "calm", "narrator".

### Today — Утренний брифинг (библиотечный голос)
```python
TODAY_SETTINGS = VoiceSettings(
    stability=0.65,
    similarity_boost=0.75,
    style=0.05,
    speed=0.90,
    use_speaker_boost=False
)
```
Спокойная, чуть ироничная. Женский, средний регистр. Теги: "professional", "calm", "female".

### Алекс — Скаут AI (библиотечный голос)
```python
ALEX_SETTINGS = VoiceSettings(
    stability=0.35,
    similarity_boost=0.70,
    style=0.15,
    speed=1.08,
    use_speaker_boost=False
)
```
Энергичный молодой гик. Мужской, высокий регистр. Теги: "young", "energetic", "excited".

### Шерлок — QA (библиотечный голос)
```python
SHERLOCK_SETTINGS = VoiceSettings(
    stability=0.70,
    similarity_boost=0.75,
    style=0.08,
    speed=0.95,
    use_speaker_boost=False
)
```
Строгий, педантичный. Мужской, низкий регистр. Теги: "serious", "authoritative", "gruff".

---

## 3. Русский язык на ElevenLabs

### Поддержка
- Модель: **eleven_multilingual_v2** — полная поддержка русского
- Модель: **eleven_v3** (alpha, март 2026) — поддерживает 70+ языков, русский в списке
- Для русского ОБЯЗАТЕЛЬНО указывать `language_code="ru"`
- Модели English-only (eleven_monolingual_v1, eleven_turbo_v2) русский НЕ поддерживают

### Известные проблемы
- **Ударения:** Иногда неправильно ставит ударения в омографах (за́мок/замо́к). Решение: использовать Pronunciation Dictionary
- **Числа:** Могут озвучиваться на английском если не включен text normalization. Решение: `apply_text_normalization="on"`
- **Латиница в тексте:** AI-термины (API, GitHub, OpenAI) произносятся по-английски — это нормально и даже нужно
- **Скорость латентности:** Multilingual v2 медленнее monolingual моделей — это нормально для офлайн-генерации

### Рекомендации для русского текста
```python
# Всегда указывать:
model_id = "eleven_multilingual_v2"  # или eleven_v3 когда станет доступен
language_code = "ru"
apply_text_normalization = "on"
```

---

## 4. Клон голоса Юрия — пошаговый процесс

### Вариант А: Instant Voice Cloning (быстрый старт)
**Требования к аудио:**
- 1-2 минуты чистого голоса (НЕ больше 3 минут — качество падает)
- Без фоновых шумов, музыки, эха
- Один голос, без пауз длиннее 2 секунд
- Форматы: MP3, WAV, M4A

**Шаги:**
1. Записать 1-2 минуты речи на телефон в тихой комнате (Voice Memos / любой рекордер)
2. Через API или веб-интерфейс ElevenLabs загрузить сэмпл
3. Пройти верификацию — прочитать фразу подтверждения (защита от клонирования чужих голосов)
4. Получить `voice_id` для использования в скриптах

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="YOUR_KEY")

# Создание клона
voice = client.voices.add(
    name="Yuri_Boss",
    files=[open("yuri_sample.mp3", "rb")],
    description="Юрий, 55-60, уверенный голос, русский",
    labels={"language": "ru", "role": "boss", "project": "ai_office"}
)
yuri_voice_id = voice.voice_id
```

### Вариант Б: Professional Voice Cloning (максимальное качество)
**Требования к аудио:**
- Минимум 30 минут, оптимально 2-3 часа
- Чистая запись без шумов, эха, музыки
- Разнообразие: повествование, вопросы, эмоции, паузы
- Формат: WAV 44.1kHz / 48kHz, 16bit+

**Шаги:**
1. Записать 30-180 минут на хороший микрофон (или собрать из подкастов/видео Юрия)
2. Загрузить через веб-интерфейс ElevenLabs → VoiceLab → Professional
3. Пройти верификацию (запись фразы)
4. Подождать 3-6 часов обучения модели
5. Получить `voice_id`

**Что записать:** Идеально — читать вслух тексты из MY_STORIES.md. Родной контент, естественные интонации, правильный стиль.

### Рекомендация для проекта
Начать с Instant Clone (1-2 мин записи) → протестировать на первой серии → если качество устраивает, работать. Если нет — собрать материал для Professional Clone.

---

## 5. Эффект "Telegram-сообщение" (bandpass + compression)

Когда Юрий отправляет войс-сообщение агентам — звук должен быть "как из телеги": узкая полоса частот, лёгкое сжатие, чуть хуже качество.

### FFmpeg-команда
```bash
ffmpeg -i yuri_clean.mp3 -af \
  "highpass=f=300,\
   lowpass=f=3400,\
   acompressor=threshold=0.05:ratio=4:attack=5:release=50:makeup=3,\
   equalizer=f=1000:t=q:w=0.5:g=3,\
   volume=0.9" \
  yuri_telegram.mp3
```

### Разбор фильтров:
| Фильтр | Что делает | Зачем |
|--------|-----------|-------|
| `highpass=f=300` | Обрезает всё ниже 300 Гц | Убирает бас — телефонный звук |
| `lowpass=f=3400` | Обрезает всё выше 3400 Гц | Убирает верха — "узкий" звук |
| `acompressor` | Сжимает динамический диапазон | Голосовое сообщение всегда "плоское" |
| `equalizer=f=1000:g=3` | Подъём средних частот | Характерный "голосовой" тон |
| `volume=0.9` | Чуть тише | Реалистичность |

### Python-интеграция (для assemble.py)
```python
import subprocess

def apply_telegram_effect(input_path, output_path):
    """Применяет эффект Telegram voice message к аудиофайлу."""
    cmd = [
        "ffmpeg", "-y", "-i", input_path, "-af",
        "highpass=f=300,"
        "lowpass=f=3400,"
        "acompressor=threshold=0.05:ratio=4:attack=5:release=50:makeup=3,"
        "equalizer=f=1000:t=q:w=0.5:g=3,"
        "volume=0.9",
        output_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)
```

---

## 6. Batch-воркфлоу: от скрипта до готового аудио

### Архитектура пайплайна

```
Раскадровка (S01E01_ru.md)
    ↓ парсинг
Реплики [{персонаж, текст, кадр}, ...]
    ↓ маппинг голосов
Генерация [{voice_id, text, settings, output_file}, ...]
    ↓ ElevenLabs API
Аудиофайлы (assets/voice/S01E01/01_yuri.mp3, 02_claude.mp3, ...)
    ↓ пост-обработка (telegram-эффект для Юрия через ноут)
    ↓ склейка в порядке кадров
assets/voice/S01E01/full.mp3  →  assemble.py
```

### Формат реплик в раскадровке (для парсера)

```markdown
## КАДР 3 — КОНФЛИКТ [0:13-0:25]
ВИЗУАЛ: Клодище за столом, Алекс вбегает
ГОЛОС:
  АЛЕКС: "Босс, OpenAI выкатили новую модель! Это game-changer!"
  КЛОДИЩЕ: "Коллега преувеличивает. Как обычно."
  ЮРИЙ [telegram]: "А вы её тестировали?"
```

### Скрипт генерации голоса

```python
#!/usr/bin/env python3
"""
AI_SHOW — Voice Generator
Генерирует озвучку серии из раскадровки.

Использование:
  python3 scripts/generate_voice.py S01E01
"""

import os
import re
import json
from pathlib import Path
from elevenlabs import ElevenLabs, VoiceSettings, DialogueInput

# ── Config ──────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
API_KEY = os.getenv("ELEVENLABS_API_KEY")
MODEL_ID = "eleven_multilingual_v2"
OUTPUT_FORMAT = "mp3_44100_128"

# ── Маппинг персонажей на голоса ────────────────────────────────
# voice_id нужно подставить реальные после выбора голосов
VOICE_MAP = {
    "ЮРИЙ": {
        "voice_id": "YOUR_YURI_CLONE_ID",
        "settings": VoiceSettings(
            stability=0.65, similarity_boost=0.90,
            style=0.05, speed=0.92, use_speaker_boost=True
        ),
        "telegram_effect": False  # True если [telegram] в тексте
    },
    "КЛОДИЩЕ": {
        "voice_id": "LIBRARY_VOICE_ID",
        "settings": VoiceSettings(
            stability=0.50, similarity_boost=0.75,
            style=0.10, speed=0.97
        )
    },
    "TODAY": {
        "voice_id": "LIBRARY_VOICE_ID",
        "settings": VoiceSettings(
            stability=0.65, similarity_boost=0.75,
            style=0.05, speed=0.90
        )
    },
    "АЛЕКС": {
        "voice_id": "LIBRARY_VOICE_ID",
        "settings": VoiceSettings(
            stability=0.35, similarity_boost=0.70,
            style=0.15, speed=1.08
        )
    },
    "ШЕРЛОК": {
        "voice_id": "LIBRARY_VOICE_ID",
        "settings": VoiceSettings(
            stability=0.70, similarity_boost=0.75,
            style=0.08, speed=0.95
        )
    },
    "УОРРЕН": {
        "voice_id": "LIBRARY_VOICE_ID",
        "settings": VoiceSettings(
            stability=0.60, similarity_boost=0.75,
            style=0.05, speed=0.95
        )
    },
    "БАЙРОН": {
        "voice_id": "LIBRARY_VOICE_ID",
        "settings": VoiceSettings(
            stability=0.30, similarity_boost=0.70,
            style=0.20, speed=1.00
        )
    },
}


def parse_script(episode_id: str) -> list[dict]:
    """Парсит раскадровку и извлекает реплики."""
    script_path = PROJECT_ROOT / "scripts" / f"{episode_id}_ru.md"
    if not script_path.exists():
        raise FileNotFoundError(f"Раскадровка не найдена: {script_path}")

    text = script_path.read_text(encoding="utf-8")
    lines = []

    # Паттерн: "  ПЕРСОНАЖ: "текст""  или  "  ПЕРСОНАЖ [telegram]: "текст""
    pattern = r'^\s+(\w+)(?:\s*\[(\w+)\])?\s*:\s*["\u201c](.+?)["\u201d]\s*$'

    shot_num = 0
    for line in text.split("\n"):
        # Детектим кадр
        shot_match = re.match(r'^## КАДР (\d+)', line)
        if shot_match:
            shot_num = int(shot_match.group(1))
            continue

        match = re.match(pattern, line)
        if match:
            character = match.group(1).upper()
            effect = match.group(2)  # "telegram" или None
            dialogue = match.group(3)
            lines.append({
                "shot": shot_num,
                "character": character,
                "text": dialogue,
                "effect": effect,
            })

    return lines


def generate_voices(episode_id: str, lines: list[dict]):
    """Генерирует аудиофайлы для каждой реплики."""
    client = ElevenLabs(api_key=API_KEY)
    output_dir = PROJECT_ROOT / "assets" / "voice" / episode_id
    output_dir.mkdir(parents=True, exist_ok=True)

    previous_request_ids = []

    for i, line in enumerate(lines):
        character = line["character"]
        if character not in VOICE_MAP:
            print(f"  [!] Персонаж {character} не в VOICE_MAP, пропускаю")
            continue

        voice_cfg = VOICE_MAP[character]
        filename = f"{i+1:02d}_{character.lower()}.mp3"
        output_path = output_dir / filename

        print(f"  [{i+1}/{len(lines)}] {character}: {line['text'][:50]}...")

        # Генерация через TTS API
        audio_iter = client.text_to_speech.convert(
            voice_id=voice_cfg["voice_id"],
            text=line["text"],
            model_id=MODEL_ID,
            language_code="ru",
            output_format=OUTPUT_FORMAT,
            voice_settings=voice_cfg["settings"],
            apply_text_normalization="on",
            # request stitching: передаём до 3 предыдущих request_id
            previous_request_ids=previous_request_ids[-3:] if previous_request_ids else None,
        )

        # Сохраняем аудио
        audio_bytes = b"".join(audio_iter)
        output_path.write_bytes(audio_bytes)

        # Применяем эффект Telegram если нужно
        if line.get("effect") == "telegram":
            telegram_path = output_dir / f"{i+1:02d}_{character.lower()}_tg.mp3"
            apply_telegram_effect(str(output_path), str(telegram_path))
            output_path.unlink()
            telegram_path.rename(output_path)
            print(f"    → telegram effect applied")

        print(f"    → {output_path.name} ({len(audio_bytes)} bytes)")

    # Сохраняем маппинг для assemble.py
    manifest = {
        "episode": episode_id,
        "model": MODEL_ID,
        "files": [
            {
                "file": f"{i+1:02d}_{l['character'].lower()}.mp3",
                "shot": l["shot"],
                "character": l["character"],
                "text": l["text"]
            }
            for i, l in enumerate(lines) if l["character"] in VOICE_MAP
        ]
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"\n  Manifest: {manifest_path}")


def apply_telegram_effect(input_path: str, output_path: str):
    """Применяет эффект Telegram voice message."""
    import subprocess
    cmd = [
        "ffmpeg", "-y", "-i", input_path, "-af",
        "highpass=f=300,"
        "lowpass=f=3400,"
        "acompressor=threshold=0.05:ratio=4:attack=5:release=50:makeup=3,"
        "equalizer=f=1000:t=q:w=0.5:g=3,"
        "volume=0.9",
        output_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)


# ── Альтернативный путь: Text-to-Dialogue API ──────────────────
def generate_dialogue(episode_id: str, lines: list[dict]):
    """
    Альтернатива: одним запросом через Text-to-Dialogue API.
    Плюсы: естественные паузы между репликами, до 10 голосов.
    Минусы: нет per-voice settings, один файл на выходе.
    """
    client = ElevenLabs(api_key=API_KEY)
    output_dir = PROJECT_ROOT / "assets" / "voice" / episode_id
    output_dir.mkdir(parents=True, exist_ok=True)

    inputs = []
    for line in lines:
        character = line["character"]
        if character not in VOICE_MAP:
            continue
        inputs.append(DialogueInput(
            text=line["text"],
            voice_id=VOICE_MAP[character]["voice_id"]
        ))

    audio_iter = client.text_to_dialogue.convert(
        inputs=inputs,
        model_id=MODEL_ID,
        language_code="ru",
    )

    output_path = output_dir / "full_dialogue.mp3"
    audio_bytes = b"".join(audio_iter)
    output_path.write_bytes(audio_bytes)
    print(f"  Dialogue: {output_path} ({len(audio_bytes)} bytes)")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/generate_voice.py S01E01")
        sys.exit(1)

    episode_id = sys.argv[1]
    print(f"=== Generating voices for {episode_id} ===\n")

    lines = parse_script(episode_id)
    print(f"  Found {len(lines)} dialogue lines\n")

    generate_voices(episode_id, lines)
    print(f"\n=== Done ===")
```

---

## 7. Стоимость и планирование бюджета

### Объём текста на серию
- Серия 60-90 сек → ~150-250 слов озвучки → ~800-1500 символов
- С учётом дублей и итераций: x2-3 → **~2500-4500 символов на серию**

### Расчёт по планам (2026)

| План | Символов/мес | Серий/мес | Цена | На символ |
|------|-------------|-----------|------|-----------|
| Free | 10,000 | 2-3 | $0 | — |
| Starter | 30,000 | 6-12 | $5/мес | $0.17/1K |
| Creator | 100,000 | 22-40 | $11/мес | $0.11/1K |
| Pro | 500,000 | 100+ | $83/мес | $0.17/1K |

### Рекомендация
**Starter ($5/мес)** на старте — хватит на 1-2 серии в неделю с запасом на тесты. Если выходить на 3+ серии/неделю — перейти на Creator ($11/мес).

**Для IVC (Instant Voice Clone):** доступно с Starter и выше.
**Для PVC (Professional Voice Clone):** требуется Creator и выше.

### Что считается в символах
- 1 символ текста = 1 credit (eleven_multilingual_v2)
- Пробелы и пунктуация тоже считаются
- Повторная генерация того же текста — снова списываются символы

---

## 8. Модели ElevenLabs — какую выбрать

| Модель | Качество | Скорость | Русский | Цена (credits) | Для чего |
|--------|----------|----------|---------|----------------|----------|
| eleven_multilingual_v2 | Высокое | Средняя | Да | 1x | **Основная для продакшна** |
| eleven_turbo_v2_5 | Хорошее | Быстрая | Да | 0.5x | Тесты, быстрые итерации |
| eleven_v3 (alpha) | Наивысшее | Средняя | Да | 1x | Когда станет public |

### eleven_v3 — что нового
- **Audio Tags:** `[excited]`, `[whispers]`, `[sighs]`, `[laughs]` — управление эмоциями inline
- **Text-to-Dialogue:** нативная поддержка многоголосых диалогов
- **Нет SSML** — вместо break тегов использовать `...` (многоточие) для пауз
- **Нет request stitching** — не поддерживает previous_request_ids
- API в alpha, для раннего доступа нужно связаться с ElevenLabs

### Пример с Audio Tags (v3)
```
[nervous] Босс, там OpenAI выкатили... [excited] Это game-changer!
[sighs] Коллега преувеличивает. Как обычно.
[calm, slightly annoyed] А вы её тестировали?
```

---

## 9. Выбор голосов из Voice Library

### Где искать
- Веб: https://elevenlabs.io/voice-library
- Категории: "Characters & Animation", "Cartoon", "Narration"
- Фильтры: язык (Russian / Multilingual), пол, возраст, стиль

### Стратегия выбора для сериала

1. **Юрий** — ТОЛЬКО клон реального голоса. Не библиотека.

2. **Клодище** — искать: мужской, 30-40 лет, интеллигентный, чуть сухой. Ключевые слова: "intellectual", "narrator", "calm male". Тестировать на фразе: "Технически говоря, это не совсем так."

3. **Today** — искать: женский, 25-35, собранный, чуть ироничный. Ключевые слова: "professional female", "news anchor", "composed". Тестировать на: "Доброе утро. Кофе остыл."

4. **Алекс** — искать: мужской, 20-25, энергичный, высокий. Ключевые слова: "young male", "energetic", "excited". Тестировать на: "Босс, это game-changer! Ну... возможно."

5. **Шерлок** — искать: мужской, 45-55, строгий, низкий. Ключевые слова: "authoritative", "grumpy", "serious". Тестировать на: "Не пойдёт. Тут три ошибки."

### Процесс
1. Отобрать 3-5 кандидатов на каждого персонажа
2. Сгенерировать тестовую фразу-маркер с рекомендованными settings
3. Послушать, выбрать лучший
4. Записать voice_id в VOICE_MAP
5. Проверить на полной сцене (диалог 2-3 персонажей) — голоса не должны путаться

---

## 10. Практические советы

### Качество генерации
- **Не генерируй одну фразу** — ElevenLabs лучше работает с контекстом. Минимум 2-3 предложения
- **Добавляй previous_text/next_text** для одиночных реплик — модель учтёт контекст
- **Seed** для воспроизводимости: укажи конкретный seed (int 0-4294967295) если нужен тот же результат
- **Пунктуация влияет на интонацию:** "Ну конечно." vs "Ну конечно!" vs "Ну конечно..."

### Организация файлов
```
assets/voice/S01E01/
├── 01_yuri.mp3         ← реплика 1
├── 02_claude.mp3       ← реплика 2
├── 03_alex.mp3         ← реплика 3
├── 04_yuri.mp3         ← реплика 4 (telegram-эффект уже применён)
├── manifest.json       ← маппинг реплик → файлов
└── full.mp3            ← склейка (для assemble.py)
```

### Два пути генерации

**Путь A: По одной реплике (рекомендуемый)**
- Полный контроль settings на реплику
- Request stitching для continuity
- Можно переделать одну реплику без пересоздания всего
- Telegram-эффект на отдельные реплики

**Путь B: Text-to-Dialogue API (для тестов)**
- Один запрос — весь диалог
- Естественные паузы между репликами
- До 10 голосов
- Нет per-voice settings (только глобальные)
- Один файл на выходе — сложнее синхронизировать с кадрами

### Pronunciation Dictionary (для русского)
Если модель неправильно произносит слова — создать словарь:
```python
# Пример: правильное ударение
dictionary = client.pronunciation_dictionaries.add_from_file(
    file=open("pronunciation.pls", "rb"),
    name="ai_office_ru"
)
```

Формат PLS (Pronunciation Lexicon Specification):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<lexicon version="1.0" xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"
         alphabet="ipa" xml:lang="ru">
  <lexeme>
    <grapheme>замок</grapheme>
    <phoneme>zɐˈmok</phoneme>
  </lexeme>
</lexicon>
```

---

*Создано: 28 марта 2026*
*Источники: ElevenLabs SDK v2.40.0, ElevenLabs docs, web research*
