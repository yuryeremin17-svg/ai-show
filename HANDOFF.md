# HANDOFF — AI_SHOW

> Последнее обновление: 21 марта 2026, сессия #2

## Статус проекта
Пайплайн сборки видео работает: картинки + голос + музыка → MP4 через `scripts/assemble.py`.
Пилотная серия S01E01 "Обратитесь к дизайнеру" — раскадровка готова, промпты для Midjourney подготовлены.
**Блокер:** ждём от Юрия ElevenLabs API key + 10 картинок из Midjourney + музыку из Suno.

## Что сделано (всего)
- Структура проекта: CLAUDE.md, SERIES_BIBLE.md, skills/scenario
- Все 8 персонажей: промпты + мастер-образы (URL в PROMPTS.md)
- Юрий: мастер-образ сгенерирован через фото (--cref), URL обновлён
- S01E01_ru.md: полная раскадровка (10 кадров), CREF-инструкции, детальные промпты
- Подробные описания всех 7 агентов (характер, голос, роль в сериале)

## Что сделано (сессия 21 марта — из AI-Design-Studio)
- **Скрипт сборки:** `scripts/assemble.py` — принимает картинки + голос + музыку, собирает MP4
  - Ken Burns эффекты (zoom in/out, pan left/right)
  - Crossfade переходы между кадрами
  - Субтитры с подсветкой ключевых слов
  - Фоновая музыка с автолупом и снижением громкости под голос
  - Заставка + аутро
- **Тест-видео:** Сгенерировано YTP-видео "AI Office" (25 сек, 1080x1920) — PIL + moviepy + ffmpeg
  - Доказана возможность программной сборки без CapCut
  - Протестированы: глитч-эффекты, scanlines, vignette, shake, zoom, flash-переходы
- **Стек обновлён:** CapCut заменён на Python-сборку, добавлены альтернативные источники картинок
- **Два источника картинок:** Midjourney (ручной) и ChatGPT/DALL-E (API) — взаимозаменяемы

## Решения (21 марта)
- **CapCut больше не нужен** — сборка видео полностью программная (assemble.py)
- **Картинки:** два источника, Midjourney и DALL-E, выбор за Юрием по ситуации
- **ElevenLabs:** ожидает API key для интеграции голосов
- **Музыка:** Suno AI для своих треков, Kevin MacLeod (incompetech.com) как fallback
- **Зависимости:** moviepy, pillow, numpy — venv для изоляции

## Что сделано (сессия 21 марта #2)
- **PROMPTS_READY.md** — 10 готовых промптов для Midjourney с --cref ссылками на мастер-образы
  - Лежит в `assets/scenes/S01E01/PROMPTS_READY.md`
  - Юрий копирует промпт → вставляет в Discord → скачивает → 01.png...10.png
- **Тест-видео перенесено** из AI-Design-Studio → `episodes/ai-office-ytp.mp4`
- **План пошагового запуска** согласован с Юрием

## Что дальше

### Срочное (от Юрия)
1. **ElevenLabs API key** (elevenlabs.io → Settings → API Keys)
2. **10 картинок** из Midjourney по промптам из PROMPTS_READY.md → `assets/scenes/S01E01/`
3. **Музыка** из Suno AI → `assets/music/bg.mp3`

### После получения ассетов (Claude делает сам)
4. Подключить ElevenLabs → сгенерировать озвучку → `assets/voice/S01E01/full.mp3`
5. **Первая сборка S01E01** → `python3 scripts/assemble.py S01E01`

### Системное (после пилота)
6. **OpenAI API key** (platform.openai.com, $5) → автогенерация картинок без Midjourney
7. **Клон голоса Юрия** в ElevenLabs (запись 30 сек)
8. **Голоса агентов** (Клодище, Today — разные тембры)
9. **Скилл /episode** → одна команда = весь цикл

## Технические заметки
- moviepy 2.2.1 использует imageio_ffmpeg (встроенный ffmpeg, brew не нужен)
- Python venv: `python3 -m venv .venv && source .venv/bin/activate && pip install moviepy pillow numpy`
- assemble.py ожидает: `assets/scenes/<episode>/01.png`, `assets/voice/<episode>/full.mp3`, `assets/music/bg.mp3`
- midjourney.com НЕ поддерживает --sref и несколько --cref одновременно
- Discord Midjourney бот: поддерживает несколько --cref, входит в подписку
- "character" в промптах = гендерно-нейтрально, всегда писать "man"/"woman"
- Pixar-стиль обеспечивается словами: stylized warm illustration + Pixar-style

## Ключевые файлы
- scripts/assemble.py — сборка видео из ассетов
- scripts/S01E01_ru.md — раскадровка пилота
- assets/characters/PROMPTS.md — промпты + URL всех 8 персонажей
- SERIES_BIBLE.md — библия сериала (персонажи, формат, тон)
