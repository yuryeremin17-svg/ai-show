# VOICE_DIRECTION_GUIDE.md — Голосовая режиссура для AI Office

> Практическое руководство: как писать голосовые указания, настраивать ElevenLabs,
> различать персонажей голосом, делать саунд-дизайн и сводить звук для 60-секундного
> анимированного видео.
>
> Создано: 28 марта 2026

---

## 1. VOICE DIRECTION SHEET — формат указаний для каждой реплики

### 1.1. Что писать на каждую строку диалога

Каждая реплика в раскадровке должна содержать 7 полей:

```
ПЕРСОНАЖ: [ИМЯ]
ТИП: [на камеру / закадровый / telegram-голосовое / прямая речь / шёпот]
ТЕКСТ: "Точный текст реплики."
ЭМОЦИЯ: [основная эмоция + нюанс]
ТЕМП: [быстро / средне / медленно / с паузами]
АКЦЕНТЫ: [какие слова выделить, где дыхание, где пауза]
ELEVENLABS: [аудио-теги и настройки]
```

### 1.2. Пример заполнения (из S01E01)

```
ПЕРСОНАЖ: КЛОДИЩЕ
ТИП: прямая речь (мультяшная сцена)
ТЕКСТ: "Здесь нужен профессиональный дизайнер. Я могу подсказать направление."
ЭМОЦИЯ: сдержанная уверенность + лёгкое высокомерие
ТЕМП: средний, ровный — как преподаватель объясняет очевидное
АКЦЕНТЫ: "профессиональный" — нажим; пауза 0.3с перед "Я могу";
         "подсказать" — снисходительно
ELEVENLABS: stability=0.55, similarity=0.78, style=0.25, speed=0.95
  Текст для API: "[matter-of-factly] Here you need a professional designer.
  [slight pause] I can suggest a direction."
```

```
ПЕРСОНАЖ: КЛОДИЩЕ
ТИП: прямая речь
ТЕКСТ: "Перестраховался."
ЭМОЦИЯ: виноватая полуулыбка — признаёт косяк, но не убит
ТЕМП: одно слово, слегка растянуто, без спешки
АКЦЕНТЫ: всё слово — одно ударение, лёгкий выдох в конце
ELEVENLABS: stability=0.45, similarity=0.78, style=0.35, speed=0.85
  Текст для API: "[sheepishly, slight smile] Perestrahovalsya. [exhales]"
```

```
ПЕРСОНАЖ: ЮРИЙ
ТИП: telegram-голосовое (+ аудио-фильтр сжатия)
ТЕКСТ: "Хорошо. А как сделать БЕЗ дизайнера? Дай три решения."
ЭМОЦИЯ: спокойная уверенность → нажим на "БЕЗ" → приказ "дай три"
ТЕМП: начало средне → ускорение к концу
АКЦЕНТЫ: "Хорошо" — нейтрально, точка; "БЕЗ" — ударение, выделить;
         "Дай три решения" — без вопроса, это приказ, точка
ELEVENLABS: stability=0.60, similarity=0.85, style=0.20, speed=1.0
  Пост-обработка: полосовой фильтр 300-3400 Hz (Telegram-сжатие),
  лёгкий клиппинг, room reverb OFF
```

### 1.3. Словарь эмоций для voice direction

Вместо размытых "грустно" / "весело" — конкретные описания:

| Вместо | Пиши так |
|--------|----------|
| весело | улыбается, голос поднимается в конце фразы |
| грустно | голос опускается, воздух между словами, без энергии |
| злится | сжатые зубы, давление в груди, слова короче |
| удивлён | брови вверх (звук "о"), пауза перед реакцией, выдох |
| уверен | ровный тон, без колебаний, точки вместо вопросов |
| нервничает | слова быстрее, дыхание чаще, незаконченные фразы |
| ироничен | лёгкое растягивание ключевого слова, полуулыбка в голосе |
| виноват | голос тише, чуть медленнее, лёгкий выдох |
| восхищён | энергия вверх, темп ускоряется, "глаза горят" слышно |

### 1.4. Система обозначений в тексте

