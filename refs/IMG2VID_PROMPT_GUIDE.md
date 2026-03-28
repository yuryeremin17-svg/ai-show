# IMG2VID Prompt Engineering Guide

> Для проекта AI_SHOW: Pixar-стиль, 9:16, персонажи-агенты + реальный Юрий
> Составлено: 28 марта 2026
> Источники: 20+ профессиональных гайдов, GitHub-репозитории, официальная документация

---

## 1. Универсальная формула промпта

### Структура (работает для Seedance, Kling, Runway)

```
[Subject + Action] + [Camera Movement] + [Setting/Atmosphere] + [Style/Lighting] + [Constraints]
```

**Развернутая формула (5 слоев):**

| Слой | Что описывает | Пример |
|------|--------------|--------|
| **Subject** | Кто/что в кадре (1 персонаж, возраст, одежда) | A stylized Pixar-style AI robot character in a navy suit |
| **Action** | Одно действие, настоящее время, конкретный глагол | slowly nods while gesturing with right hand |
| **Camera** | Размер кадра + движение + угол | Medium close-up, slow push-in, eye level |
| **Style** | Визуальный якорь + свет + цвет | Warm golden afternoon light, soft shadows, Pixar-style 3D animation |
| **Constraints** | Запреты (позитивная формулировка!) | Clear facial features, stable face, no distortion, smooth motion |

### Золотое правило: ОДИН кадр = ОДНО действие = ОДНО движение камеры

---

## 2. Словарь движений (Motion Vocabulary)

### Тонкие движения (НАШЕ основное — для talking heads и реакций)

| Английский | Что дает | Когда использовать |
|-----------|---------|-------------------|
| gently nods | мягкий кивок | согласие, слушание |
| slowly turns head | плавный поворот головы | взгляд на собеседника |
| slight head tilt | легкий наклон головы | удивление, интерес |
| subtle eyebrow raise | поднятие бровей | вопрос, скепсис |
| soft smile forming | мягкая улыбка появляется | одобрение |
| eyes glistening with emotion | глаза блестят | момент инсайта |
| leans slightly forward | легкий наклон вперед | интерес, внимание |
| leans back in chair | откидывается в кресле | уверенность, расслабление |
| crosses arms slowly | медленно скрещивает руки | скепсис, защита |
| taps fingers on desk | постукивает пальцами по столу | нетерпение, раздумье |
| adjusts glasses | поправляет очки | сосредоточенность |
| takes a deep breath | глубокий вдох | перед важным решением |
| blinks naturally | естественное моргание | реализм |
| exhales slowly | медленный выдох | облегчение |
| rests chin on hand | подпирает подбородок рукой | задумчивость |

### Модификаторы интенсивности

| Модификатор | Эффект |
|------------|--------|
| **gently, softly** | минимальное движение |
| **slowly, gradually** | замедленное действие |
| **subtly, barely** | еле заметное |
| **naturally, fluidly** | органичное, без механичности |
| **deliberately, steadily** | контролируемое, уверенное |

### Слова, усиливающие движение (использовать ОСТОРОЖНО)

| Модификатор | Эффект |
|------------|--------|
| **quickly, rapidly** | ускоренное |
| **dramatically** | преувеличенное |
| **explosively, violently** | экстремальное (НЕ для нас) |
| **energetically** | энергичное |

### Фоновые/средовые движения (добавляют жизнь сцене)

```
A light breeze moves hair and clothing
Dust motes drift in sunlight through windows
Subtle shadows shift across the wall
Steam rises gently from coffee cup
Screen light flickers softly on face
Papers rustle slightly on desk
City lights twinkle through window behind
Clouds drift slowly across Dubai skyline
```

---

## 3. Камера: термины и эффекты

### Основные движения камеры

| Термин | Что делает | Когда использовать |
|--------|-----------|-------------------|
| **slow push-in** | Камера медленно приближается | Эмоциональный момент, раскрытие |
| **gentle pull-back** | Камера медленно отъезжает | Показать контекст, среду |
| **slow pan left/right** | Горизонтальный поворот | Осмотр пространства |
| **subtle tilt up/down** | Вертикальный наклон | Взгляд сверху вниз или снизу вверх |
| **tracking shot** | Камера следует за субъектом | Движение персонажа |
| **static shot** | Камера неподвижна | Talking head, диалог |
| **slow orbit** | Камера медленно облетает | Драматичный момент |
| **rack focus** | Смена фокуса с одного объекта на другой | Переключение внимания |

### Что работает ЛУЧШЕ ВСЕГО для нашего формата

**Рекомендации для Pixar-стиль + talking head:**

