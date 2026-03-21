# S01E01 — Готовые промпты для Midjourney (Discord)

> Копируй каждый промпт в Discord-бот Midjourney.
> Выбери лучший из 4-х вариантов → Upscale → скачай → сохрани как `01.png`, `02.png`, ... `10.png` сюда.
> После всех 10 кадров: `python3 scripts/assemble.py S01E01`

## Мастер-образы (CREF)

| Персонаж | URL |
|----------|-----|
| Юрий | https://cdn.midjourney.com/82c8efac-5016-4808-8f14-aa25a10dd536/0_0.png |
| Клодище | https://cdn.midjourney.com/98ee8ef2-6e52-4899-b0fb-6613088d6302/0_2.png |
| Today | https://cdn.midjourney.com/736231e0-530b-4fcb-bf3c-538be3c68156/0_0.png |

---

## КАДР 1 — ЗАЦЕПКА (01.png)
```
stylized warm illustration, close-up laptop screen showing messy presentation with misaligned tables and clashing colors, man's hand hovering over keyboard, warm office lighting, Dubai skyline through window --ar 9:16
```
> Без CREF — крупный план экрана.

---

## КАДР 2 — КОНТЕКСТ (02.png)
```
stylized warm illustration, confident Mediterranean man late 50s with curly grey-streaked dark hair in blue shirt at modern desk, slight smirk, coffee cup in hand, messy presentation on screen behind him, Dubai skyline, Pixar-style --ar 9:16 --cref https://cdn.midjourney.com/82c8efac-5016-4808-8f14-aa25a10dd536/0_0.png
```
> CREF: Юрий

---

## КАДР 3 — ЗАПРОС (03.png)
```
stylized warm illustration, Mediterranean man late 50s with curly grey-streaked hair in blue shirt typing on laptop at desk, beside him tall thin man in black turtleneck sweater with round glasses adjusting spectacles, modern bright office, Pixar-style --ar 9:16 --cref https://cdn.midjourney.com/82c8efac-5016-4808-8f14-aa25a10dd536/0_0.png https://cdn.midjourney.com/98ee8ef2-6e52-4899-b0fb-6613088d6302/0_2.png
```
> CREF: Юрий + Клодище

---

## КАДР 4 — ОТКАЗ (04.png)
```
stylized warm illustration, tall thin man in black turtleneck with round glasses standing with arms crossed serious expression, thought bubble showing silhouette of designer with palette, Mediterranean man in blue shirt raising eyebrow, office setting, Pixar-style --ar 9:16 --cref https://cdn.midjourney.com/82c8efac-5016-4808-8f14-aa25a10dd536/0_0.png https://cdn.midjourney.com/98ee8ef2-6e52-4899-b0fb-6613088d6302/0_2.png
```
> CREF: Юрий + Клодище

---

## КАДР 5 — ПАУЗА (05.png)
```
stylized warm illustration, Mediterranean man late 50s with curly grey-streaked hair in blue shirt leaning back in office chair, semi-transparent memory scene showing employee shrugging with papers labeled contractor needed, warm nostalgic lighting, Pixar-style --ar 9:16 --cref https://cdn.midjourney.com/82c8efac-5016-4808-8f14-aa25a10dd536/0_0.png
```
> CREF: Юрий

---

## КАДР 6 — ДРУГОЙ ВОПРОС (06.png)
```
stylized warm illustration, Mediterranean man late 50s in blue shirt leaning forward pointing at screen with determined expression, tall thin man in black turtleneck with round glasses stepping back slightly surprised, dynamic office scene, Pixar-style --ar 9:16 --cref https://cdn.midjourney.com/82c8efac-5016-4808-8f14-aa25a10dd536/0_0.png https://cdn.midjourney.com/98ee8ef2-6e52-4899-b0fb-6613088d6302/0_2.png
```
> CREF: Юрий + Клодище

---

## КАДР 7 — ТРИ РЕШЕНИЯ (07.png)
```
stylized warm illustration, tall thin man in black turtleneck with round glasses animated and excited, three design options on screen with one highlighted in green, presentation transforming beautifully, dynamic energy, Pixar-style --ar 9:16 --cref https://cdn.midjourney.com/98ee8ef2-6e52-4899-b0fb-6613088d6302/0_2.png
```
> CREF: Клодище

---

## КАДР 8 — РАЗОБЛАЧЕНИЕ (08.png)
```
stylized warm illustration, Mediterranean man late 50s in blue shirt with arms crossed and knowing smirk facing tall thin man in black turtleneck with round glasses who has guilty half-smile, warm office lighting, humorous moment, Pixar-style --ar 9:16 --cref https://cdn.midjourney.com/82c8efac-5016-4808-8f14-aa25a10dd536/0_0.png https://cdn.midjourney.com/98ee8ef2-6e52-4899-b0fb-6613088d6302/0_2.png
```
> CREF: Юрий + Клодище

---

## КАДР 9 — ИНСАЙТ (09.png)
```
stylized warm illustration, split screen comparison, left side shows question bubble what do you think with hesitant tall thin man in black turtleneck, right side shows give 3 solutions with energetic confident same man, arrow between them, clean infographic style, Pixar-style --ar 9:16 --cref https://cdn.midjourney.com/98ee8ef2-6e52-4899-b0fb-6613088d6302/0_2.png
```
> CREF: Клодище

---

## КАДР 10 — ФИНАЛ (10.png)
```
stylized warm illustration, Mediterranean man late 50s with curly grey-streaked hair in blue shirt at desk with coffee, beautiful finished presentation on laptop, stylish young woman with dark hair in bun and muted green blouse in doorway with tablet and knowing smile, tall thin man in black turtleneck working in background, warm golden hour lighting, Dubai skyline, Pixar-style --ar 9:16 --cref https://cdn.midjourney.com/82c8efac-5016-4808-8f14-aa25a10dd536/0_0.png https://cdn.midjourney.com/98ee8ef2-6e52-4899-b0fb-6613088d6302/0_2.png https://cdn.midjourney.com/736231e0-530b-4fcb-bf3c-538be3c68156/0_0.png
```
> CREF: Юрий + Клодище + Today

---

## Чек-лист после генерации

- [ ] Все 10 файлов в `assets/scenes/S01E01/` (01.png — 10.png)
- [ ] Персонажи узнаваемы и консистентны между кадрами
- [ ] Формат 9:16 (вертикальное видео)
- [ ] Кадр 8 (ключевой) — самый выразительный
- [ ] Today в кадре 10 — в дверях, на заднем плане
