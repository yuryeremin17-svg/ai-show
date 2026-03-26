# HANDOFF — AI_SHOW

> Последнее обновление: 26 марта 2026, сессия #4

## Статус проекта
Пайплайн: Midjourney (картинки агентов) + реальное фото Юрия → Seedance/Dreamina (img2vid, доступен в ОАЭ) → ElevenLabs (голос) → assemble.py (сборка).
14 персонажей с именами, мастер-образы в `assets/characters/masters/` (15 файлов).
Юрий — реальный человек среди мультяшных агентов (визуальный контраст = главная фишка).
S01E01 — раскадровка готова, промпты обновлены для веб-версии Midjourney.
**Блокер:** ждём от Юрия 10 картинок из Midjourney + ElevenLabs API key + музыку из Suno.

## Что сделано (сессия 26 марта)
- **14 персонажей** — имена утверждены, мастер-образы сгенерированы и сохранены
- **Юрий = реальное фото** (yuri_real.jpg), не мультяшный — визуальный контраст с агентами
- **Новые персонажи:** Нео (Скаут GitHub), Тесла (Конструкторское бюро), Фрида (Клод-Дизайн), Люк (Клод-Видео), Артур (Клод-Брокер), Стелла (Клод-Астролог)
- **Клоды-кураторы** — вариации Клодища (водолазка+очки), 2 девушки + 2 парня
- **Seedance 2.0** — доступен в ОАЭ через Dreamina и CapCut (веб)
- **CapCut Video Studio** — Seedance встроен, можно генерить img2vid без отдельного инструмента
- **Аудит всех файлов** — SERIES_BIBLE, CLAUDE.md, PROMPTS.md, PROMPTS_READY, SEEDANCE_GUIDE обновлены

## Решения (26 марта)
- Юрий — реальное фото, агенты — Pixar-мульт (как "Кто подставил кролика Роджера")
- Midjourney для картинок (пока), Dreamina/Seedance для img2vid
- Dreamina также умеет генерить картинки (Seedream) — потенциальная замена Midjourney
- Имена персонажей со "вторым дном": Нео (Matrix), Уоррен (Баффет), Шерлок, Альберт (Эйнштейн), Тесла, Фрида (Кало), Стелла (звезда), Байрон (поэт)

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

## Что дальше

### Срочное (от Юрия)
1. **10 картинок** из Midjourney по промптам из PROMPTS_READY.md → `assets/scenes/S01E01/`
2. **ElevenLabs API key** (elevenlabs.io → Settings → API Keys)
3. **Музыка** из Suno AI → `assets/music/bg.mp3`
4. **Тест img2vid**: загрузить 2-3 картинки в Dreamina → Seedance → оценить качество

### После получения ассетов (Claude делает сам)
5. Подключить ElevenLabs → сгенерировать озвучку → `assets/voice/S01E01/full.mp3`
6. **Первая сборка S01E01** → `python3 scripts/assemble.py S01E01`

### Системное (после пилота)
7. **Клон голоса Юрия** в ElevenLabs (запись 30 сек)
8. **Голоса агентов** (Клодище, Today — разные тембры)
9. **Тест Dreamina/Seedream** — может ли заменить Midjourney для картинок
10. **Скилл /episode** → одна команда = весь цикл

## Ключевые файлы
- SERIES_BIBLE.md — библия сериала (14 персонажей с именами, формат, тон)
- assets/characters/PROMPTS.md — промпты + файлы всех 14 персонажей
- assets/characters/masters/ — 15 мастер-образов (файлы)
- scripts/S01E01_ru.md — раскадровка пилота (10 кадров)
- assets/scenes/S01E01/PROMPTS_READY.md — промпты для Midjourney (веб)
- scripts/assemble.py — сборка видео из ассетов
- refs/SEEDANCE_GUIDE.md — справочник Seedance 2.0
- refs/VIDEO_PIPELINE_RESEARCH_2026.md — исследование инструментов

## Технические заметки
- moviepy 2.2.1 использует imageio_ffmpeg (встроенный ffmpeg)
- Python venv: `python3 -m venv .venv && source .venv/bin/activate && pip install moviepy pillow numpy`
- assemble.py ожидает: `assets/scenes/<episode>/01.png`, `assets/voice/<episode>/full.mp3`, `assets/music/bg.mp3`
- Midjourney веб-версия: midjourney.com → Imagine
- Seedance: dreamina.capcut.com (доступен в ОАЭ, веб)
- Pixar-стиль: `stylized warm illustration` + `Pixar-style character design`

## Предыдущие сессии
- **Сессия 3 (23 марта):** assemble.py v2 (видеоклипы), img2vid промпты, Seedance документация, исследование пайплайнов
- **Сессия 2 (21 марта):** assemble.py v1, PROMPTS_READY, тест-видео YTP
- **Сессия 1 (4 марта):** структура проекта, SERIES_BIBLE, scenario скилл, 8 персонажей
