# VOICE_MAP.md — Карта голосов AI Office

> Для Claude в любом проекте, который работает с голосами агентов.
> Единый источник правды: `AI_SHOW/scripts/config.py` → VOICE_PROFILES
> Обновлено: 30 марта 2026

---

## Где что лежит

| Что | Где | Зачем |
|-----|-----|-------|
| **Voice profiles (код)** | `AI_SHOW/scripts/config.py` → VOICE_PROFILES | voice_id + settings для ElevenLabs API |
| **voice_gen.py** | `AI_SHOW/scripts/voice_gen.py` | Скрипт генерации: парсит раскадровку → MP3 + SRT + timing.json |
| **Готовые MP3 S01E02** | `AI_SHOW/assets/voice/S01E02/` | 22 файла, готовы к монтажу |
| **Готовые MP3 S01E01** | `AI_SHOW/assets/voice/S01E01/` | Файлы для первой серии |
| **Тестовые MP3** | `AI_SHOW/assets/voice/test/` | Прослушка голосов, не для продакшена |
| **Голосовые паспорта** | `AI_SHOW/refs/VOICE_DIRECTION_GUIDE.md` | Тембр, темп, placement, эмоции |
| **ElevenLabs гайд** | `AI_SHOW/refs/ELEVENLABS_VOICE_GUIDE.md` | API, клон Юрия, batch workflow |
| **Telegram-фильтр** | `AI_SHOW/skills/scenario/SKILL.md` подроль 4 | FFmpeg-команда для Telegram-эффекта |

---

## Голоса: полная таблица

| Персонаж | Ключ в config.py | voice_id | Голос ElevenLabs | Характер голоса | Утверждён |
|----------|------------------|----------|-----------------|-----------------|-----------|
| Юрий | `ЮРИЙ` | `IIKFPiMReo9YmycfbMxL` | my Dubai Agent (клон) | Тёплый баритон, уверенный | ✅ |
| Юрий (Telegram) | `ЮРИЙ_TG` | `IIKFPiMReo9YmycfbMxL` | тот же + bandpass фильтр | Сжатый, как голосовое | ✅ |
| Клодище | `КЛОДИЩЕ` | `cjVigY5qzO86Huf0OWal` | Eric | Мягкий тенор, интеллигентный | ✅ |
| Тоня (Today) | `TODAY` | `EXAVITQu4vr4xnSDxMaL` | Sarah | Спокойный женский, ироничный | ✅ |
| Алекс | `АЛЕКС` | `3XOBzXhnDY98yeWQ3GdM` | Brayden | Молодой, бодрый, чилл | ✅ Юрий |
| Уоррен | `УОРРЕН` | `iP95p4xoKVk53GoZ742B` | Chris | Обаятельный, приземлённый | ✅ Юрий |
| Байрон | `БАЙРОН` | `bIHbv24MWmeRgasZH58o` | Will | Молодой, расслабленный оптимист | ✅ Юрий |
| Шерлок | `ШЕРЛОК` | `pqHfZKP75CvOlQylNhV4` | Bill | Старый, ворчливый, строгий | ✅ Юрий |
| Альберт | `АЛЬБЕРТ` | `CwhRBWXzGAHq8TQ4Fs17` | Roger | Спокойный, вдумчивый | ✅ Юрий |
| Нео | — | — | — | Нужен подбор | ⬜ |
| Тесла | — | — | — | Нужен подбор | ⬜ |
| Фрида | — | — | — | Нужен подбор (жен.) | ⬜ |
| Люк | — | — | — | Нужен подбор | ⬜ |
| Артур | — | — | — | Нужен подбор | ⬜ |
| Стелла | — | — | — | Нужен подбор (жен.) | ⬜ |

---

## Как использовать в другом проекте

### Вариант 1: Копировать voice_id напрямую

```python
from elevenlabs import ElevenLabs, VoiceSettings

client = ElevenLabs(api_key="...")

audio = client.text_to_speech.convert(
    voice_id="cjVigY5qzO86Huf0OWal",  # Клодище = Eric
    text="Технически говоря, это не моя вина.",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
    voice_settings=VoiceSettings(
        stability=0.50,
        similarity_boost=0.75,
        style=0.30,
        speed=0.92,
    ),
    language_code="ru",
)

with open("клодище.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

### Вариант 2: Импортировать config.py

```python
import sys
sys.path.insert(0, "/Users/apple/Documents/WORK/AI_SHOW/scripts")
from config import VOICE_PROFILES

profile = VOICE_PROFILES["КЛОДИЩЕ"]
# → {"voice_id": "cjVigY5qzO86Huf0OWal", "stability": 0.50, ...}
```

### Вариант 3: Использовать voice_gen.py

```bash
cd /Users/apple/Documents/WORK/AI_SHOW
source .venv/bin/activate
python scripts/voice_gen.py S01E01
```

Скрипт сам: парсит раскадровку → определяет персонажей → берёт профили из config.py → генерирует MP3 + SRT + timing.json.

---

## Telegram-эффект (голосовое сообщение)

```bash
ffmpeg -i input.mp3 -af "highpass=f=300,lowpass=f=3400,acompressor=threshold=-20dB:ratio=6:attack=5:release=50,equalizer=f=1500:width_type=o:width=1.5:g=4" output_telegram.mp3
```

Используется для реплик Юрия, когда он "отправляет голосовое" агентам.

---

## Уровни микширования

```
Голос:   -6 dBFS peak, -16 LUFS
Музыка:  -18 dB под голосом, -10 dB в паузах
SFX:     -12 dB
Мастер:  -14 LUFS integrated, -1 dBFS true peak
```

---

## Важные правила

1. **config.py = единый источник правды.** Не дублировать voice_id в других файлах — импортировать.
2. **model_id всегда `eleven_multilingual_v2`**, language_code всегда `"ru"`.
3. **Юрий = клон.** Остальные = библиотечные голоса ElevenLabs.
4. **Тоня** в коде = `TODAY` (историческое), маппинг `ТОНЯ` → `TODAY` есть в GENITIVE_TO_NOM.
5. **Голоса утверждены Юрием** лично (прослушал 3 варианта каждого). Не менять без его одобрения.
