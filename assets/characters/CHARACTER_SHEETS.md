# Character Sheets — промпты для дополнительных ракурсов

> Генерация: Midjourney (веб-версия)
> Метод: загрузить мастер-образ как --cref (Character Reference)
> Формат: --ar 1:1
> Цель: 3 ракурса на персонажа (фронт уже есть)

---

## Клодище — профиль (вид сбоку)

```
stylized warm illustration, tall thin intellectual man in black turtleneck sweater with round glasses, side profile view, looking at tablet in his hands, thoughtful expression, neat dark hair, narrow elongated silhouette, warm studio lighting, clean neutral background, Pixar-style character design --ar 1:1 --cref [claude.png]
```
**Файл:** `masters/claude_profile.png`

---

## Клодище — 3/4 ракурс

```
stylized warm illustration, tall thin intellectual man in black turtleneck sweater with round glasses, three-quarter view slightly turned right, arms crossed with slight smirk, confident pose, narrow elongated silhouette, warm studio lighting, clean neutral background, Pixar-style character design --ar 1:1 --cref [claude.png]
```
**Файл:** `masters/claude_3q.png`

---

## Клодище — эмоция: виноватая улыбка

```
stylized warm illustration, tall thin intellectual man in black turtleneck sweater with round glasses, front view, adjusting glasses nervously with one hand, guilty sheepish half-smile, slightly hunched shoulders, warm studio lighting, clean neutral background, Pixar-style character design --ar 1:1 --cref [claude.png]
```
**Файл:** `masters/claude_guilty.png`

---

## Локация: Офис агентов (environment reference)

```
stylized warm illustration, modern bright open office interior, large windows with Dubai skyline and Burj Khalifa visible outside, warm golden hour lighting, clean desks with monitors and coffee cups, whiteboard with diagrams, potted plants, warm wood and glass materials, cozy but professional atmosphere, no people, empty office ready for characters, Pixar-style environment design --ar 16:9
```
**Файл:** `assets/locations/office_main.png`

---

## Локация: Офис агентов (вертикальный, для шотов 9:16)

```
stylized warm illustration, modern bright office interior corner, large window with Dubai skyline visible, warm golden hour lighting, desk with monitor showing code and charts, coffee cup, stack of books, whiteboard edge visible, warm wood and glass, cozy professional atmosphere, no people, Pixar-style environment design --ar 9:16
```
**Файл:** `assets/locations/office_vertical.png`

---

## Генерация

**Платформа:** midjourney.com → Imagine
**Метод:** загрузить мастер-образ через Character Reference (иконка с человечком), вставить промпт, выбрать лучший из 4 → Upscale → скачать

## Порядок генерации (для S01E01)

**Минимум для первого эпизода:**
1. `claude_profile.png` — нужен для шота 2 (вид сбоку за столом)
2. `claude_3q.png` — нужен для шотов 3-4
3. `claude_guilty.png` — нужен для шота 5 ("перестраховался")
4. `office_main.png` — environment reference для всех мульт-шотов
5. `office_vertical.png` — то же, вертикальный формат

---

*Создано: 27 марта 2026*
