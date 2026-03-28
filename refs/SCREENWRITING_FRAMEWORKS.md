# Фреймворки сценаристики для короткого анимационного контента

> Исследование: март 2026
> Цель: найти лучшие индустриальные подходы к написанию сценариев для 60-90 секундных анимированных серий
> Применение: улучшение скилла /scenario (SKILL.md) для AI Office

---

## 1. ПРОВЕРЕННЫЕ ФРЕЙМВОРКИ НАРРАТИВА

### 1.1 Pixar Story Spine (Kenn Adams → Brian McDonald → Emma Coats)

Формула, которую Pixar использует для каждого фильма. Адаптируется под любой хронометраж.

```
Once upon a time there was _______.     → МИР ЮРИЯ: статус-кво
Every day, _______.                      → Рутина (подразумевается в зацепке)
One day _______.                         → Инцидент / проблема
Because of that, _______.                → МИР АГЕНТОВ: реакция
Because of that, _______.                → Поворот / эскалация
Until finally _______.                   → Кульминация
And ever since then _______.             → МИР ЮРИЯ: инсайт
```

**Адаптация под 60 секунд AI Office:**
- "Once upon a time" + "Every day" = ШОТ 1 (зацепка, 0:00-0:10). Юрий озвучивает ситуацию.
- "One day" = ПЕРЕХОД + ШОТ 2 (0:10-0:20). Что пошло не так.
- "Because of that" x2 = ШОТ 3-4 (0:20-0:45). Агенты реагируют, конфликт, поворот.
- "Until finally" = ШОТ 5 (0:45-0:50). Развязка в мире агентов.
- "Ever since then" = ШОТ 6 (0:50-1:00). Юрий с инсайтом.

