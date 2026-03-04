#!/bin/bash
# Скилл: /scenario — Сценарист видеосериала AI Office
# Путь: AI_SHOW/skills/scenario/run.sh
# Версия: 1.0
# Использование: bash skills/scenario/run.sh "история или тема"
# Опции: --lang ru|en|both --duration short|long

SHOW_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
OFFICE_DIR="$HOME/Documents/WORK/AI_OFFICE"
TODAY=$(date +%Y-%m-%d)
REPORT_DIR="$SHOW_DIR/scripts"

# === Параметры по умолчанию ===
LANG="ru"
DURATION="short"
STORY=""
MODEL="sonnet"

# === Парсинг аргументов ===
while [[ $# -gt 0 ]]; do
    case $1 in
        --lang) LANG="$2"; shift 2 ;;
        --duration) DURATION="$2"; shift 2 ;;
        *) STORY="$1"; shift ;;
    esac
done

if [ -z "$STORY" ]; then
    printf "Ошибка: укажи историю или тему для серии.\n"
    printf "Пример: bash skills/scenario/run.sh \"Обратитесь к дизайнеру\"\n"
    printf "\n"
    printf "Опции:\n"
    printf "  --lang ru|en|both       (по умолчанию: ru)\n"
    printf "  --duration short|long   (short=2мин, long=3мин, по умолчанию: short)\n"
    exit 1
fi

# === Хронометраж ===
if [ "$DURATION" = "long" ]; then
    DURATION_TEXT="2.5-3 минуты (~400-450 слов), 10-12 кадров"
else
    DURATION_TEXT="2-2.5 минуты (~300-350 слов), 8-10 кадров"
fi

# === Определяем следующий номер серии ===
LAST_EP=$(ls "$REPORT_DIR"/S01E*_ru.md 2>/dev/null | sort | tail -1 | grep -oE 'E[0-9]+' | grep -oE '[0-9]+')
if [ -z "$LAST_EP" ]; then
    NEXT_EP="01"