```
**жирный**     = ударение, нажим на слово
...            = пауза 0.3-0.5 сек (дыхание)
[пауза 1с]    = длинная пауза (дать зрителю переварить)
(шёпотом)     = сменить громкость
CAPS           = громче, с давлением (не крик)
→              = ускорение темпа
←              = замедление темпа
//             = дыхание/вдох
|              = микро-пауза (0.1с, смена мысли)
```

---

## 2. CHARACTER VOICE BIBLE — голосовые паспорта персонажей

### 2.1. Матрица голосов (ElevenLabs параметры)

| Персонаж | Pitch | Timbre | Speed | Placement | EL Voice Type | EL Model |
|----------|-------|--------|-------|-----------|---------------|----------|
| **Юрий** (закадр) | средне-низкий | тёплый, бархатный, чуть хриплый | 0.95-1.0 | грудь | Voice Clone (свой) | v2 / v3 |
| **Юрий** (telegram) | тот же + фильтр | сжатый, как через телефон | 1.0-1.05 | грудь | Voice Clone + постобработка | v2 / v3 |
| **Клодище** | средний | мягкий, интеллигентный, "очки слышно" | 0.90-0.95 | рот/нос | Library: intellectual male | v3 |
| **Today** | средне-высокий | чистый, ровный, спокойный, слегка прохладный | 0.90 | голова/рот | Library: calm professional female | v3 |
| **Алекс** | высокий | яркий, энергичный, слегка nasal | 1.10-1.15 | нос/рот | Library: young excited male | v3 |
| **Уоррен** | средне-низкий | деловой, ровный, немного сухой | 0.95 | грудь/рот | Library: business male | v3 |
| **Байрон** | средний | мечтательный, "витает", мягкие согласные | 0.90 | голова | Library: dramatic artistic male | v3 |
| **Шерлок** | средне-низкий | резкий, сухой, "карандаш скрипит" | 1.0 | нос | Library: strict older male | v3 |

### 2.2. ElevenLabs Voice Settings по персонажам

```
ЮРИЙ (закадровый рассказчик):
  stability:       0.60  (достаточно стабильный, но живой)
  similarity_boost: 0.85  (максимально похож на оригинал)
  style:           0.20  (немного экспрессии, не монотонно)
  speed:           0.95  (чуть медленнее — вес слов)
  speaker_boost:   true

ЮРИЙ (telegram-голосовое):
  stability:       0.55  (чуть больше вариации — "реальная запись")
  similarity_boost: 0.80
  style:           0.15
  speed:           1.05  (чуть быстрее — разговорный стиль)
  speaker_boost:   true
  POST-FX:         bandpass 300-3400 Hz, -3dB compression,
                   slight noise floor +0.5dB

КЛОДИЩЕ:
  stability:       0.50  (нужна вариация для эмоций)
  similarity_boost: 0.75
  style:           0.30  (выраженный характер)
  speed:           0.92  (думающий, не торопится)
  speaker_boost:   false

TODAY:
  stability:       0.65  (стабильная, ровная)
  similarity_boost: 0.75
  style:           0.15  (минимальный стиль — это её стиль)
  speed:           0.90  (неспешно, уверенно)
  speaker_boost:   false

АЛЕКС (скаут AI):
  stability:       0.35  (высокая вариация — эмоциональный)
  similarity_boost: 0.70
  style:           0.45  (максимальная экспрессия)
  speed:           1.12  (тараторит от возбуждения)
  speaker_boost:   false

УОРРЕН (скаут Biz):
  stability:       0.60  (стабильный, деловой)
  similarity_boost: 0.75
  style:           0.15  (сдержанный)
  speed:           0.95  (размеренный)
  speaker_boost:   false

БАЙРОН (контент):
  stability:       0.40  (творческая вариация)
  similarity_boost: 0.70
  style:           0.40  (драматичный)
  speed:           0.88  (мечтательно-медленный)
  speaker_boost:   false

ШЕРЛОК (QA):
  stability:       0.65  (предсказуемый, сухой)
  similarity_boost: 0.75
  style:           0.10  (минимум стиля — это и есть стиль)
  speed:           1.0   (ровный, без спешки)
  speaker_boost:   false
```

