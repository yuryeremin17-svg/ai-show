# Midjourney Prompt Engineering Guide — AI Office Series

> Практический справочник для генерации консистентных кадров анимационного сериала.
> Стиль: stylized warm illustration, Pixar-style. Формат: 9:16 (vertical).
> Актуально: Midjourney V6.1 / V7 (март 2026).

---

## 1. Формула промпта (порядок имеет значение)

Midjourney уделяет больше внимания словам в НАЧАЛЕ промпта. Порядок = приоритет.

### Универсальная формула для AI Office:

```
[STYLE LOCK], [SUBJECT + ACTION], [EMOTION/EXPRESSION], [ENVIRONMENT], [LIGHTING], [CAMERA/COMPOSITION], [MOOD] --ar 9:16 --cref [URL] --cw [0-100] --sref [CODE] --no [unwanted]
```

### Пример (полный):

```
stylized warm illustration, tall thin man in black turtleneck with round glasses excitedly presenting three design options on glowing screen, proud confident expression, modern bright office with Dubai skyline through floor-to-ceiling windows, warm golden hour lighting, medium shot from slightly below, energetic optimistic mood, Pixar-style character design --ar 9:16 --cref [URL] --cw 100 --sref [CODE]
```

### Разбор по слотам:

| # | Слот | Что писать | Почему здесь |
|---|------|-----------|-------------|
| 1 | **Style lock** | `stylized warm illustration` | Первые слова = максимальный вес. Фиксирует стиль. |
| 2 | **Subject + Action** | `tall thin man in black turtleneck with round glasses presenting options` | Главный объект кадра — сразу после стиля. |
| 3 | **Emotion/Expression** | `proud confident expression` | Pixar = эмоции. Без них — мёртвый кадр. |
| 4 | **Environment** | `modern bright office, Dubai skyline through windows` | Контекст сцены. |
| 5 | **Lighting** | `warm golden hour lighting` | Свет = настроение. Конкретный термин > "nice lighting". |
| 6 | **Camera/Composition** | `medium shot from slightly below` | Контролирует ракурс и масштаб. |
| 7 | **Mood anchor** | `energetic optimistic mood` | Финальный усилитель атмосферы. |
| 8 | **Style tail** | `Pixar-style character design` | Повторное закрепление стиля в конце промпта. |
| 9 | **Parameters** | `--ar 9:16 --cref --cw --sref --no` | Всегда в самом конце. |

### Оптимальная длина: 20-40 слов (без параметров)

- Меньше 15 слов — слишком много додумывает MJ.
- Больше 50 слов — начинает игнорировать часть.
- Каждое слово должно работать. Если можно убрать без потери смысла — убирай.

---

## 2. Style Lock — как держать единый стиль на 20+ кадров

### Три уровня фиксации (использовать ВСЕ ТРИ одновременно):

**Уровень 1: Текстовый якорь (в каждом промпте)**
```
stylized warm illustration ... Pixar-style character design
```
- `stylized warm illustration` — ПЕРВЫЕ слова каждого промпта (максимальный вес)
- `Pixar-style character design` — в конце промпта (закрепление)
- Никогда не менять эти фразы между кадрами серии

**Уровень 2: --sref код (Style Reference)**
```
--sref [CODE]
```
- Сгенерируй 1 идеальный кадр в нужном стиле
- Открой Style Creator на midjourney.com — создай код из этого кадра
- Используй ОДИН И ТОТ ЖЕ --sref код для ВСЕХ кадров серии
- Лайкни код — он сохранится в Likes для повторного использования
- Можно миксовать коды: `--sref CODE1 CODE2` (но для серии лучше один)

**Уровень 3: --cref мастер-образ (Character Reference)**
```
--cref [URL мастер-образа] --cw 100
```
- Мастер-образы уже созданы: `assets/characters/masters/`
- --cref фиксирует не только персонажа, но и частично стиль
- Один и тот же мастер-образ = визуальный якорь серии

### Чек-лист стиля перед генерацией серии:

- [ ] Текстовый якорь одинаковый во всех промптах
- [ ] --sref код создан и записан
- [ ] Мастер-образы загружены на midjourney.com
- [ ] Тестовый кадр сгенерирован и одобрен
- [ ] Все промпты серии используют ту же формулу

---

## 3. --cref / --oref — Character Reference

### Какой параметр использовать:

