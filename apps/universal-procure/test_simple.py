#!/usr/bin/env python3
"""
Простой тест парсера без pytest
"""

import sys
from pathlib import Path

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, str(Path(__file__).parent))

from parser.ru_nlq import NLQParser

def test_parser():
    """Простой тест парсера"""
    
    print("🧪 Тестирование парсера естественного языка")
    print("=" * 60)
    
    parser = NLQParser()
    
    # Тест 1: Бумага А4 Москва
    print("\n📝 Тест 1: 'бумага А4 офисная Москва до 200 тыс руб'")
    query1 = "бумага А4 офисная Москва до 200 тыс руб"
    result1 = parser.parse(query1)
    
    print(f"   ОКПД2: {result1['okpd2']}")
    print(f"   Регион: {result1['region']}")
    print(f"   Цена до: {result1['price_max']}")
    print(f"   Диагностика: {result1['diagnostics']}")
    
    # Проверяем результаты
    success1 = (
        "17.23.13.110" in result1["okpd2"] and
        "Город Москва" in result1["region"] and
        result1["price_max"] == 200000
    )
    print(f"   ✅ Успех: {success1}")
    
    # Тест 2: Строительство дорог Крым
    print("\n📝 Тест 2: 'услуги по строительству дорог Крым от 5 до 20 млн'")
    query2 = "услуги по строительству дорог Крым от 5 до 20 млн"
    result2 = parser.parse(query2)
    
    print(f"   ОКПД2: {result2['okpd2']}")
    print(f"   Регион: {result2['region']}")
    print(f"   Цена от: {result2['price_min']}")
    print(f"   Цена до: {result2['price_max']}")
    print(f"   Диагностика: {result2['diagnostics']}")
    
    # Проверяем результаты
    success2 = (
        "42.11.*" in result2["okpd2"] and
        "Республика Крым" in result2["region"] and
        result2["price_min"] == 5000000 and
        result2["price_max"] == 20000000
    )
    print(f"   ✅ Успех: {success2}")
    
    # Тест 3: Медицинское оборудование Москва конкурс
    print("\n📝 Тест 3: 'поставка медоборудования Москва конкурс'")
    query3 = "поставка медоборудования Москва конкурс"
    result3 = parser.parse(query3)
    
    print(f"   ОКПД2: {result3['okpd2']}")
    print(f"   Регион: {result3['region']}")
    print(f"   Метод: {result3['method']}")
    print(f"   Диагностика: {result3['diagnostics']}")
    
    # Проверяем результаты
    success3 = (
        "26.60.*" in result3["okpd2"] and
        "Город Москва" in result3["region"] and
        "конкурс" in result3["method"]
    )
    print(f"   ✅ Успех: {success3}")
    
    # Тест 4: Электромонтаж СПб новые за неделю
    print("\n📝 Тест 4: 'электромонтажные работы до 3 млн руб Санкт-Петербург новые за неделю'")
    query4 = "электромонтажные работы до 3 млн руб Санкт-Петербург новые за неделю"
    result4 = parser.parse(query4)
    
    print(f"   ОКПД2: {result4['okpd2']}")
    print(f"   Регион: {result4['region']}")
    print(f"   Цена до: {result4['price_max']}")
    print(f"   Публикация с: {result4['publish_date_from']}")
    print(f"   Диагностика: {result4['diagnostics']}")
    
    # Проверяем результаты
    success4 = (
        "43.21.*" in result4["okpd2"] and
        "Город Санкт-Петербург" in result4["region"] and
        result4["price_max"] == 3000000 and
        result4["publish_date_from"] is not None
    )
    print(f"   ✅ Успех: {success4}")
    
    # Итоги
    print("\n" + "=" * 60)
    print("📊 Итоги тестирования:")
    print(f"   Тест 1: {'✅ ПРОЙДЕН' if success1 else '❌ ПРОВАЛЕН'}")
    print(f"   Тест 2: {'✅ ПРОЙДЕН' if success2 else '❌ ПРОВАЛЕН'}")
    print(f"   Тест 3: {'✅ ПРОЙДЕН' if success3 else '❌ ПРОВАЛЕН'}")
    print(f"   Тест 4: {'✅ ПРОЙДЕН' if success4 else '❌ ПРОВАЛЕН'}")
    
    total_success = sum([success1, success2, success3, success4])
    print(f"\n🎯 Общий результат: {total_success}/4 тестов пройдено")
    
    if total_success == 4:
        print("🎉 Все тесты пройдены успешно!")
    else:
        print("⚠️  Некоторые тесты не пройдены. Проверьте логи выше.")

if __name__ == "__main__":
    test_parser()