1. **slow push-in** — лучший друг. Усиливает эмоцию, не отвлекает
2. **static shot + subtle dolly** — для диалогов
3. **gentle pull-back** — для раскрытия сцены (начало кадра)
4. **slow orbit** — для "wow" моментов (кульминация)

**Избегать:**
- whip pan (слишком агрессивно)
- snap zoom (рвет атмосферу)
- Dutch angle (не подходит для стилизации)
- handheld shake (конфликтует с Pixar-эстетикой)

### Формулировка для камеры (Seedance-оптимальная)

```
Camera: [shot size], [movement type], [speed], [angle]
```

Примеры:
```
Camera: medium close-up, slow push-in, smooth gimbal, eye level
Camera: wide shot, gentle pull-back, steady, slightly high angle
Camera: close-up, static tripod, no movement
Camera: medium shot, slow 180-degree orbit, smooth, eye level
```

---

## 4. Constraint-фразы (предотвращение артефактов)

### Обязательный блок для КАЖДОГО промпта AI_SHOW

```
Clear facial features, stable face, no distortion, no deformation.
Natural body proportions, no stiffness. Same character throughout.
4K ultra-high definition, rich details, sharp resolution.
Natural and fluid motion, smooth and stable footage.
Silky smooth camera movement, no jitter, no flickering.
```

### Категории constraint-фраз

**Лицо и тело:**
```
Clear facial features, stable face, no distortion
Normal body proportions, natural structure
Detailed hands, anatomically correct fingers
Same character, consistent clothing, unchanged hairstyle
Maintain facial features and wardrobe consistent with @Image1
```

**Движение:**
```
Natural and fluid motion
Smooth and stable footage
No blur, no ghosting, no flickering
Physically accurate, natural motion
Gestures follow speech flow without mechanical repetition
```

**Камера:**
```
Silky smooth camera movement, no jitter
No snap zooms, no whip pans
No Dutch angles, no jump cuts
Steady footage, stable horizon
```

**Среда:**
```
No extra characters, no crowd
No text overlays, no watermarks
No floating UI elements
No rain/fog/smoke unless specified
Clean background, no clutter
```

**Стиль:**
```
Warm stylized Pixar-style 3D animation
Consistent color palette throughout
Cinematic quality, natural colors, soft lighting
No neon, no heavy color grading
No cartoon saturation, maintain warmth
```

### ВАЖНО: Seedance НЕ поддерживает negative prompts

Вместо: "no distortion, don't deform the face"
Писать: "Clear facial features, stable face, natural proportions"

Всегда **позитивная формулировка** того, что ХОТИМ, а не того, чего НЕ хотим.
Исключение: "no flickering, no jitter" — работают как constraint, не как negative prompt.

---

## 5. Time Segments (временные сегменты)

### Когда использовать

- Клипы **до 5 сек** — НЕ нужны (одно действие)
- Клипы **5-10 сек** — опционально (помогают)
- Клипы **10-15 сек** — ОБЯЗАТЕЛЬНО (без них модель теряет фокус)

### Формат

```
0-3s: [setup / начальная сцена]
4-7s: [main action / основное действие]
8-10s: [resolution / завершение]
```

Для 15 секунд:
```
0-3s: [setup]
4-8s: [development]
9-12s: [climax / turn]
13-15s: [resolution / hold]
```

### Примеры для AI_SHOW

**Кадр: Клодище реагирует на задачу**
```
0-3s: Medium close-up. Klodische (blue AI robot in navy suit) sits at desk, reading screen. Slight head tilt, processing information.
4-8s: Eyes widen subtly, slight lean forward. A soft smile begins forming. Right hand rises in a gentle "eureka" gesture.
9-10s: Confident nod, settles back. Screen reflects in eyes. Camera holds.
```

**Кадр: Юрий объясняет идею**
```
0-4s: Medium shot. Real man (50s, beard, glasses) sits in modern office chair. Gestures with right hand while speaking. Camera: slow push-in.
5-9s: Leans forward slightly, makes eye contact. Left hand joins gesture for emphasis. Warm afternoon light through windows.
10-12s: Slight smile, nods. Settles back confidently. Camera holds on expression.
```

### Правила time segments

1. **Каждый сегмент = одно действие** (не перегружать)
2. **Последний сегмент = hold** (камера фиксируется, персонаж в финальной позе)
3. **Не перекрывать timestamps** (0-3, 4-7, 8-10 — НЕ 0-3, 2-5, 4-7)
4. **Subject повторять** в каждом сегменте (модель может забыть)

---

## 6. Чего ИЗБЕГАТЬ (антипаттерны)

### Убивают качество