### 2.3. ElevenLabs Voice Design — промпты для создания голосов

Для персонажей, которым нет подходящего голоса в библиотеке, используем Voice Design
(elevenlabs.io → My Voices → Add Voice → Voice Design):

```
КЛОДИЩЕ:
"A male voice in his mid-30s. Intellectual, slightly nasal, soft-spoken
but confident. Think a university professor who also codes. Speaks
Russian with clear diction. Warm but detached, like he's always
thinking three steps ahead. Slight breathiness when admitting mistakes."

TODAY:
"A female voice in her late 20s. Calm, composed, slightly cool.
Professional but not corporate — think a trusted executive assistant
who knows more than she says. Clear articulation, measured pace.
Russian speaker. Never raises her voice, but every word has weight."

АЛЕКС:
"A young male voice, early 20s. Energetic, enthusiastic, slightly nasal.
Talks fast when excited, stumbles over words sometimes. Think a junior
developer who just found an amazing repo. Russian speaker with a modern,
tech-savvy vibe. High energy, infectious enthusiasm."

ШЕРЛОК:
"An older male voice, 50s. Dry, precise, slightly irritated by default.
Think a veteran editor who has seen every mistake possible. Clipped
consonants, measured pace. Russian speaker. Every word is chosen
carefully. Sounds like he's about to say 'not good enough.'"
```

### 2.4. ElevenLabs v3 Audio Tags — справочник по персонажам

Eleven v3 поддерживает аудио-теги в квадратных скобках. Они управляют эмоциями,
паузами, манерой подачи.

**Универсальные теги:**

| Категория | Теги |
|-----------|------|
| Эмоции | [happy], [sad], [angry], [excited], [nervous], [frustrated], [calm], [sorrowful] |
| Подача | [whispers], [shouts], [matter-of-factly], [sarcastically], [deadpan], [playfully] |
| Реакции | [laughs], [sighs], [clears throat], [gasps], [exhales], [gulps] |
| Темп | [pause], [rushed], [drawn out], [hesitates], [stammers] |
| Когнитивные | [thinking], [realizing], [resigned tone], [with conviction] |
| Характер | [sheepishly], [proudly], [dismissively], [warmly], [coldly] |

**Теги по персонажам AI Office:**

```
КЛОДИЩЕ:
  Базовый:     [thoughtfully], [matter-of-factly]
  Когда прав:  [with quiet confidence], [intellectual tone]
  Когда косяк: [sheepishly], [slight embarrassment], [exhales]
  "Перестраховался": [sheepishly, slight smile, resigned]

TODAY:
  Базовый:     [calmly], [measured], [cool professionalism]
  Ирония:      [slight smile], [knowing tone], [understated]
  "Кофе остыл": [neutral, but the subtext is everything]

АЛЕКС:
  Базовый:     [excited], [energetically], [rushed]
  Когда хайп:  [breathlessly excited], [can barely contain himself]
  Когда осадили: [deflated], [mumbling], [trailing off]

УОРРЕН:
  Базовый:     [business-like], [measured], [pragmatically]
  Про Алекса:  [dismissively], [slight condescension]
  Про деньги:  [with conviction], [leaning forward]

БАЙРОН:
  Базовый:     [dreamily], [with artistic flair], [softly]
  Творит:      [inspired], [building momentum], [eyes lighting up]
  Обижен:      [hurt, but trying to hide it], [muttering]

ШЕРЛОК:
  Базовый:     [dryly], [clipped], [unimpressed]
  Нашёл ошибку: [triumphantly dry], [I-told-you-so tone]
  "Не пойдёт": [flatly], [with finality], [pencil tapping]
```

---

## 3. AUDIO MIXING STANDARDS — уровни звука для 60-сек видео

### 3.1. Целевая громкость по платформам

