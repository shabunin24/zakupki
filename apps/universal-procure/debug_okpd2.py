#!/usr/bin/env python3
"""
Отладка поиска ОКПД2
"""

import sys
from pathlib import Path

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, str(Path(__file__).parent))

from parser.ru_nlq import NLQParser

def debug_okpd2():
    """Отладка поиска ОКПД2"""
    
    print("🔍 Отладка поиска ОКПД2")
    print("=" * 60)
    
    parser = NLQParser()
    
    # Тестовый запрос
    query = "услуги по строительству дорог Крым от 5 до 20 млн"
    normalized = parser._normalize_text(query)
    lemmatized = parser._lemmatize_text(normalized)
    
    print(f"📝 Запрос: {query}")
    print(f"📝 Нормализованный: {normalized}")
    print(f"📝 Лемматизированный: {lemmatized}")
    
    # Проверяем поиск ключевых слов
    print(f"\n🔍 Поиск ключевых слов:")
    for keyword, okpd2_codes in parser.okpd2_dict.items():
        if keyword in lemmatized:
            print(f"   Найдено: {keyword} -> {okpd2_codes}")
    
    # Проверяем поиск по частям
    print(f"\n🔍 Поиск по частям:")
    words = lemmatized.split()
    for word in words:
        for keyword, okpd2_codes in parser.okpd2_dict.items():
            if word in keyword or keyword in word:
                print(f"   Слово '{word}' частично совпадает с '{keyword}' -> {okpd2_codes}")
    
    # Проверяем конкретные ключевые слова
    print(f"\n🔍 Проверка конкретных ключевых слов:")
    test_keywords = ["строительство дорог", "дороги", "строительство"]
    for keyword in test_keywords:
        if keyword in parser.okpd2_dict:
            print(f"   '{keyword}' найден: {parser.okpd2_dict[keyword]}")
        else:
            print(f"   '{keyword}' НЕ найден")
    
    # Парсим запрос
    print(f"\n🔍 Результат парсинга:")
    result = parser.parse(query)
    print(f"   ОКПД2: {result['okpd2']}")
    print(f"   Диагностика: {result['diagnostics']}")

if __name__ == "__main__":
    debug_okpd2()