| Ошибка | Почему плохо | Как исправить |
|--------|-------------|--------------|
| Два+ действия в одном промпте | Модель путается, ни одно не делает хорошо | Одно действие на кадр |
| Описание внешности при img2vid | Конфликт с входной картинкой | При img2vid описывать ТОЛЬКО движение |
| "beautiful", "amazing", "cool" | Пустые слова, модель игнорирует | Конкретные визуальные термины |
| Промпт > 200 слов | Модель теряет фокус | 50-150 слов оптимально |
| Промпт < 30 слов | Недостаточно информации | Минимум 40-50 слов |
| Негативные фразы "don't do X" | Seedance/Runway не понимают | Позитивные constraint-фразы |
| Множественные камеры в одном кадре | Хаотичный результат | Одно движение камеры на кадр |
| 3+ персонажа в кадре | Identity confusion | Максимум 2 персонажа |
| Смена среды mid-prompt | Модель путается между сценами | Одна среда на промпт |
| Абстрактные концепции | "feel of freedom" — модель не понимает | Конкретные физические действия |

### Слова-убийцы (вызывают проблемы)

```
ИЗБЕГАТЬ: exaggerated, extreme, high-speed, aggressive, violent
ИЗБЕГАТЬ: beautiful, cool, amazing, nice, good, interesting
ИЗБЕГАТЬ: somehow, kind of, sort of, maybe
ИЗБЕГАТЬ: transform into, morph, change shape (при сохранении персонажа)
```

### Правило переделки

- 1-я попытка не удалась -> меняем Camera или Action (НЕ добавляем слова)
- 2-я попытка не удалась -> меняем reference image или shot plan
- 3-я попытка не удалась -> СТОП, переосмыслить подход

---

## 7. Сравнение платформ для нашей задачи

### Задача: Pixar-стиль иллюстрация -> анимация (тонкие движения, 9:16, 5-15 сек)

| Критерий | Seedance 2.0 | Kling 3.0 | Runway Gen-4 |
|----------|-------------|-----------|-------------|
| **Наш вердикт** | **ОСНОВНОЙ** | Запасной | Для экспериментов |
| Стиль анимации | Отлично (anime/Pixar) | Хорошо | Средне (реализм лучше) |
| Консистентность персонажа | Отлично (@Image refs) | Средне (1-2 img) | Хорошо (multi-ref) |
| Тонкие движения | Отлично | Отлично | Хорошо |
| Камера | Отлично | Хорошо | Отлично |
| Разрешение | 2K | 1080p | 720p (free) / 4K (paid) |
| Длительность | до 15 сек | до 10 сек | 5 или 10 сек |
| FPS | 24 (кинематограф) | 30 (smooth) | 24 |
| Reference inputs | до 12 (9 img + 3 vid + 3 audio) | 1-2 img | Multi-image |
| Стоимость ~10 сек | ~$0.60 | ~$0.50 | ~$0.50 (Standard) |
| Watermark | Нет | Да (убирается на paid) | Нет (paid) |
| Доступность ОАЭ | Dreamina / CapCut (веб) | klingai.com (веб) | runwayml.com |
| Negative prompts | НЕТ (только позитивные) | ДА (поддерживает) | НЕТ |
| Time segments | ДА | НЕТ (последовательные действия) | НЕТ |
| Motion Brush | НЕТ | ДА (уникальная фича) | ДА |

### Когда что использовать

**Seedance 2.0 (основной):**
- Все кадры с AI-агентами (Pixar-стиль)
- Кадры с тонкой мимикой и жестами
- Когда нужна консистентность персонажа через @Image
- Когда нужны time segments (длинные кадры 10-15 сек)

**Kling 3.0 (запасной):**
- Если Seedance дает артефакты на конкретном кадре
- Когда нужен Motion Brush (точечная анимация элемента)
- Для более "органичного" движения людей
- Когда нужен быстрый дешевый тест

**Runway Gen-4 (эксперименты):**
- Для реалистичных кадров с Юрием (фото -> видео)
- Когда нужен кинематографический look
- Для сложных камерных движений
- Motion Brush для точечного контроля

---

## 8. Готовые шаблоны для AI_SHOW

### Шаблон A: Персонаж-агент говорит / реагирует

```
@Image1 as the first frame. [CHARACTER_NAME], a stylized Pixar-style
AI robot character in [OUTFIT], [ACTION — one specific gesture or
expression change]. [SETTING — modern Dubai office, floor-to-ceiling
windows]. Warm golden afternoon lighting, soft shadows.
Camera: medium close-up, slow push-in, eye level.
Warm Pixar-style 3D animation, consistent character design.
Clear facial features, stable face, no distortion.
Natural and fluid motion, smooth stable footage. 4K.
```