| Версия MJ | Параметр | Что делает |
|-----------|----------|-----------|
| V6 / V6.1 | `--cref URL` | Character Reference. Копирует лицо + одежду + волосы. |
| V7 | `--oref URL` | Omni Reference. Замена --cref. Более точная. Стоит 2x GPU. |
| V7 | `--cref` | **НЕ РАБОТАЕТ в V7!** Используй --oref. |

### Вес персонажа (--cw / --ow):

| Значение | Что копирует | Когда использовать |
|----------|-------------|-------------------|
| `--cw 100` (default) | Лицо + волосы + одежда | Стандартные кадры. Персонаж "как есть". |
| `--cw 50` | Лицо + волосы, одежда свободнее | Персонаж в другой одежде (костюм → casual). |
| `--cw 0` | Только лицо | Полная смена образа, только лицо узнаваемое. |

Для V7: `--ow` вместо `--cw`, диапазон 0-1000 (default 100).

### Правила для лучших результатов --cref:

1. **Один персонаж на мастер-образе.** Несколько лиц = путаница.
2. **Фронтальный ракурс.** Анфас или 3/4 — НЕ профиль, НЕ затылок.
3. **Хорошее освещение.** Без теней на лице.
4. **Сгенерированное MJ изображение работает лучше реальных фото.** Для Юрия (реальное фото) — может потребоваться несколько попыток.
5. **Формат мастер-образа:** портрет 2:3 или 4:5 (для лица) или 1:1 (для full body).

### Несколько персонажей в одном кадре:

**Проблема:** --cref с двумя персонажами часто сливает их в одного.

**Решения:**
- **Метод A (текстовое разделение):** Описать персонажей максимально контрастно в тексте + один --cref.
- **Метод B (раздельная генерация):** Сгенерировать персонажей отдельно → совместить в Photoshop/Canva.
- **Метод C (V7 --oref):** Загрузить изображение с двумя персонажами как --oref и описать обоих в промпте.

**Наша практика для AI Office:**
- Кадры с 1 персонажем — --cref его мастер-образ, `--cw 100`
- Кадры с 2 персонажами — текстом описать обоих контрастно, --cref главного персонажа кадра
- Кадры с 3+ — рассмотреть раздельную генерацию

---

## 4. Запрещённые слова и антипаттерны

### Слова, вызывающие нестабильность стиля:

| Не писать | Почему | Писать вместо |
|-----------|--------|--------------|
| `beautiful` | Слишком абстрактно, MJ додумывает | Конкретное описание: `warm`, `elegant`, `charming` |
| `amazing`, `stunning` | Пустые усилители | Конкретный визуал: `dramatic lighting`, `vivid colors` |
| `realistic`, `photorealistic` | Ломает стилизованный стиль | `stylized`, `illustrated` |
| `4K`, `8K`, `high resolution` | Не влияет на стиль, засоряет промпт | Убрать. MJ генерит в своём разрешении. |
| `HDR` | Даёт фотоэффект, не иллюстрацию | `warm tones`, `rich colors` |
| `don't`, `without`, `not` | MJ НЕ понимает отрицания в тексте! | Использовать `--no` параметр |
| `hyper-detailed` | Тянет в фотореализм | `detailed`, `intricate` |
| `trending on ArtStation` | Устаревший хак, нестабильный результат | Конкретный стиль: `Pixar-style` |
| `masterpiece` | Пустое слово | Убрать |
| `unreal engine`, `octane render` | 3D-рендер вместо иллюстрации | `warm illustration` |

### Параметр --no (негативный промпт):

```
--no text, watermark, logo, photorealistic, anime, dark, gloomy
```

- Один `--no` на промпт (не несколько)
- Перечисление через запятую внутри одного --no
- Для нашего стиля стандартный набор:
  ```
  --no text, watermark, logo, photorealistic, anime, 3d render, dark shadows
  ```

---

## 5. Шаблоны промптов для сцен AI Office

### Шаблон A: Один персонаж крупно (портрет/реакция)

```
stylized warm illustration, [ОПИСАНИЕ ПЕРСОНАЖА] [ДЕЙСТВИЕ/ПОЗА], [ЭМОЦИЯ] expression, [ДЕТАЛИ ОКРУЖЕНИЯ], [ОСВЕЩЕНИЕ], close-up portrait shot, [НАСТРОЕНИЕ], Pixar-style character design --ar 9:16 --cref [URL] --cw 100 --no text, watermark, photorealistic
```

**Пример:**
```
stylized warm illustration, tall thin man in black turtleneck with round glasses crossing arms with skeptical raised eyebrow, disapproving expression, modern office desk with messy papers behind him, warm soft studio lighting, close-up portrait shot, humorous slightly tense mood, Pixar-style character design --ar 9:16 --cref [claude_master] --cw 100 --no text, watermark, photorealistic
```

