# Правила парсинга дат и временных периодов

## Относительные периоды

### "За X дней/неделю/месяц"
- "за 3 дня" → `publish_date_from = today - 3`
- "за неделю" → `publish_date_from = today - 7`
- "за месяц" → `publish_date_from = today - 30`
- "за год" → `publish_date_from = today - 365`

### "На следующей неделе"
- "на следующей неделе" → `deadline_from = next_monday`, `deadline_to = next_sunday`
- "в следующем месяце" → `deadline_from = next_month_start`, `deadline_to = next_month_end`

### "Завтра/послезавтра/через N дней"
- "завтра" → `deadline_date = today + 1`
- "послезавтра" → `deadline_date = today + 2`
- "через 5 дней" → `deadline_date = today + 5`

## Абсолютные даты

### Форматы дат
- "до 30.09" → `deadline_date <= 30.09.current_year`
- "с 01.10 по 15.10" → `deadline_from = 01.10.current_year`, `deadline_to = 15.10.current_year`
- "с 01.01.2025 по 31.12.2025" → `deadline_from = 01.01.2025`, `deadline_to = 31.12.2025`

### Сезонные периоды
- "в этом году" → `deadline_from = 01.01.current_year`, `deadline_to = 31.12.current_year`
- "в следующем году" → `deadline_from = 01.01.next_year`, `deadline_to = 31.12.next_year`

## Временные окна по умолчанию

### Ключевые слова
- "новые" → `publish_date_from = today - 7d` (по умолчанию)
- "актуальные" → `publish_date_from = today - 30d`
- "текущие" → `publish_date_from = today - 90d`

### Без уточнений
- Если временные рамки не указаны → не ставить жёстких ограничений
- Использовать разумные значения по умолчанию для поиска

## Алгоритм парсинга

1. **Приоритет 1**: Абсолютные даты (если указаны)
2. **Приоритет 2**: Относительные периоды от текущей даты
3. **Приоритет 3**: Ключевые слова с дефолтными значениями
4. **Приоритет 4**: Без ограничений по времени

## Примеры

```
"новые закупки за неделю" → publish_date_from = today - 7
"дедлайн на следующей неделе" → deadline_from = next_monday, deadline_to = next_sunday
"с 01.10 по 15.10" → deadline_from = 01.10.current_year, deadline_to = 15.10.current_year
"через 3 дня" → deadline_date = today + 3
```