**Пример заполнения:**
```
@Image1 as the first frame. Klodische, a stylized Pixar-style AI robot
character in a navy business suit, slowly nods while a confident smile
forms on his face. His right hand rises in a subtle explanatory gesture.
Modern Dubai office with floor-to-ceiling windows showing city skyline.
Warm golden afternoon lighting through windows, soft shadows on desk.
Camera: medium close-up, slow push-in, eye level.
Warm Pixar-style 3D animation, consistent character design.
Clear facial features, stable face, no distortion.
Natural and fluid motion, smooth stable footage. 4K.
```

### Шаблон B: Реальный Юрий в кадре

```
@Image1 as the first frame. A real man in his 50s with short gray beard
and glasses, [ACTION]. [SETTING]. Natural warm lighting.
Camera: [CAMERA MOVEMENT], eye level.
Photorealistic quality, natural skin tones, sharp details.
Clear facial features, stable face, no distortion.
Natural and fluid motion, smooth stable footage. 4K.
```

**Пример заполнения:**
```
@Image1 as the first frame. A real man in his 50s with short gray beard
and glasses, leans forward slightly and gestures with his right hand
while speaking. Modern minimalist office with warm wood desk and
large monitor showing charts. Natural warm afternoon lighting from
the left, soft fill light.
Camera: medium shot, gentle push-in, eye level.
Photorealistic quality, natural skin tones, sharp details.
Clear facial features, stable face, no distortion.
Natural and fluid motion, smooth stable footage. 4K.
```

### Шаблон C: Двое персонажей в диалоге

```
@Image1 as the first frame. Two characters in a modern office:
[CHAR_A DESCRIPTION] on the left, [CHAR_B DESCRIPTION] on the right.
[CHAR_A ACTION — one gesture]. [CHAR_B REACTION — one response].
[SETTING]. Warm afternoon lighting, soft shadows.
Camera: medium shot, static with subtle dolly, eye level.
Warm Pixar-style 3D animation, consistent character designs.
Clear facial features on both characters, stable faces, no distortion.
Natural and fluid motion, smooth stable footage. 4K.
```

### Шаблон D: Кадр с переходом (time segments, 10-15 сек)

```
@Image1 as the first frame.

0-4s: [SETUP — кто, где, что делает. Camera movement начинается.]
5-9s: [MAIN ACTION — ключевое действие. Camera продолжает.]
10-12s: [RESOLUTION — реакция/завершение. Camera holds.]

Warm Pixar-style 3D animation. Modern Dubai office setting.
Clear facial features, stable face, no distortion, no deformation.
Natural and fluid motion, smooth stable footage. 4K.
```

**Пример заполнения:**
```
@Image1 as the first frame.

0-4s: Medium shot. Klodische sits at desk reviewing holographic data
display. Slight head tilt, reading. Camera: slow push-in begins.
5-9s: Eyes widen with realization. Turns to face camera, confident
smile forming. Right hand rises in "eureka" gesture. Push-in continues.
10-12s: Nods firmly, settles back. Holographic display pulses green
(success). Camera holds. Warm golden afternoon light.

Warm Pixar-style 3D animation, consistent character design.
Clear facial features, stable face, no distortion.
Natural and fluid motion, smooth stable footage. 4K.
```

### Шаблон E: Атмосферный establishing shot

```
@Image1 as the first frame. [WIDE SCENE DESCRIPTION].
[ENVIRONMENTAL MOVEMENT — clouds, light, particles].
No characters in frame. [SETTING DETAILS].
Camera: wide shot, slow [pan/pull-back/crane-up], smooth.
Warm Pixar-style 3D animation, rich environment detail.
Cinematic quality, soft lighting, no flickering. 4K.
```

---

## 9. Промпт-формулы для Kling (когда Seedance не справился)

### Структура Kling (отличия от Seedance)

```
[Scene context from image] → [Specific motion emerging from image] → [Camera behavior]
```

**Правило Kling:** Image уже задает сцену. Промпт описывает ТОЛЬКО что МЕНЯЕТСЯ.

### Шаблон Kling для нашего стиля

```
The character slowly [ACTION]. [One environmental detail animates].
Camera: [one movement]. Maintain character identity and proportions.
Gentle, smooth motion. Keep consistent animation style.
```

**Пример:**
```
The robot character slowly nods and raises right hand in a subtle
explaining gesture. Light through windows shifts warmly.
Camera: slow push-in, steady. Maintain character identity,
keep proportions. Gentle, smooth, natural motion.
```