### Шаблон B: Два персонажа в диалоге

```
stylized warm illustration, [ПЕРСОНАЖ 1 + ДЕЙСТВИЕ] facing [ПЕРСОНАЖ 2 + ДЕЙСТВИЕ], [ЭМОЦИИ ОБОИХ], [СРЕДА], [ОСВЕЩЕНИЕ], medium two-shot, [НАСТРОЕНИЕ], Pixar-style character design --ar 9:16 --cref [URL главного] --cw 100 --no text, watermark, photorealistic
```

**Пример:**
```
stylized warm illustration, confident Mediterranean man late 50s in blue shirt leaning forward pointing at screen facing tall thin man in black turtleneck with round glasses stepping back surprised, determined expression vs caught-off-guard expression, modern bright office, warm afternoon light through windows, medium two-shot, dynamic confrontational mood, Pixar-style character design --ar 9:16 --cref [yuri_master] --cw 100 --no text, watermark, photorealistic
```

### Шаблон C: Обстановка / Establishing shot (без крупных персонажей)

```
stylized warm illustration, [СРЕДА + ДЕТАЛИ], [small figure(s) ОПИСАНИЕ если нужно], [ОСВЕЩЕНИЕ], wide establishing shot, [НАСТРОЕНИЕ], Pixar-style environment design --ar 9:16 --no text, watermark, photorealistic
```

**Пример:**
```
stylized warm illustration, modern bright open-plan office with glass walls and Dubai skyline panorama, multiple screens showing dashboards, coffee cups and papers on desks, small figure in black turtleneck walking between desks, warm morning golden light streaming through windows, wide establishing shot, busy productive mood, Pixar-style environment design --ar 9:16 --no text, watermark, photorealistic
```

### Шаблон D: Экран / UI / Инфографика (split screen, сравнение)

```
stylized warm illustration, split screen composition, left side showing [ВАРИАНТ A], right side showing [ВАРИАНТ B], [ВИЗУАЛЬНЫЙ КОНТРАСТ], clean infographic layout, warm palette, Pixar-style graphic design --ar 9:16 --no text, watermark, photorealistic
```

### Шаблон E: Эмоциональный пик / ключевой кадр

```
stylized warm illustration, [ПЕРСОНАЖ в ДРАМАТИЧНОМ МОМЕНТЕ], [СИЛЬНАЯ ЭМОЦИЯ] expression, [ДРАМАТИЧНЫЕ ДЕТАЛИ СРЕДЫ], [ДРАМАТИЧНОЕ ОСВЕЩЕНИЕ: rim light / dramatic side lighting], dynamic [angle: low angle / dutch angle], [INTENSE MOOD], Pixar-style character design --ar 9:16 --cref [URL] --cw 100 --no text, watermark, photorealistic
```

---

## 6. Вертикальный формат 9:16 — специфика

### Что работает в 9:16:

- **Вертикальные элементы** — стоящие персонажи, колонны, здания, дверные проёмы
- **Портреты** — крупный план лица / верхняя часть тела
- **Многоуровневая композиция** — передний план (стол/руки) + средний (персонаж) + фон (окно/город)
- **Правило третей** — глаза персонажа на верхней трети
- **Негативное пространство сверху** — оставлять место для субтитров

### Что НЕ работает в 9:16:

- Горизонтальные панорамы (обрежутся)
- Групповые сцены с 3+ персонажами в ряд (не влезут)
- Широкие офисные виды (потеряют детали)

### Промпт-добавки для 9:16:

| Нужен результат | Добавить в промпт |
|----------------|-------------------|
| Персонаж в полный рост | `full body portrait, standing pose` |
| Крупный план лица | `close-up portrait, head and shoulders` |
| Средний план (по пояс) | `medium shot, waist up` |
| Пространство для субтитров | `negative space at bottom of frame` |
| Глубина (многослойность) | `foreground object slightly blurred, character in middle ground, background visible` |

---

## 7. Словарь арт-дирекции

### Освещение (Lighting):