| Платформа | Integrated LUFS | True Peak (dBTP) | Примечание |
|-----------|----------------|-------------------|------------|
| Instagram Reels | -14 LUFS | -1.0 dBTP | Meta нормализует через xHE-AAC |
| YouTube Shorts | -14 LUFS | -1.0 dBTP | YouTube нормализует до -14 |
| TikTok | -14 LUFS | -1.0 dBTP | Нет официального стандарта, -14 безопасно |
| LinkedIn Video | -14 LUFS | -1.0 dBTP | Менее агрессивная нормализация |
| Telegram | нет нормализации | -1.0 dBTP | Звучит как есть — контролируй сам |

**Правило:** Целься в **-14 LUFS integrated**, **-1.0 dBTP** true peak.
Это работает на всех платформах без потери качества.

### 3.2. Относительные уровни элементов микса

```
ЭЛЕМЕНТ              dBFS (peak)    Отн. к голосу   Описание
─────────────────────────────────────────────────────────────
Голос (диалог)       -6 to -3 dBFS  0 (reference)   Всегда на первом плане
Музыка (под голос)   -18 to -24 dBFS  -12 to -18    Фон, не мешает словам
Музыка (без голоса)  -12 to -9 dBFS   -6 to -3      В паузах громче
SFX акцентные        -9 to -6 dBFS   -3 to 0        Telegram-звонок, swoosh
SFX фоновые          -24 to -18 dBFS -18 to -12     Клавиатура, кофе, ambient
Тишина (пауза)       -60 dBFS        —              Не мёртвая тишина — room tone
```

### 3.3. Правила микширования для 60-секундного видео

1. **Голос = царь.** Всё остальное — его свита. Если слово неразборчиво — проблема.
2. **Музыка ducking:** Когда голос говорит — музыка автоматически уходит на -18/-24 dBFS.
   Когда голос молчит — музыка поднимается до -12/-9 dBFS. Transition: 0.3 сек.
3. **SFX ducking:** Акцентные SFX (Telegram-звонок) могут быть громче музыки, но не громче голоса.
   Исключение: звук в паузе между репликами (тогда на уровне голоса).
4. **Пауза после шутки:** 1-1.5 сек тишины (только room tone + тихая музыка).
   Зритель должен успеть засмеяться.
5. **Переходы между мирами:** Swoosh на уровне -9 dBFS, длительность 0.5 сек.
   Музыка меняет тему при переходе (реал → мульт = другая тональность).
6. **True peak limiter:** Обязательно на мастер-шине. Ceiling = -1.0 dBTP.
7. **Проверка на мобильном:** Финальный микс слушать через динамик телефона.
   80% аудитории Instagram/TikTok смотрят без наушников.

### 3.4. Формула для assemble.py / audio_mix.py

```python
# Уровни в dB для ffmpeg/moviepy
LEVELS = {
    "voice":        0,      # reference, без изменений
    "music_under":  -18,    # музыка под голосом
    "music_alone":  -9,     # музыка в паузах
    "sfx_accent":   -6,     # Telegram-звонок, swoosh
    "sfx_ambient":  -21,    # typing, coffee, room
    "silence":      -60,    # room tone
}

DUCKING = {
    "attack":  0.1,   # сек — как быстро музыка уходит вниз
    "release": 0.3,   # сек — как быстро возвращается
    "threshold": -30,  # dBFS — порог срабатывания (когда голос начинается)
    "ratio":   -12,    # dB — на сколько музыка уходит вниз
}

TARGET_LUFS = -14
TRUE_PEAK = -1.0  # dBTP
```

---

## 4. SOUND DESIGN CHECKLIST — для 60-секундного анимированного видео

### 4.1. Слои звука (от нижнего к верхнему)

```
СЛОЙ 5 (верх):  ГОЛОС — диалоги, закадр, Telegram-голосовые
СЛОЙ 4:         SFX АКЦЕНТ — Telegram-звонок, swoosh переходов, удар/клик
СЛОЙ 3:         SFX ФОНОВЫЕ — клавиатура, кофе, шелест бумаг
СЛОЙ 2:         МУЗЫКА — ироничный инструментал
СЛОЙ 1 (низ):   AMBIENCE — гул офиса, далёкий город, кондиционер
```

### 4.2. Чеклист SFX для каждого эпизода

**Обязательные звуки (каждый эпизод):**

