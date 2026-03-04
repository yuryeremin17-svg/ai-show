# Промпты для создания мастер-образов персонажей

> Порядок действий:
> 1. Скопируй промпт в Midjourney (Discord)
> 2. Выбери лучший вариант из 4-х (upscale)
> 3. Скопируй URL картинки сюда (в поле "URL")
> 4. Этот URL потом подставляется как --cref во все раскадровки

> **Принципы дизайна (Pixar-школа):**
> - **Силуэт-тест:** каждый персонаж узнаваем по силуэту за 1 секунду
> - **Свой цвет:** доминирующий цвет = мгновенная идентификация на экране телефона
> - **Характер в позе:** даже без лица — понятно кто это по позе и пропорциям

---

## 1. Юрий — Босс (цвет: тёплый синий)

**ВАЖНО:** Загрузи СВОЁ ФОТО в Midjourney, потом используй его как --cref

```
stylized warm illustration, confident man late 50s, broad shoulders, slight smirk, smart casual blue shirt no tie, sitting at modern desk with laptop, coffee cup nearby, Dubai skyline through window, warm golden lighting, distinctive silhouette, Pixar-style character design --ar 1:1 --cref [ТВОЁ_ФОТО_URL] --cw 70
```

> --cw 70 = сохранит черты лица, но стилизует. Если слишком похож — уменьши до 50. Если не похож — увеличь до 90.

**URL мастер-образа:** _________________

---

## 2. Клодище (Claude) — Зам и архитектор (цвет: чёрный/тёмно-серый)

```
stylized warm illustration, tall thin intellectual character with round glasses, dark black turtleneck sweater, holding tablet with code on screen, thoughtful expression, slightly absent-minded, books stacked nearby, narrow elongated silhouette, Pixar-style character design --ar 1:1
```

**URL мастер-образа:** _________________

---

## 3. Скаут AI — Техно-разведчик (цвет: фиолетовый)

```
stylized warm illustration, young tech geek character in purple hoodie, headphones around neck, hunched over tablet with news feeds and charts, excited wide eyes, laptop with stickers visible, slightly messy hair, compact energetic silhouette, Pixar-style character design --ar 1:1
```

**URL мастер-образа:** _________________

---

## 4. Скаут Biz — Бизнес-разведчик (цвет: голубой)

```
stylized warm illustration, business-savvy character in light blue rolled-up shirt sleeves, holding financial newspaper, coffee cup in other hand, light stubble, focused composed expression, upright confident posture, early morning energy, Pixar-style character design --ar 1:1
```

**URL мастер-образа:** _________________

---

## 5. Контент — Фантазёр (цвет: бордовый/цветной)

```
stylized warm illustration, creative artistic character wearing dark red beret and colorful scarf, holding ornate quill pen, inspired dreamy upward gaze, vintage easel with canvas nearby, paint splashes, expressive wide silhouette, Pixar-style character design --ar 1:1
```

**URL мастер-образа:** _________________

---

## 6. QA — Зануда-перфекционист (цвет: коричневый)

```
stylized warm illustration, short stocky strict character in brown vest over white shirt, red pencil in hand, round glasses on tip of nose, stack of papers with red marks, pursed lips, disapproving but caring expression, wide solid silhouette, Pixar-style character design --ar 1:1
```

**URL мастер-образа:** _________________

---

## 7. Аналитик (Research) — Профессор (цвет: бежевый/твидовый)

```
stylized warm illustration, professor-type character with beige tweed jacket elbow patches, surrounded by towering open books and charts, whiteboard with complex diagrams behind, absorbed in deep thought, slightly disheveled, books extending beyond silhouette, Pixar-style character design --ar 1:1
```

**URL мастер-образа:** _________________

---

## 8. Today — Утренний брифинг (она) (цвет: приглушённый зелёный)

```
stylized warm illustration, stylish young woman with dark hair in neat bun, thin elegant glasses, muted green silk blouse, wristwatch on wrist, holding tablet and leather folder, calm confident expression, slight knowing smile, graceful upright silhouette, morning light, Pixar-style character design --ar 1:1
```

**URL мастер-образа:** _________________

---

## Общий стиль (--sref)

После создания первого персонажа, сохрани URL лучшей картинки и добавляй `--sref [URL]` ко всем остальным промптам — это обеспечит единый стиль.

**URL стиля (--sref):** _________________

---

## Цветовая карта (для быстрой проверки)

| Персонаж | Цвет | Силуэт |
|----------|------|--------|
| Юрий | тёплый синий | широкие плечи, уверенная поза |
| Клодище | чёрный | высокий, узкий, вытянутый |
| Скаут AI | фиолетовый | компактный, сгорбленный над планшетом |
| Скаут Biz | голубой | прямая осанка, газета |
| Контент | бордовый | широкий, берет, мольберт |
| QA | коричневый | приземистый, основательный |
| Аналитик | бежевый | окружён книгами (выходят за контур) |
| Today | зелёный | стройный, аккуратный, планшет |

---

## Советы

- **--ar 1:1** для мастер-образов (портрет). В раскадровках будет --ar 9:16 (вертикальное видео)
- Генерируй 2-3 варианта каждого персонажа, выбирай самый характерный
- Если персонаж не нравится — добавь/убери детали в промпте
- Сохраняй URL сюда — скилл scenario будет подставлять их автоматически
- **Тест:** поставь всех 8 рядом мелко (как на экране телефона) — если различаешь каждого за 1 секунду, дизайн работает

*Обновлено: 4 марта 2026*
