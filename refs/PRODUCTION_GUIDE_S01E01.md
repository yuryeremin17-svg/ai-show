# PRODUCTION_GUIDE_S01E01 — Гайд для Юрия

> Всё что нужно сделать для запуска первой серии. ~1.5 часа.

---

## Шаг 0 — Настроить ухо (5 мин)

Перед Suno — послушай на YouTube 30 секунд каждого:
1. **Coca-Cola Happiness Factory** — обрати внимание на музыку когда конвейер работает
2. **Pixar "Up" — Married Life** — первые 20 сек. Тепло и лёгкость
3. **The Office (US) — тема** — 5 сек. Узнаваемый джингл

Не копируем — настраиваем ухо.

---

## Шаг 1 — Suno: фирменный трек (30 мин)

Заходи на suno.com → Create. Выключи "Custom lyrics" (нужен инструментал).

### Промпт 1 — Джингл (5-10 сек):
```
short catchy intro jingle, pizzicato strings and xylophone,
playful and warm, Pixar animation style, memorable melodic hook,
bright and optimistic, no vocals, 10 seconds
```

### Промпт 2 — Тема конвейера (30-60 сек):
```
upbeat playful orchestral, pizzicato strings, light percussion,
xylophone melody, whimsical and cheerful, Pixar movie soundtrack,
warm and confident mood, building energy, no vocals, 100 BPM
```

### Промпт 3 — Тема финала (15-30 сек):
```
soft jazz lounge, warm piano chords, subtle brush drums,
relaxed confident mood, gentle acoustic bass, evening atmosphere,
slightly ironic undertone, no vocals, 80 BPM
```

Каждый промпт → 2-3 генерации (4-6 вариантов). Слушай, выбирай по трём вопросам:

1. **"Застряло?"** — Промотай, подожди 5 минут. Мелодия крутится в голове? Это ОНО.
2. **"Наш?"** — Подходит к мультику с агентами? Или про что-то другое?
3. **"Не надоест?"** — Через 10 серий — ещё ок?

**Лицензия:** Suno Free — для черновиков. Когда выберем финальный — подключаем Pro ($8/мес) и перегенерим.

---

## Шаг 2 — Съёмка (15 мин)

### Где снимать:
- Дома или в любом месте с хорошим светом
- Окно СБОКУ (не сзади, не спереди) — мягкий боковой свет
- Фон нейтральный (стена, окно с Дубаем)
- Кондиционер выключить (шум)

### Как снимать:
- Фронтальная камера, вертикально (9:16)
- Крупный план: голова + плечи
- Телефон на уровне глаз (стопка книг / штатив)
- НЕ держать в руке
- 3-4 дубля каждого клипа

### Клип А (шот 1 — утро):
> "Утро. Пачка задач. Новости разобрать, пост написать, отчёт проверить, клиенту ответить... Раньше для этого нужна была команда. Сейчас — я нажимаю Enter."

- Настроение: чуть устало, с иронией
- В конце — жест рукой вниз (нажимаешь Enter за кадром)

### Клип Б (шот 5 — финал):
> "Целая команда. Аналитик, копирайтер, контролёр, зам... и ассистент, которая знает мой график лучше меня. Ну... почти не спорят."
>
> "И вся эта история стоит дешевле, чем ланч на двоих в Дубае."
>
> "И это не офис дешёвый. Это ланчи в Дубае такие."
>
> "Хотя сейчас не сезон — может, за ланч с десертом."

- Кофе в руке
- Настроение: расслабленное, стендап
- Паузы между фразами

---

## Шаг 3 — Midjourney: 5 картинок (30 мин)

Открой Midjourney (веб). Копируй промпты ниже один за одним.

### Картинка 1 — Оверлей экрана (красные бейджи):
```
stylized warm illustration, soft 3D rendering, close-up of laptop screen showing messenger app with stack of unread notifications with red badges, task list visible, warm golden glow from screen, cozy professional atmosphere, matte finish, subtle depth of field --ar 16:9
```

### Картинка 2 — Конвейер (Алекс → Байрон → Шерлок):
```
stylized warm illustration, soft 3D rendering, Pixar-style character design, bright modern office with conveyor belt of glowing task cards, three cartoon characters working in sequence: first a young guy in purple hoodie grabbing cards excitedly, second a creative type in dark red beret writing with glowing pen with crossed-out paragraphs floating around, third a short stocky man in brown vest at the end inspecting documents with magnifying glass and red pencil with scoreboard on wall behind him, warm golden lighting, soft ambient shadows, cozy professional atmosphere, matte finish, subtle depth of field --ar 9:16
```
**Важно:** после генерации добавь `--oref` с мастер-образами scout_ai.png, content.png, qa.png

### Картинка 3 — Клодище и Today у доски:
```
stylized warm illustration, soft 3D rendering, Pixar-style character design, tall thin man in black turtleneck with round glasses standing at whiteboard with colorful flow diagram directing task cards, one card fallen on floor under his shoe unnoticed, elegant woman in muted sage green silk blouse with neat bun and thin glasses standing beside him holding tablet with raised eyebrow looking at the fallen card, warm office with Dubai skyline through window, warm golden lighting, soft ambient shadows, cozy professional atmosphere, matte finish, subtle depth of field --ar 9:16
```
**Важно:** `--oref` с claude.png и today.png

### Картинка 4 — Результат вылетает:
```
stylized warm illustration, soft 3D rendering, Pixar-style character design, end of conveyor belt with stack of finished documents flying out each stamped with green checkmark seal, multiple Telegram notification bubbles appearing on large monitor screen, purple-hoodie character giving thumbs up in background, beret character adjusting beret proudly, brown-vest character already inspecting next batch, warm golden lighting, soft ambient shadows, cozy professional atmosphere, matte finish, subtle depth of field --ar 9:16
```
**Важно:** `--oref` с scout_ai.png, content.png, qa.png

### Картинка 5 — Оверлей экрана (зелёные галочки):
```
stylized warm illustration, soft 3D rendering, close-up of laptop screen showing messenger app with stack of completed notifications with green checkmarks, all tasks done, warm golden glow from screen, cozy professional atmosphere, matte finish, subtle depth of field --ar 16:9
```

---

## Шаг 4 — Скинь мне всё

- Все дубли видео (клип А + клип Б)
- Лучшие треки из Suno (или все — я помогу выбрать)
- Картинки из Midjourney (выбранные варианты)

**Всё остальное делаю я:** озвучка агентов, монтаж, сборка.

---

## Итого

| Шаг | Что | Время |
|-----|-----|-------|
| 0 | Послушать 3 референса на YouTube | 5 мин |
| 1 | Suno — 3 промпта (джингл + конвейер + финал) | 30 мин |
| 2 | Съёмка 2 клипов (по 3-4 дубля) | 15 мин |
| 3 | Midjourney — 5 промптов | 30 мин |
| 4 | Скинуть всё | 5 мин |

**Общее время: ~1.5 часа**

---

*Создано: 28 марта 2026*