### Negative prompt для Kling (ПОДДЕРЖИВАЕТСЯ!)

```
distortion, deformation, extra limbs, morphing, flickering,
face change, style change, blurry, ghosting, jitter,
extra characters, text overlay, watermark
```

---

## 10. Промпт-формулы для Runway Gen-4 (для Юрий-реал кадров)

### Структура Runway

```
[Subject action — precise active verb] + [Scene detail] + [Camera movement] + [Visual style]
```

**Правила Runway Gen-4:**
1. Начинать с простого промпта, усложнять итеративно
2. НЕ описывать внешность при img2vid — только ДЕЙСТВИЕ
3. Один глагол на предложение
4. НЕТ negative prompts — только позитивные описания
5. Простые действия = 5 сек, сложные = 10 сек

### Шаблон Runway для реальных кадров

```
The man leans forward slightly, gesturing with his right hand while
speaking. Warm natural light. Camera tracks in gently.
Cinematic, photorealistic.
```

---

## 11. Чек-лист перед генерацией

```
[ ] Промпт 50-150 слов (не менее 30, не более 200)
[ ] Одно действие на кадр
[ ] Одно движение камеры
[ ] Максимум 2 персонажа
[ ] Constraint-блок в конце
[ ] @Image1 reference привязан
[ ] Time segments для клипов >10 сек
[ ] Никаких "beautiful/cool/amazing"
[ ] Позитивная формулировка (не "don't")
[ ] Конкретный глагол действия (не "moves")
[ ] Указан shot size (close-up/medium/wide)
[ ] Указан свет и атмосфера
```

---

## Источники

- [Seedance 2.0 Prompt Template (WaveSpeed)](https://wavespeed.ai/blog/posts/blog-seedance-2-0-prompt-template/)
- [18 Seedance 2.0 Prompts (Dreamina Official)](https://dreamina.capcut.com/resource/seedance-2-0-prompt)
- [Seedance 2.0 Prompt Guide (SeaArt)](https://www.seaart.ai/blog/seedance-2-0-prompt)
- [Seedance 2.0 Camera Movement Cheat Sheet (PromeAI)](https://www.promeai.pro/blog/2026/02/11/seedance-2-0-camera-movement-cheat-sheet/)
- [Awesome Seedance 2 Prompts (GitHub)](https://github.com/YouMind-OpenLab/awesome-seedance-2-prompts)
- [Seedance 2.0 Prompt Guide (Imagine.art)](https://www.imagine.art/blogs/seedance-2-0-prompt-guide)
- [Seedance 2.0 Prompt Tips: Motion-Focused (z-image.ai)](https://z-image.ai/blog/seedance-2-0-prompt-tips-motion)
- [Seedance vs Kling Comparison](https://seedancevideo.com/vs-kling/)
- [Seedance vs Runway Comparison](https://www.seedance.tv/blog/seedance-vs-runway)
- [Kling 3.0 Prompting Guide (fal.ai)](https://blog.fal.ai/kling-3-0-prompting-guide/)
- [Hidden Secrets of Kling AI (InVideo)](https://invideo.io/blog/hidden-secrets-of-kling-ai/)
- [Kling AI Prompts Guide (VEED)](https://www.veed.io/learn/kling-ai-prompting-guide)
- [Gen-4 Video Prompting Guide (Runway Official)](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide)
- [Gen-4 Image References (Runway Official)](https://help.runwayml.com/hc/en-us/articles/40042718905875-Creating-with-Gen-4-Image-References)
- [Runway Gen-4 Prompts (FilmArt)](https://filmart.ai/runway-gen-4-prompts/)
- [Img2Vid Prompts (GitHub)](https://github.com/yanis112/Img2Vid-Prompts)
- [AI Video Prompt Engineering Guide (Bonega)](https://bonega.ai/en/blog/ai-video-prompt-engineering-guide-2025)
- [Best AI Image to Video Prompts (InVideo)](https://invideo.io/blog/best-prompts-for-ai-image-to-video/)
- [AI Video Prompt Guide (LTX Studio)](https://ltx.studio/blog/ai-video-prompt-guide)
- [Seedance 2.0 Guide (Freepik)](https://www.freepik.com/blog/how-to-write-prompts-for-seedance-2-0/)
- [AI Video Model Comparison 2026 (RizzGen)](https://rizzgen.ai/blogs/runway-kling-veo-sora-ltx-wan-seedance-comparison)
- [Seedance vs Top Generators (AI.cc)](https://www.ai.cc/blogs/seedance-2-vs-top-ai-video-generators-2026/)

---
*Правка: обновить по мере тестирования реальных генераций*
