# HANDOFF — AI_SHOW

> Последнее обновление: 28 марта 2026, сессия #6

## Статус проекта
Концепция **"Два мира"** принята. Юрий = реальное видео, агенты = мультик Pixar. Миры не пересекаются. Переходы = Seedance-клипы.
Пайплайн: voice-first (голоса → аниматик → картинки → сборка). 9 ролей в PIPELINE.md.
14 персонажей, мастер-образы готовы (14/14 PNG в masters/).
**/scenario v2.7** — 6 подролей с полными инструкциями. 10 справочников в refs/.
S01E01 "Обратитесь к дизайнеру" пересобран (станет E02). Нужен пилот — знакомство с офисом.

---

## ПЛАН НА СЛЕДУЮЩУЮ СЕССИЮ

### ШАГ 1: ✅ ВЫПОЛНЕН (сессия 28 марта)

Все 6 подролей сценариста написаны в `skills/scenario/SKILL.md` (v2.7, 911 строк).
12/12 чекбоксов из предыдущего плана закрыты.

### ШАГ 1б: Написать скрипты пайплайна

Сейчас скрипты — только описания. Нужно написать код:

**`voice_gen.py`** — генерация голосов:
```
Вход:  scripts/S01EXX_ru.md (секции "Текст озвучки")
Выход: assets/voice/S01EXX/yuri_01.mp3, claude_02.mp3, ...
       assets/voice/S01EXX/timing.json (длительность каждого файла)
API:   ElevenLabs (нужен ключ)
Голоса: Юрий = клон, агенты = библиотека ElevenLabs
Фильтры: Telegram-голосовое = ffmpeg bandpass filter
Справочник: refs/ELEVENLABS_VOICE_GUIDE.md (профили, settings, batch workflow)
```

**`animatic.py`** — грубый черновик:
```
Вход:  timing.json + голоса + placeholder-картинки (цветные плашки с текстом)
Выход: episodes/S01EXX_animatic.mp4
Зачем: проверить ритм ДО генерации в Midjourney
```

**`audio_mix.py`** — аудио-микс:
```
Вход:  голоса (mp3) + музыка (bg.mp3) + SFX (telegram.mp3, swoosh.mp3)
Выход: assets/voice/S01EXX/mix.mp3 (один файл, все слои)
Уровни: голос -6dBFS, музыка -18dB под голосом, SFX -12dB, мастер -14 LUFS
Справочник: refs/VOICE_DIRECTION_GUIDE.md (mixing standards)
```

**`assemble.py` v3** — финальная сборка:
```
Вход:  видеоклипы (shot01.mp4, ...) + аудио-микс (mix.mp3)
Выход: episodes/S01EXX.mp4
Новое: поддержка реального видео + мульт в одном потоке
       субтитры из .srt файла
       dissolve переходы
```

### ШАГ 2: Сценарист набрасывает 3-5 идей серий

**Спросить Юрия:** что хочет рассказать? Какие темы?

Предварительные наброски:
- **S01E01** — "Мой офис из роботов" (ПИЛОТ, знакомство с агентами, Юрий представляет команду)
- **S01E02** — "Обратитесь к дизайнеру" (уже готов, перенумеровать)
- **S01E03** — "Подписал не читая" (AI подписывает отчёт без проверки)
- **S01E04-05** — из банка идей SERIES_BIBLE.md (10 тем)

Сценарист должен предложить **ИДЕИ** (логлайн + инсайт), не полные сценарии. Юрий выберет.

### ШАГ 3: API ключ ElevenLabs

Без ключа голоса не генерируются. Юрий: elevenlabs.io → Profile → API Key.

### ШАГ 4: Создать аудио-набор сезона

6 музыкальных файлов (Suno AI):
- theme_jingle.mp3 (3-5 сек, интро)
- outro_melody.mp3 (3-5 сек, финал)
- bed_chill.mp3 (90 сек, lo-fi для рабочих сцен)
- bed_tension.mp3 (90 сек, нарастание)
- insight_sting.mp3 (3 сек, aha-момент)
- comedy_sting.mp3 (2 сек, для гэгов)

10 SFX (Freesound.org / Pixabay):
- swoosh × 2, telegram notification, pop, portal_to_ai, portal_to_real, keyboard, record_scratch, sparkle, sad_trombone

---

## Что сделано (сессия 28 марта)

- **/scenario v2.7** — 6 подролей с полными инструкциями (911 строк):
  1. Сценарист — Story Spine + ABT + таблица хуков + voice-first + факт-чек + образец S01E01
  2. Раскадровщик — 5-beat sheet + 5 правил шотсайзов + шаблон шота (ШОТСАЙЗ, ЗВУК, СУБТИТРЫ, РИТМ, MOOD)
  3. Промпт-инженер — формула MJ (prefix/suffix) + формула Seedance (constraint block) + запрещённые слова
  4. Voice & Audio Director — голосовые паспорта 5 персонажей + аудио-карта + Telegram FFmpeg-команда + уровни микширования
  5. Режиссёр съёмки — чеклист перед съёмкой + карточка шота + правила перформанса + continuity
  6. Арт-директор — священные коровы + палитры двух миров + 5-секундный drift check + правило 3 попыток