| Термин | Эффект | Когда использовать |
|--------|--------|-------------------|
| `warm golden hour lighting` | Тёплый мягкий свет, золотые тона | Позитивные сцены, финалы, инсайты |
| `soft diffused morning light` | Мягкий утренний, без резких теней | Спокойные сцены, утренние брифинги (Today) |
| `warm studio lighting` | Равномерный тёплый, как в студии | Стандартные офисные сцены |
| `dramatic side lighting` | Контрастный боковой свет | Конфликтные моменты, напряжение |
| `rim light` (контровый) | Светящийся контур вокруг фигуры | Героические моменты, важные решения |
| `warm afternoon light through windows` | Свет из окон, Дубай за стеклом | Стандартная офисная среда AI Office |
| `cinematic lighting` | Кинематографичное, с глубиной | Ключевые драматичные кадры |
| `low-key lighting` | Много теней, драматично | Тревожные моменты (ошибки, провалы) |
| `high-key lighting` | Яркий, почти без теней | Лёгкие комедийные моменты |
| `volumetric light rays` | Лучи света в воздухе (God rays) | Моменты озарения, "эврика" |
| `cool blue ambient light` | Холодный голубоватый | Экраны, технологические сцены |
| `neon glow` | Неоновое свечение | НЕ использовать (ломает стиль Pixar) |

### Камера (Camera angles):

| Термин | Эффект | Когда |
|--------|--------|-------|
| `close-up` | Только лицо | Эмоции, реакции |
| `medium shot` | По пояс | Диалоги, стандарт |
| `medium full shot` | По колени | Действия с руками + контекст |
| `full body shot` | В полный рост | Представление персонажа |
| `wide shot` | Персонаж + много среды | Establishing shots |
| `over-the-shoulder shot` | Через плечо одного на другого | Диалоги между двумя |
| `low angle` (снизу вверх) | Власть, доминирование | Юрий принимает решение |
| `high angle` (сверху вниз) | Уязвимость, подчинение | Клодище пойман на ошибке |
| `eye level` | Нейтрально, на уровне глаз | Стандартные сцены |
| `dutch angle` | Наклон, дезориентация | Когда что-то идёт не так |
| `bird's-eye view` | Вид сверху | Общий план офиса |

### Эмоции (Expressions):

| Термин | Визуал |
|--------|--------|
| `proud confident expression` | Гордость, уверенность |
| `skeptical raised eyebrow` | Скептицизм (Юрий) |
| `guilty half-smile` | Пойман, но с юмором (Клодище) |
| `excited wide eyes` | Восторг (Алекс-скаут) |
| `calm knowing smile` | Спокойная уверенность (Today) |
| `disapproving pursed lips` | Недовольство (Шерлок-QA) |
| `dreamy inspired upward gaze` | Витает в облаках (Байрон) |
| `caught-off-guard surprised` | Застигнут врасплох |
| `determined focused gaze` | Решительность |
| `warm genuine laugh` | Настоящий смех |
| `subtle mysterious smile` | Загадочная улыбка (Стелла) |
| `overwhelmed exhausted` | Заваленный работой |

### Настроение сцены (Mood):

| Термин | Когда |
|--------|-------|
| `warm cozy atmosphere` | Позитивный рабочий момент |
| `tense confrontational mood` | Конфликт / спор |
| `humorous lighthearted mood` | Комедийная сцена |
| `nostalgic reflective mood` | Флэшбек, воспоминание |
| `energetic dynamic mood` | Экшн, прорыв |
| `calm professional atmosphere` | Спокойная работа |
| `dramatic revelation mood` | Момент истины |
| `chaotic office energy` | Офисный хаос, суета |

---

## 8. V6 vs V7 — что использовать для AI Office

### Рекомендация: V6.1 как основная, V7 для тестирования

| Критерий | V6 / V6.1 | V7 |
|----------|-----------|-----|
| Стилизация Pixar | Лучше контроль | Тянет к фотореализму |
| --cref | Работает | **НЕ работает!** Нужен --oref |
| --sref | Работает | Работает (улучшен) |
| Скорость | Стандартная | +25% быстрее |
| Текст на картинке | Плохо | Хорошо (но нам не нужен) |
| Стоимость --oref | — | 2x GPU |

### Как зафиксировать версию:

```
... --v 6.1
```
или
```
... --v 7
```

Если не указать — используется дефолт сервера (сейчас V7). Для стабильности серии **всегда указывай версию явно**.

---

## 9. Рабочий процесс генерации серии (чек-лист)

### До генерации:

1. Раскадровка готова (скилл scenario)
2. Выбрать --sref код: сгенерировать 1 тестовый кадр → создать код через Style Creator → записать
3. Загрузить мастер-образы персонажей на midjourney.com
4. Записать URL мастер-образов для --cref

### Генерация каждого кадра:

