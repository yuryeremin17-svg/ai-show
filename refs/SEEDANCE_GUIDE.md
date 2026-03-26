# Seedance 2.0 — Справочник для AI_SHOW

> Статус: Доступен в ОАЭ через Dreamina (dreamina.capcut.com) и CapCut (веб-версия)
> Обновлено: 26 марта 2026

## Формула промптов

**Subject + Action + Setting + Lighting + Camera Language + Style + Quality + Constraints**

## Обязательные constraint-фразы (в конец КАЖДОГО промпта)

**Персонаж:**
```
Clear facial features, stable face, no distortion, no deformation. Normal body proportions, natural structure, no stiffness. Same character, consistent clothing, unchanged hairstyle.
```

**Качество + Движение (всегда):**
```
4K ultra-high definition, rich details, sharp resolution. Cinematic quality, natural colors, soft lighting. No blur, no ghosting, no flickering, stable footage. Natural and fluid motion, smooth and stable footage. Silky smooth camera movement, no jitter.
```

## Система @-ссылок

| Паттерн | Что делает |
|---------|-----------|
| `@Image1 as the first frame` | Фиксирует первый кадр |
| `reference @Video1 for camera movement` | Берёт только камеру |
| `@Image1 performs the dance from @Video1` | Персонаж + движение |
| `Extend @Video1 by 5s` | Продление (длительность = только новое) |
| `Replace [char] in @Video1 with @Image1` | Замена персонажа |
| `use @Audio1 for background music` | Аудио напрямую |
| `reference @Video1's voice timbre` | Клон голоса |

## Time Segments (обязательно для >10 сек)

```
0-3s: [сцена]
4-8s: [сцена]
9-12s: [сцена]
13-15s: [закрытие]
```

## Настройки

- Формат: 16:9, 9:16, 1:1, 4:3, 3:4
- Длительность: 4-15 сек за генерацию
- Референс-картинок: до 6
- Референс-видео: до 6 (суммарно ≤15 сек)

## Язык действий

**Используй:** slow, gentle, continuous, natural, fluid, smooth
**НЕ используй:** exaggerated, high-speed, extreme, "beautiful", "cool", "amazing"

## Шаблон для AI Office (Pixar-стиль)

```
[Scene description]. [Character action — slow, natural]. [Setting — modern office, Dubai skyline]. Warm golden afternoon lighting through floor-to-ceiling windows. [Camera — slow push-in / pull-back / orbit]. Warm stylized Pixar-style illustration. Clear facial features, stable face, no distortion. 4K ultra-high definition, rich details, cinematic quality. Natural and fluid motion, smooth stable footage.
```

## Модули документации

| Задача | Модуль |
|--------|--------|
| Камера, движение | 02_camera-motion.md |
| Консистентность персонажей | 03_character-consistency.md |
| Голос, lip-sync | 09_audio-lipsync.md |
| Монтаж, эффекты | 04_editing-effects.md |
| Продление видео | 05_video-extension.md |
| Реклама | 06_commercial-ads.md |
| One-take, нарратив | 07_one-take-storytelling.md |
| Шаблоны промптов | 01_prompt-templates.md |
| Паттерны комьюнити | 08_community-patterns.md |

## Где открыть (когда станет доступно)

| Платформа | URL | Примечание |
|-----------|-----|-----------|
| Dreamina | dreamina.capcut.com | Доступен в ОАЭ (веб) |
| CapCut | capcut.com | Доступен в ОАЭ (веб) |
| fal.ai | fal.ai/seedance-2.0 | API |

## Связь с пайплайном AI_SHOW

```
ТЕКУЩИЙ:  scenario → Midjourney (картинки) → Seedance/Dreamina (img2vid) → ElevenLabs → assemble.py
АЛЬТ:     scenario → Dreamina (картинки + видео в одном) → ElevenLabs → assemble.py
```

---
*Источник: 11 документов Seedance 2.0 (SYSTEM_PROMPT + модули 00-09 + community prompts)*