- **10 справочников в refs/** (суммарно ~4500 строк):
  - SCREENWRITING_FRAMEWORKS.md — Pixar Story Spine, Dan Harmon, ABT, Micro Drama
  - SCREENWRITING_RESEARCH.md — Kurzgesagt, TED-Ed, Смешарики, Reels, Explainer
  - SHOT_PLANNING_GUIDE.md — типы шотов, ASL данные, beat sheet, 9:16, mixed media
  - ART_DIRECTION.md — Style Bible, палитра, drift detection, anchor system, QA (19 разделов)
  - MIDJOURNEY_PROMPT_GUIDE.md — формула, style lock, --oref, шаблоны, словарь
  - IMG2VID_PROMPT_GUIDE.md — Seedance/Kling/Runway, движения, камера, constraints
  - VOICE_DIRECTION_GUIDE.md — голосовые паспорта, система PACE, mixing, SFX
  - ELEVENLABS_VOICE_GUIDE.md — API settings, профили, batch workflow, клон Юрия
  - FILMING_GUIDE.md — чеклист съёмки, кадрирование 9:16, свет Дубай, перформанс
  - LIVE_ACTION_DIRECTION_GUIDE.md — continuity, переходы, цвет, mixed media

- **Верификация расширена** до ~55 пунктов (было 9)
- **--cref → --oref** (Midjourney V7)
- **MOOD** поле добавлено в шаблон шота

## Решения (28 марта)

- Подход к подролям: Kurzgesagt-гибрид (глубина + ритм Reels + визуальные метафоры + факт-чек)
- Каждая подроль исследована (3 варианта из индустрии → выбран лучший для нашего формата)
- MJ: оставаться на V6.1 для Pixar-стиля (V7 --oref для персонажей)
- Seedance = основной инструмент img2vid, Kling = запасной, Runway = для реал-кадров Юрия
- Музыка: создание ТЗ в сценарии, генерация Suno — отдельный шаг

## Блокеры

| Блокер | Что блокирует | Как решить |
|--------|---------------|------------|
| API ключ ElevenLabs | Голоса → аниматик → всё | Юрий даёт ключ |
| Скрипты не написаны | Автоматизация пайплайна | ШАГ 1б |
| Клипы Юрия не сняты | Реальное видео | По инструкции из refs/FILMING_GUIDE.md |
| Аудио-набор не создан | Музыка и SFX для серий | ШАГ 4 (Suno + Freesound) |
| Anchor-файлы не созданы | Style lock для генерации | При первой генерации кадров |

## Ключевые файлы

- **skills/scenario/SKILL.md** — скилл-сценарист v2.7 (911 строк, 6 подролей)
- SERIES_BIBLE.md — библия сериала (14 персонажей, формат 60 сек, два мира)
- scripts/PIPELINE.md — 9 ролей, voice-first конвейер
- scripts/S01E01_ru.md — раскадровка v2 (60 сек, два мира)
- scripts/S01E01_PRODUCTION.md — продакшн-план
- assets/characters/PROMPTS.md — промпты 14 персонажей
- **refs/** — 10 справочников (см. выше)

## Персонажи (полный состав)

| # | Имя | Роль | Файл |
|---|-----|------|------|
| 1 | Юрий | Босс (реальное фото) | yuri_real.jpg |
| 2 | Клодище | Зам | claude.png |
| 3 | Today | Брифинг | today.png |
| 4 | Алекс | Скаут AI | scout_ai.png |
| 5 | Уоррен | Скаут Biz | scout_biz.png |
| 6 | Нео | Скаут GitHub | scout_github.png |
| 7 | Байрон | Контент | content.png |
| 8 | Шерлок | QA | qa.png |
| 9 | Альберт | Аналитик | analyst.png |
| 10 | Тесла | Конструкторское бюро | design_bureau.png |
| 11 | Фрида | Клод-Дизайн (она) | claude_design.png |
| 12 | Люк | Клод-Видео (он) | claude_video.png |
| 13 | Артур | Клод-Брокер (он) | claude_broker.png |
| 14 | Стелла | Клод-Астролог (она) | claude_astro.png |

## Предыдущие сессии
- **Сессия 6 (28 марта):** /scenario v2.7, 6 подролей готовы, 10 справочников, 6001 строк
- **Сессия 5 (27 марта):** Концепция "Два мира", PIPELINE, /scenario v2.0, S01E01 пересобран
- **Сессия 4 (26 марта):** 14 персонажей с именами, Seedance доступен в ОАЭ
- **Сессия 3 (23 марта):** assemble.py v2, img2vid, Seedance документация
- **Сессия 2 (21 марта):** assemble.py v1, PROMPTS_READY, тест-видео
- **Сессия 1 (4 марта):** структура проекта, SERIES_BIBLE, scenario скилл