- [ ] Telegram notification (стилизованный) — мост между мирами
- [ ] Transition swoosh (реал → мульт) — camera dive
- [ ] Transition swoosh (мульт → реал) — camera exit
- [ ] Room tone (офис агентов) — тихий гул, кондиционер, далёкие клики
- [ ] Room tone (мир Юрия) — реальная комната, тихо

**По ситуации:**

- [ ] Typing / клавиатура — когда печатают сообщение
- [ ] Notification badge — пузырь чата появляется
- [ ] Coffee clink — чашка о стол (если в кадре)
- [ ] Paper shuffle — бумаги (если в кадре)
- [ ] Glasses adjust — Клодище поправляет очки
- [ ] Door — Today появляется в дверях
- [ ] Pencil tap — Шерлок стучит карандашом
- [ ] Gasp / reaction — удивление персонажа
- [ ] Комедийная пауза — тишина + тихий room tone

**Запрещено:**

- Laugh track (закадровый смех)
- Чрезмерные whoosh на каждом движении
- Музыкальные стингеры на каждую шутку (только на главный поворот)
- Звуки из стоковых библиотек без обработки (узнаваемые)

### 4.3. Источники SFX

| Тип | Источник | Формат |
|-----|----------|--------|
| Telegram-звук | [Quick Sounds](https://quicksounds.com) / [DeadSounds](https://deadsounds.com) | WAV/MP3 |
| UI-звуки (клик, swipe) | [Freesound.org](https://freesound.org) — CC0 | WAV |
| Офисные звуки | [Freesound.org](https://freesound.org) — CC0 | WAV |
| Swoosh/transition | [Pixabay Audio](https://pixabay.com/sound-effects/) — royalty-free | MP3 |
| Ambient/room tone | [Freesound.org](https://freesound.org) — CC0 | WAV |
| AI-генерация SFX | [CapCut AI SFX](https://www.capcut.com/tools/ai-sound-effects-generator) | MP3 |
| ElevenLabs v3 | Аудио-теги типа [gunshot], [clapping] — встроенные | MP3 |

### 4.4. Музыка

**Формат:** Один трек на эпизод, 60-70 сек, loop-friendly.

**Стиль для AI Office:**
- Лёгкий, ироничный инструментал
- Электронный + акустические элементы (пиццикато, глокеншпиль)
- Два настроения: A-часть (спокойно, офис) и B-часть (энергия, поворот)
- Тишина / обрыв на комедийные паузы

**Промпт для Suno AI:**
```
Light ironic instrumental, playful pizzicato strings and glockenspiel,
modern electronic beats, office comedy vibe, starts calm then builds
energy at 0:25, drops to silence at 0:42, resolves warmly.
60 seconds, loopable ending. No vocals.
```

---

## 5. VOICE DIRECTION — профессиональная терминология

### 5.1. Размещение голоса (placement)

| Термин | Где резонирует | Звучит как | Персонажи |
|--------|---------------|------------|-----------|
| Chest voice | грудь | глубокий, тёплый, авторитетный | Юрий, Уоррен |
| Head voice | голова | светлый, лёгкий, мечтательный | Байрон, Стелла |
| Nasal | нос | резкий, "гнусавый", характерный | Алекс, Шерлок |
| Mouth/oral | рот | чёткий, нейтральный, деловой | Today, Клодище |
| Throat | горло | хриплый, сдавленный, напряжённый | — (стресс/конфликт) |

### 5.2. Текстура голоса (timbre descriptors)

Описания, которые можно использовать в промптах ElevenLabs Voice Design
и в голосовых указаниях:

| Описание | Значение | Когда использовать |
|----------|----------|-------------------|
| Бархатный (velvet) | мягкий, обволакивающий | Юрий-рассказчик, тёплые моменты |
| Хрустящий (crisp) | чёткие согласные, "щёлкает" | Шерлок, точные реплики |
| Дымчатый (smoky) | хриплый с теплотой | Юрий в откровенные моменты |
| Медовый (honey) | тёплый, густой, приятный | Today, когда смягчается |
| Стальной (steely) | холодный, ровный, без вибрато | Today в рабочем режиме |
| Звонкий (bright/ringing) | высокая энергия, "звенит" | Алекс при открытии |
| Сухой (dry) | минимум обертонов, "факт" | Шерлок, Уоррен |
| Искрящийся (sparkling) | быстрые модуляции, живой | Алекс, Фрида |
| Бумажный (papery) | тихий, шелестящий | Альберт, длинные объяснения |

### 5.3. Дыхание и паузы как инструмент

```
Тип дыхания         Обозначение    Когда
─────────────────────────────────────────────
Вдох перед фразой   //             Начало монолога, смена темы
Выдох после фразы   [exhales]      Признание, сожаление, облегчение
Задержка дыхания    [beat]         Перед поворотом, "а потом..."
Смешок              [slight laugh] Самоирония Юрия
Цоканье             [tsk]          Шерлок недоволен
Хмыканье            [hmm]          Клодище думает
Тяжёлый вздох       [sighs]        Юрий устал от AI
```

### 5.4. Как писать "не просто happy" — система PACE

Каждая эмоция описывается через 4 параметра:

**P** — Placement (откуда звук: грудь/голова/нос)
**A** — Airflow (много/мало воздуха, зажато/свободно)
**C** — Cadence (ритм: ровный/рваный/ускоряющийся/затухающий)
**E** — Energy (уровень энергии: 1-10)

Примеры:

```
"Перестраховался" (Клодище):
  P: рот (нейтральное, без давления)
  A: свободный, лёгкий выдох в конце
  C: одно слово, чуть растянуто, falling intonation
  E: 3/10 (тихая отставка)

"И понеслось! Три варианта. Тут же." (Юрий):
  P: грудь → рот (энергия поднимается)
  A: больше воздуха к концу
  C: три короткие фразы, ускорение, стаккато
  E: 7/10 (восторг от результата)

"Босс, там OpenAI выкатили..!" (Алекс):
  P: нос/рот (высокий, звонкий)
  A: много воздуха, breathless
  C: быстро, без пауз, одним потоком
  E: 9/10 (еле сдерживается)

"Кофе остыл." (Today):
  P: рот (чёткий, ровный)
  A: минимальный, контролированный
  C: два слова, ровная интонация, точка
  E: 2/10 (спокойствие, но подтекст на 8/10)
```

---

## 6. ПОЛНЫЙ ШАБЛОН VOICE DIRECTION SHEET (для раскадровки)

Вставляется в каждый скрипт серии после раскадровки:

```markdown
---

## VOICE DIRECTION SHEET

### Общие параметры эпизода
- Модель: ElevenLabs Eleven v3
- Язык: русский (ru)
- Формат: WAV 44100 Hz 16-bit → MP3 320 kbps (финал)
- Именование: voice_{персонаж}_{шот}_{тейк}.mp3

### Реплики

#### ШОТ [N] — [название]

| # | Персонаж | Текст | Тип | Эмоция (PACE) | EL Settings | Audio Tags |
|---|----------|-------|-----|---------------|-------------|------------|
| 1 | ЮРИЙ | "текст" | закадр | P:грудь A:свободный C:ровный E:5 | stab=0.60 sim=0.85 sty=0.20 spd=0.95 | [warmly] |
| 2 | КЛОДИЩЕ | "текст" | прямая | P:рот A:свободный C:ровный E:4 | stab=0.50 sim=0.75 sty=0.30 spd=0.92 | [matter-of-factly] |

#### Тайминги (после генерации)

| # | Файл | Длительность | Шот | Начало |
|---|------|-------------|-----|--------|
| 1 | voice_yuri_01.mp3 | 4.2s | Шот 2 | 0:10.0 |
| 2 | voice_claude_01.mp3 | 3.8s | Шот 2 | 0:14.2 |

---
```

---

## 7. WORKFLOW — от раскадровки к озвучке

### 7.1. Последовательность (voice-first)

```
1. Сценарист → текст реплик
2. Voice Director → заполняет Voice Direction Sheet
   (эмоция PACE, EL settings, audio tags для каждой реплики)
3. Генерация → ElevenLabs API (voice_gen.py)
   - Для каждой реплики: тейк A, тейк B, тейк C
   - Выбираем лучший
4. Тайминг → измеряем длительность каждого файла
5. Аниматик → placeholder + реальные голоса → проверка ритма
6. [Если ритм не ок] → пересоздаём реплики с другим speed/pace
7. [Если ритм ок] → фиксируем тайминги → промпты для Midjourney/Seedance
```

### 7.2. Пост-обработка аудио

**Telegram-голосовое (фильтр):**
```bash
ffmpeg -i voice_yuri_tg_raw.mp3 \
  -af "highpass=f=300,lowpass=f=3400,acompressor=threshold=-20dB:ratio=4:attack=5:release=50,volume=0.9" \
  voice_yuri_tg.mp3
```

**Room tone (генерация тишины с шумом):**
```bash
ffmpeg -f lavfi -i "anoisesrc=d=60:c=pink:a=0.003" \
  -af "highpass=f=100,lowpass=f=8000" \
  room_tone_office.mp3
```

**Нормализация до -14 LUFS:**
```bash
ffmpeg -i final_mix.mp3 \
  -af "loudnorm=I=-14:TP=-1.0:LRA=11" \
  final_normalized.mp3
```

---

## 8. REFERENCES

### Источники для этого документа

- [Animation Script Template — Voices.com](https://www.voices.com/blog/animation-script-template/)
- [How to Give Best Voice Over Direction — Voices.com](https://www.voices.com/blog/how-to-give-the-best-voice-over-direction/)
- [ElevenLabs TTS Documentation](https://elevenlabs.io/docs/creative-platform/playground/text-to-speech)
- [ElevenLabs Voice Settings](https://elevenlabs-sdk.mintlify.app/speech-synthesis/voice-settings)
- [ElevenLabs v3 Audio Tags](https://elevenlabs.io/blog/v3-audiotags)
- [ElevenLabs v3 Character Direction](https://elevenlabs.io/blog/eleven-v3-character-direction)
- [ElevenLabs v3 Precision Delivery Control](https://elevenlabs.io/blog/eleven-v3-audio-tags-precision-delivery-control-for-ai-speech)
- [ElevenLabs v3 Multi-Character Dialogue](https://elevenlabs.io/blog/eleven-v3-audio-tags-bringing-multi-character-dialogue-to-life)
- [ElevenLabs Voice Design v3](https://elevenlabs.io/blog/voice-design-v3)
- [ElevenLabs Voice Design Documentation](https://elevenlabs.io/docs/eleven-creative/voices/voice-design)
- [ElevenLabs Text to Dialogue API](https://elevenlabs.io/docs/overview/capabilities/text-to-dialogue)
- [Loudness Standards Comparison Table — Youlean](https://youlean.co/loudness-standards-full-comparison-table/)
- [LUFS Standards for 50+ Platforms — Dan Murtagh](https://danmurtagh.com/lufs-loudness-standards/)
- [Target LUFS for YouTube, TikTok, Spotify 2025](https://clickyapps.com/creator/video/guides/lufs-targets-2025)
- [Audio Levels for Short Video — PremiumBeat](https://www.premiumbeat.com/blog/how-to-set-audio-levels-for-video/)
- [Audio Levels for Film — WeVideo](https://www.wevideo.com/blog/how-to-set-audio-levels)
- [Sound Design for Visual Media — Sound On Sound](https://www.soundonsound.com/techniques/sound-design-visual-media)
- [How to Layer SFX — SFX Engine](https://sfxengine.com/blog/how-to-layer-sound-effects-in-video)
- [Vocal Traits for Characters — Voquent](https://www.voquent.com/blog/vocal-characteristics-how-should-your-character-sound/)
- [Voice Character Development — Voice-Reel](https://www.voice-reel.com/voice-acting-character-development/)
- [Voice Acting Glossary — GVAA](https://globalvoiceacademy.com/resources/glossary-of-voice-acting-terms/)
- [ElevenLabs Cheat Sheet — Webfuse](https://www.webfuse.com/elevenlabs-cheat-sheet)

---

*Создано: 28 марта 2026*
*Для проекта AI Office (AI_SHOW)*