1. Собрать промпт по формуле (Раздел 1)
2. Добавить --cref нужного персонажа
3. Добавить --sref код серии
4. Добавить --ar 9:16 --v 6.1
5. Добавить --no text, watermark, photorealistic
6. Сгенерировать → выбрать лучший из 4-х → Upscale
7. Проверить: стиль совпадает с предыдущими кадрами? Персонаж узнаваем?

### После генерации всех кадров:

1. Разложить по `assets/scenes/S01EXX/01.png ... NN.png`
2. Визуальная проверка: все кадры в одном стиле?
3. Если нужно — регенерировать выбивающиеся кадры
4. Опционально: img2vid через Seedance/Dreamina

---

## 10. Промпт-веса (::) — продвинутая техника

Для акцентирования важных частей промпта:

```
stylized warm illustration::2, tall thin man in black turtleneck::1.5 crossing arms, skeptical expression, modern office --ar 9:16
```

- `::2` — этот фрагмент в 2 раза важнее стандартного
- `::1` — стандартный вес (по умолчанию)
- `::0.5` — менее важный, фоновый
- Используй для стиля (`stylized warm illustration::2`) — гарантирует что стиль не потеряется

---

## 11. Быстрая шпаргалка (копировать при генерации)

### Стандартный хвост промпта:

```
Pixar-style character design --ar 9:16 --v 6.1 --cref [URL] --cw 100 --sref [CODE] --no text, watermark, logo, photorealistic, anime, 3d render
```

### Стандартное начало промпта:

```
stylized warm illustration,
```

### Стандартная среда офиса:

```
modern bright open-plan office with glass walls, Dubai skyline through floor-to-ceiling windows
```

### Стандартное освещение (выбрать одно):

```
warm afternoon light through windows
soft diffused morning light
warm golden hour lighting
dramatic side lighting
```

---

## Источники

- [Midjourney Character Reference — docs](https://docs.midjourney.com/hc/en-us/articles/32162917505293-Character-Reference)
- [Midjourney Omni Reference — docs](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference)
- [Midjourney Style Reference — docs](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference)
- [Midjourney Style Creator — docs](https://docs.midjourney.com/hc/en-us/articles/41308374558221-Style-Creator)
- [Midjourney Multi-Prompts & Weights — docs](https://docs.midjourney.com/hc/en-us/articles/32658968492557-Multi-Prompts-Weights)
- [Midjourney Prompt Basics — docs](https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics)
- [Midjourney --no parameter — docs](https://docs.midjourney.com/hc/en-us/articles/32173351982093-No)
- [Consistent Characters Guide 2026 — Medium](https://medium.com/@impijushsaha/how-to-create-consistent-characters-in-midjourney-the-complete-guide-for-2026-405c3bfbb4e1)
- [ImaginePro — Omni-Reference Guide](https://www.imaginepro.ai/blog/2025/7/midjourney-omni-reference-guide)
- [ImaginePro — Character Reference Guide](https://www.imaginepro.ai/blog/2025/7/midjourney-character-reference-guide)
- [Midjourney Camera & Lighting Prompts — Aituts](https://aituts.com/midjourney-camera-prompts/)
- [Midjourney Cartoon Styles — Aiarty](https://www.aiarty.com/midjourney-prompts/midjourney-cartoon-styles.htm)
- [Midjourney Lighting Keywords — Medium](https://medium.com/@robmoraisjr/mastering-midjourney-series-the-12-lighting-keywords-you-need-to-know-4b3a3c7ab283)
- [Midjourney Prompt Formula — Skywork](https://skywork.ai/blog/midjourney-prompts-formulas-2025/)
- [Midjourney V7 Cheat Sheet — Medium](https://medium.com/@alijeebutt99/the-ultimate-midjourney-v7-cheat-sheet-parameters-styles-and-tips-a9a4e4c99583)
- [Midjourney V6 vs V7 — AIArtForce](https://www.aiartforce.com/blogs/ai-art-force-blog/midjourney-v6-vs-v7-differences-and-how-to-use-them-may-2-2025)
- [Midjourney Prompts Guide 2026 — Printify](https://printify.com/blog/midjourney-prompts/)
- [Midjourney Camera Angles — Aiarty](https://www.aiarty.com/midjourney-prompts/midjourney-camera-angles.htm)
- [Midjourney Negative Prompts — Aiarty](https://www.aiarty.com/midjourney-prompts/midjourney-negative-prompts.htm)
- [SREF Codes Library — promptsref.com](https://promptsref.com/)

---

*Создано: 28 марта 2026*
*На основе: Midjourney docs, community best practices, research 2025-2026*