else
    NEXT_EP=$(printf "%02d" $((10#$LAST_EP + 1)))
fi

# === Загрузка контекста ===
MY_STORIES="$OFFICE_DIR/refs/MY_STORIES.md"
SERIES_BIBLE="$SHOW_DIR/SERIES_BIBLE.md"

if [ ! -f "$MY_STORIES" ]; then
    printf "ПРЕДУПРЕЖДЕНИЕ: MY_STORIES.md не найден: %s\n" "$MY_STORIES" >&2
fi

if [ ! -f "$SERIES_BIBLE" ]; then
    printf "Ошибка: SERIES_BIBLE.md не найден: %s\n" "$SERIES_BIBLE" >&2
    exit 1
fi

# Извлекаем персонажей и формат из библии (секции)
BIBLE_CONTENT=$(cat "$SERIES_BIBLE")

# Извлекаем историю из MY_STORIES если передано название
STORY_CONTEXT=""
if [ -f "$MY_STORIES" ]; then
    # Ищем секцию с похожим названием
    STORY_CONTEXT=$(cat "$MY_STORIES")
fi

# === Формирование промпта через файл (ERRORS.md #2) ===
PROMPT_FILE=$(mktemp)
trap 'rm -f "$PROMPT_FILE"' EXIT

# Часть с переменными
cat > "$PROMPT_FILE" <<BLOCK
Ты — режиссёр-сценарист мини-сериала "AI Office".

ЗАДАЧА: Написать раскадровку для видеосерии на основе истории: "${STORY}"

ХРОНОМЕТРАЖ: ${DURATION_TEXT}

ЯЗЫК: ${LANG}

НОМЕР СЕРИИ: S01E${NEXT_EP}

BLOCK

# Часть без переменных (безопасная для спецсимволов)
cat >> "$PROMPT_FILE" <<'BLOCK'
БИБЛИЯ СЕРИАЛА (обязательно следовать):
BLOCK

cat "$SERIES_BIBLE" >> "$PROMPT_FILE"

cat >> "$PROMPT_FILE" <<'BLOCK'

---

БАНК ИСТОРИЙ (источник фактов):
BLOCK

if [ -f "$MY_STORIES" ]; then
    cat "$MY_STORIES" >> "$PROMPT_FILE"
fi

cat >> "$PROMPT_FILE" <<'BLOCK'

---

ИНСТРУКЦИИ:

1. Найди указанную историю в банке историй. Если не нашёл — используй текст как свободную тему.

2. Напиши раскадровку СТРОГО по формату:

# S01E[XX] — "Название серии"
> Инсайт: [одно предложение]
> Хронометраж: ~[X:XX]
> Источник: MY_STORIES.md / [секция] или "свободная тема"
> Персонажи: [кто появляется]

---

Далее кадры по структуре:
- КАДР 1 — ЗАЦЕПКА [0:00-0:05]
- КАДР 2-3 — КОНТЕКСТ [0:05-0:20]
- КАДР 4-6 — СИТУАЦИЯ [0:20-1:00]
- КАДР 7-8 — ПОВОРОТ [1:00-1:30]
- КАДР 9-10 — ИНСАЙТ [1:30-2:20]
- КАДР 11-12 — ФИНАЛ [2:20-2:40]

Каждый кадр:
```
## КАДР N — НАЗВАНИЕ [таймкод]
ВИЗУАЛ: [что видит зритель — место, персонаж, действие, эмоция]
ГОЛОС: "[точный текст озвучки в кавычках]"
НАСТРОЕНИЕ: [одно слово]
MIDJOURNEY: stylized warm illustration, [описание сцены], [персонаж по библии] --ar 9:16
```

3. После кадров добавь:

## Текст озвучки (цельный)
[Весь текст ГОЛОС подряд одним куском — для записи. Без номеров кадров, без пауз-маркеров кроме "..." для естественных пауз]

## Заметки для продакшена
- Ключевой кадр: [номер и почему]
- Настроение музыки: [описание]
- Переходы: [рекомендация]

4. ПРАВИЛА:
- Зацепка с ПЕРВОЙ секунды. Не "Привет" и не "Сегодня расскажу". Сразу в ситуацию.
- Диалоги — ДОСЛОВНО из истории если есть. Живые диалоги > пересказ.
- ОДИН инсайт. Если два — скажи и предложи разбить.
- Юмор ОБЯЗАТЕЛЕН. Самоирония, абсурд ситуации, узнавание.
- Финал = вопрос к зрителю или крючок. Не точка.
- Тон: как рассказываешь другу за кофе. Не со сцены.
- Метафоры из физического мира (принтер, экскаватор, лупа).
- Крепкое словцо допустимо — редко и метко.
- Персонажи — по описаниям из библии. Midjourney-промпты консистентные.
- НЕ ВЫДУМЫВАТЬ факты, диалоги, события. Только из банка историй.

5. ВЕРИФИКАЦИЯ (в конце):
- Зацепка в первые 5 сек? ДА/НЕТ
- Поворот есть? ДА/НЕТ
- Один инсайт? ДА/НЕТ
- Юмор есть? ДА/НЕТ
- Факты из MY_STORIES? ДА/НЕТ
- Хронометраж (слов): [число]

Если lang=both — напиши ДВЕ версии: сначала русскую, потом английскую (адаптация, не перевод).
BLOCK

# === Вызов API ===
PROMPT_CONTENT=$(cat "$PROMPT_FILE")

printf "Генерирую раскадровку S01E%s: %s (lang=%s, %s)...\n" "$NEXT_EP" "$STORY" "$LANG" "$DURATION_TEXT"

RESULT=$(cd "$OFFICE_DIR" && python3 -c "
import sys
sys.path.insert(0, '.')
from llm import call_llm
prompt = open('$PROMPT_FILE').read()
result = call_llm(prompt, model='$MODEL')
print(result)
")

# === Проверка результата ===
if printf '%s' "$RESULT" | grep -qi "rate limit\|error\|overloaded"; then
    printf "ОШИБКА API: %s\n" "$RESULT" >&2
    exit 1
fi

# === Сохранение ===
if [ "$LANG" = "both" ]; then
    # Разделяем на ru и en версии
    printf '%s' "$RESULT" > "$REPORT_DIR/S01E${NEXT_EP}_full.md"
    printf "Раскадровка сохранена: %s/S01E%s_full.md\n" "$REPORT_DIR" "$NEXT_EP"
else
    printf '%s' "$RESULT" > "$REPORT_DIR/S01E${NEXT_EP}_${LANG}.md"
    printf "Раскадровка сохранена: %s/S01E%s_%s.md\n" "$REPORT_DIR" "$NEXT_EP" "$LANG"
fi

printf "Готово.\n"