**Источники:**
- [Pixar Story Spine — Story Prompt](https://www.storyprompt.com/blog/the-story-spine-also-known-as-pixars-story-structure)
- [Pixar Story Spine: Ultimate Structure 2026 — Automateed](https://www.automateed.com/pixar-story-spine)
- [22 Rules of Storytelling — Industrial Scripts](https://industrialscripts.com/pixar-storytelling-rules/)

---

### 1.2 Dan Harmon Story Circle (8 шагов)

Создан для ТВ-эпизодов (Community, Rick and Morty). Идеально для коротких историй с трансформацией героя.

```
1. YOU      — Герой в зоне комфорта         → Юрий в офисе
2. NEED     — Хочет/нуждается               → Задача (презентация, отчёт...)
3. GO       — Выходит из зоны комфорта       → Даёт задание агентам
4. SEARCH   — Ищет, сталкивается с трудностями → Агенты работают (хаос)
5. FIND     — Находит что искал              → Результат (неожиданный)
6. TAKE     — Платит цену                    → Поворот (подвох, ошибка)
7. RETURN   — Возвращается с опытом          → Юрий осмысляет
8. CHANGE   — Изменился                      → Инсайт
```

**Для 60 секунд:** шаги 1-2 сжимаются в зацепку (5 сек), 3-6 = мир агентов (40 сек), 7-8 = инсайт (10 сек). Круг замыкается — зритель чувствует завершённость.

**Почему это ценно для AI Office:** Каждая серия — микро-трансформация Юрия. Он начинает с одним пониманием AI, заканчивает с другим. Зритель трансформируется вместе с ним.

**Источники:**
- [Dan Harmon Story Circle — Reedsy](https://reedsy.com/blog/guide/story-structure/dan-harmon-story-circle/)
- [Story Circle Explained — Arc Studio](https://www.arcstudiopro.com/blog/dan-harmons-story-circle-screenplay)
- [Storytelling 101 — Boords](https://boords.com/blog/storytelling-101-the-dan-harmon-story-circle)

---

### 1.3 ABT Framework (Randy Olson — "And, But, Therefore")

Самый минималистичный фреймворк. Один абзац = одна история. Изначально создан для науч-попа.

```
[Контекст] AND [ещё контекст],
BUT [проблема/конфликт],
THEREFORE [решение/вывод].
```

**Пример для AI Office:**
> "Мне нужна была презентация для клиента в Дубае, AND Клодище за час сделал 20 слайдов, BUT он туда вставил цифры которых не существует, THEREFORE — если не проверяешь AI, ты не управляешь. Ты доверяешь."

**Применение:** ABT — идеальный тест для сценария. Если не можешь описать серию в одном ABT-предложении — история не сфокусирована, инсайтов больше одного.

---

### 1.4 Micro Drama Structure (индустрия вертикальных сериалов, 2025-2026)

Формат, взорвавший TikTok и ReelShort. Ключевые правила:

```
0-5 сек:   HOOK — конфликт, напряжение, инцидент. Зритель решает остаться.
5-20 сек:  SETUP — герой + проблема. Минимум контекста.
20-50 сек: ESCALATION — 2-3 поворота. Каждые 10 сек — новый бит.
50-60 сек: TWIST + CLIFFHANGER — удар + крючок на следующую серию.
```

**Ключевой принцип:** Нет пространства для сабплотов. Один конфликт, одна эмоция, один поворот. Каждая секунда "без драмы" — потеря зрителя.

**Источники:**
- [How to Write a Micro Drama Script — Writers Imran Thakur](https://writersimranthakur.com/2026/02/27/how-to-write-a-micro-drama-script-that-meets-industry-standards/)
- [Anatomy of a Vertical Drama Script — Medium](https://medium.com/real-reel/the-anatomy-of-a-vertical-drama-script-edcb43d139bb)
- [Micro-Dramas and Vertical-First Storytelling 2026 — Vitrina AI](https://vitrina.ai/blog/micro-dramas-and-vertical-first-storytelling)
- [What Are Verticals and Micro-Dramas — Final Draft](https://www.finaldraft.com/blog/what-are-verticals-and-micro-dramas)

---

## 2. ПРАВИЛА ЗАЦЕПКИ (HOOK) — ПЕРВЫЕ 3-5 СЕКУНД

### Три психологических триггера (OpusClip research):

1. **Pattern Interruption** — сломай ожидание. Не "Привет, сегодня расскажу...", а сразу действие.
2. **Curiosity Gap** — обещай информацию, которой у зрителя нет. "Мой AI-менеджер подписал отчёт. Не читая."
3. **Social Proof** — покажи что другие нашли ценность. "Это уже случилось с 10 000 руководителей."

Лучшие хуки комбинируют минимум 2 из 3 триггеров.

### Типы хуков для edutainment (ранжированы по эффективности):

| Тип | Пример для AI Office | Сила |
|-----|---------------------|------|
| **Bold Statement** | "Мой AI-сотрудник соврал мне в лицо." | Шок + curiosity |
| **Mid-Action** | Юрий смотрит на экран, лицо меняется | Pattern interrupt |
| **Question** | "А вы проверяете что пишет ваш ChatGPT?" | Curiosity + relevance |
| **Contrast** | "Красивый отчёт. С выдуманными цифрами." | Tension |
| **Confession** | "Я доверил AI важную презентацию. Зря." | Vulnerability + curiosity |

### Правило Instagram Reels (2026):
- Первые 3 секунды определяют будут ли смотреть.
- Последние 10 секунд определяют будут ли смотреть СНОВА (алгоритм).
- Субтитры обязательны — 80% смотрят без звука.

**Источники:**
- [Instagram Reels Hook Formulas — OpusClip](https://www.opus.pro/blog/instagram-reels-hook-formulas)
- [TikTok Hook Formulas — OpusClip](https://www.opus.pro/blog/tiktok-hook-formulas)
- [Short-Form Video Hook Scripts — Postoria](https://postoria.io/blog/hook-scripts)
- [Short-Form Storytelling: First 8 Seconds — Trivision](https://trivision.com/uncategorized/short-form-storytelling-reels-tiktok-instagram-youtube/)

---

## 3. ПРАВИЛО "ОДИН ИНСАЙТ НА ЭПИЗОД"

### Индустриальный консенсус:
- **Social Media Examiner:** "One message per video. Don't overload the viewer."
- **Levitate Media (2026):** "Focus on one clear message using concise content."
- **Kurzgesagt (внутренний процесс):** Каждое видео = один вопрос. Десятки черновиков отсекают всё лишнее.
- **Micro Drama стандарт:** "No space for subplots. Single emotional problem, one confrontation, one revelation."

### Тест "одного инсайта":
1. **ABT-тест:** Опиши серию в одном "AND-BUT-THEREFORE". Если не получается — инсайтов больше одного.
2. **Elevator test:** Объясни серию за 10 секунд другу. Если нужно больше — расфокус.
3. **Remove test:** Убери инсайт. Если история всё ещё работает с другим инсайтом — значит этот не главный.

**Источники:**
- [How to Create Short-Form Video Series — Social Media Examiner](https://www.socialmediaexaminer.com/how-to-create-a-short-form-video-series/)
- [Short Form Video Production Best Practices 2026 — Levitate Media](https://levitatemedia.com/learn/mastering-short-form-video-production-best-practices-and-marketing-tips)

---

## 4. ЮМОР В EDUTAINMENT

### Концепция "EdCom" (Educational Comedy):
Термин по аналогии с SitCom. Юмор НЕ украшение — юмор = механизм запоминания.

### Правила юмора в образовательном контенте:

1. **Юмор привязан к теме.** Шутка ради шутки не работает. Смешно должно быть ПОТОМУ ЧТО зритель узнаёт ситуацию.
2. **Фильтры сложности.** Чем больше "фильтров" в шутке (контекст + ирония + визуальный гэг + timing), тем она вознаграждающе. Но первый фильтр = узнавание ("у меня так же!").
3. **Эмпатия перед юмором.** Зритель сначала должен посочувствовать/узнать себя, потом смеяться. Не наоборот.
4. **Юмор снижает тревогу.** Для аудитории 35-60 лет, которая боится AI — юмор делает тему безопасной.
5. **Не объясняй шутку.** Если нужен восклицательный знак чтобы было смешно — не смешно.

### Типы юмора для AI Office (от сильного к слабому):
| Тип | Пример | Почему работает |
|-----|--------|----------------|
| **Узнавание** | "Клодище: Технически говоря... Юрий: Коротко." | Каждый менеджер это говорил |
| **Абсурд ситуации** | AI-агент обижается на критику | Антропоморфизм AI = смешно + страшно |
| **Самоирония** | "Я доверил роботу. Ну конечно." | Юрий смеётся над собой |
| **Running gag** | "Кофе остыл." (Today) | Нарастает от серии к серии |
| **Visual gag** | Шерлок с красным карандашом, всё исчёркано | Работает без звука |

**Источники:**
- [Making Humorous Educational Videos — Reimagine Education](https://www.reimagine-education.com/making-humorous-educational-videos/)
- [Engaging Students With Humor — APS](https://www.psychologicalscience.org/observer/engaging-students-with-humor)
- [Educational Comedy Video Ideas — VidClue](https://vidclue.com/educational-comedy)

---

## 5. КОНСИСТЕНТНОСТЬ ПЕРСОНАЖЕЙ ЧЕРЕЗ СЕРИИ

### Индустриальный стандарт — Animation Bible:

**Обязательные элементы для каждого персонажа:**
1. **Model Sheet** — turnarounds (вид спереди/сбоку/сзади), expression sheet, color key
2. **Silhouette Test** — персонаж узнаваем только по силуэту
3. **Color Palette** — точные цвета (hex/Pantone), forbidden variations
4. **Voice/Speech Pattern** — фразы-маркеры, словарный запас, длина реплик
5. **Character Rules** — что персонаж НИКОГДА не делает / ВСЕГДА делает

### Для AI-генерации (Midjourney/Seedance):
- **Master Image (--cref)** — один эталонный образ на персонажа
- **Prompt Template** — фиксированная часть промпта (стиль + персонаж) + переменная (сцена)
- **Forbidden Elements** — что НЕЛЬЗЯ менять (цвет одежды, очки, пропорции)
- **Drift Detection** — сравнение каждого нового кадра с мастером

### Для голоса/характера (текст сценария):
- **Vocabulary Bank** — слова которые персонаж использует / НЕ использует
- **Reaction Patterns** — как реагирует на конфликт, похвалу, ошибку
- **Relationship Matrix** — как говорит с каждым другим персонажем (иначе!)

**Уже реализовано в AI Office:**
- SERIES_BIBLE.md содержит фразы-маркеры, характеры, цвета, мастер-образы
- assets/characters/PROMPTS.md содержит промпты для Midjourney

**Чего не хватает (рекомендация):**
- Vocabulary Bank для каждого персонажа (10-15 слов "да", 10-15 слов "нет")
- Reaction Matrix (таблица: персонаж x ситуация → реакция)
- Expression Sheet в промптах (не только нейтральный, но и angry/happy/confused)

**Источники:**
- [What Goes in an Animation Bible — Escape Studios](https://escapestudiosanimation.blogspot.com/2019/07/what-goes-in-animation-bible.html)
- [The Pitch Bible Essentials — AWN](https://www.awn.com/animationworld/pitch-bible-just-essentials)
- [11 Essentials Every Animated Series Bible Needs — Pixune](https://pixune.com/blog/11-essentials-of-animated-series-bibles-2025/)
- [Character Consistency — i.Bible](https://www.i.bible/behind-the-scenes/character-consistency/)

---

## 6. ПРИМЕРЫ ОТ СТУДИЙ И СОЗДАТЕЛЕЙ

### 6.1 Pixar SparkShorts
- Формат: 5-10 минут, но принципы масштабируются
- Правило: **Personal stories first.** Каждый SparkShort основан на личном опыте создателя
- Правило: **Emotion is the entry point.** Начни с эмоции, потом строй историю вокруг
- Релевантно для AI Office: истории Юрия = личный опыт. Это главное конкурентное преимущество

### 6.2 Love, Death + Robots (Netflix)
- Формат: 5-17 минут, anthology
- Правило: **Minimum viable worldbuilding.** "What is the absolute minimum the audience needs to know about the world to understand the central conflict?"
- Правило: **Start from difference.** "How is the world different from ours? Answer upfront."
- Релевантно для AI Office: мир агентов = мир отличный от нашего. Объяснять его нужно за 3 секунды (переход в экран), не за 30.

### 6.3 Kurzgesagt — In a Nutshell
- Формат: 8-15 минут edutainment
- **Script process:** 12+ черновиков на видео. Сначала research, потом draft, потом cut-cut-cut.
- **Visual metaphors:** Сложная идея = простой визуальный образ. Не объяснять — показывать.
- **Fact-checking:** Отдельный этап. Эксперты читают перед продакшеном.
- Релевантно: принцип "сначала текст, потом визуал" (voice-first) совпадает с подходом AI Office

### 6.4 Explainer Video Industry (60-секундный стандарт)
- **140-160 слов** на 60 секунд при нормальном темпе речи
- **Формула:** Hook (10 сек) → Problem (10 сек) → Solution (30 сек) → CTA (10 сек)
- **Правило:** "Edit to remove anything that doesn't serve the central message"
- **Язык:** Разговорный, сокращения, короткие фразы. "Не лекция — разговор."

**Источники:**
- [SparkShorts — Pixar](https://www.pixar.com/sparkshorts)
- [Love Death Robots Short-Form Storytelling — No Film School](https://nofilmschool.com/love-death-and-robots-displays-short-term-storytelling)
- [Worldbuilding in an Instant — No Film School](https://nofilmschool.com/worldbuilding-in-an-instant-love-death-robots)
- [Kurzgesagt Video Production Process — 10 Studio](https://10.studio/the-incredible-amount-of-work-behind-kurzgesagts-beautiful-animated-videos/)
- [How to Write Explainer Video Script — Creamy Animation](https://creamyanimation.com/how-to-write-an-explainer-video-script/)

---

## 7. AI-ASSISTED WORKFLOWS (2025-2026)

### Как студии используют AI в сценаристике:

1. **Netflix (2025):** Внутренний AI-инструмент для storyboards и scene breakdowns из текста. Сокращение pre-production на 30-50%. Но **сценарий пишут люди**.

2. **BoundaryML podcast (2025):** Полный pipeline "AI that works" — от промпта к анимации. Claude/GPT генерируют script breakdown, затем автоматическая раскадровка.

3. **CJ ENM (Korea):** AI сжимает pipeline с 18-24 месяцев до 12. Pre-production (storyboards, character sheets) — основная зона ускорения.

### Модель для AI Office:
```
Юрий (выбор истории + решения)
  → Claude/scenario (сценарий + промпты)      ← AI пишет
    → Midjourney (визуал)                       ← AI генерирует
      → Seedance (анимация)                     ← AI оживляет
        → ElevenLabs (голос)                    ← AI озвучивает
          → assemble.py (сборка)                ← AI монтирует
```

Это полностью AI-assisted pipeline, где человек — creative director и final approver.

**Источники:**
- [Building an Animation Pipeline — BoundaryML](https://boundaryml.com/podcast/2025-11-18-building-an-animation-pipeline)
- [Animation Pipeline Optimization 2026 — Vitrina AI](https://vitrina.ai/blog/animation-pipeline-optimization-global-studios-2026)

---

## 8. PIXAR 22 RULES — ВЫЖИМКА ДЛЯ 60-СЕКУНДНОГО ФОРМАТА

Из 22 правил Emma Coats, адаптированные под наш формат:

| # | Правило Pixar | Применение к AI Office (60 сек) |
|---|--------------|-------------------------------|
| 1 | Admire trying > succeeding | Юрий ошибается с AI — и это нормально. Зритель уважает попытку. |
| 2 | Audience > writer | Не "мне интересно рассказать", а "зрителю интересно узнать". |
| 4 | Story Spine | Каждая серия проверяется через Story Spine (см. 1.1). |
| 6 | Challenge = opposite | Юрий-скептик получает AI-энтузиастов. Юрий-контролёр получает AI который врёт. |
| 7 | End before middle | Знай инсайт ДО написания сценария. Пиши от финала к началу. |
| 13 | Characters need opinions | Клодище, Шерлок, Алекс — у каждого позиция. Пассивные = яд. |
| 16 | What are the stakes? | Что теряет Юрий если AI облажается? Клиента. Деньги. Лицо. |
| 19 | Coincidence in, not out | AI может СОЗДАТЬ проблему случайно. Но решение = осознанное. |
| 22 | What's the essence? | Если убрать всё лишнее — что останется? Это и есть серия. |

**Источники:**
- [Pixar 22 Rules — Industrial Scripts](https://industrialscripts.com/pixar-storytelling-rules/)
- [Pixar 22 Rules — No Film School](https://nofilmschool.com/pixar-story-structure)
- [Pixar 22 Rules — Daniel Scrivner](https://www.danielscrivner.com/pixar-22-rules-of-storytelling-and-7-sentences-to-build-stronger-stories/)

---

## 9. СВОДНАЯ РЕКОМЕНДАЦИЯ: ЧТО ВНЕДРИТЬ В SKILL.md

### Немедленно (высокий импакт, мало усилий):

1. **ABT-тест** — добавить в верификацию: "Опиши серию в одном AND-BUT-THEREFORE. Если не можешь — расфокус."

2. **Story Spine check** — добавить в секцию "Как скилл пишет сценарий": перед написанием раскадровки заполни Story Spine для серии.

3. **Типология хуков** — добавить таблицу из секции 2 в инструкции сценариста: Bold Statement / Mid-Action / Question / Contrast / Confession.

4. **Word count guard** — добавить в верификацию: "Текст озвучки Юрия: 80-100 слов (русский) / 100-130 слов (английский) на 60 секунд."

5. **Тест последних 10 секунд** — добавить: "Финал серии = определяет вернётся ли зритель. Вопрос или крючок. Не точка."

### Следующий этап (средний импакт):

6. **Vocabulary Bank** — создать для ключевых персонажей (Клодище, Today, Алекс, Шерлок).

7. **Reaction Matrix** — таблица "персонаж x ситуация → реакция" для сценариста.

8. **Expression Sheet prompts** — расширить PROMPTS.md: для каждого персонажа 3-4 эмоции (neutral, happy, frustrated, surprised).

### На будущее (стратегическое):

9. **Dan Harmon Circle mapping** — формализовать 8 шагов как альтернативный check для сложных серий.

10. **Minimum viable worldbuilding** — правило L,D+R: "Что минимум нужно знать о мире агентов чтобы понять конфликт?"

---

*Исследование: 28 марта 2026*
*На основе: 15+ веб-источников, индустриальные стандарты Pixar/Netflix/Kurzgesagt, micro drama формат 2025-2026*
