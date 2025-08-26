#!/usr/bin/env python3
"""
Отладка парсера естественного языка
"""

import sys
from pathlib import Path

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, str(Path(__file__).parent))

from parser.ru_nlq import NLQParser

def debug_parser():
    """Отладка работы парсера"""
    
    print("🔍 Отладка парсера естественного языка")
    print("=" * 60)
    
    parser = NLQParser()
    
    # Тестовый запрос
    query = "бумага А4 офисная Москва до 200 тыс руб"
    print(f"📝 Запрос: {query}")
    
    # Проверяем нормализацию
    normalized = parser._normalize_text(query)
    print(f"📝 Нормализованный: {normalized}")
    
    # Проверяем лемматизацию
    lemmatized = parser._lemmatize_text(normalized)
    print(f"📝 Лемматизированный: {lemmatized}")
    
    # Проверяем справочники
    print(f"\n📚 Справочник ОКПД2 (первые 5 ключей):")
    for i, (key, value) in enumerate(parser.okpd2_dict.items()):
        if i >= 5:
            break
        print(f"   {key}: {value}")
    
    print(f"\n📚 Справочник регионов (первые 5):")
    for i, region in enumerate(parser.regions_dict):
        if i >= 5:
            break
        print(f"   {region['canonical']}: {region['aliases']}")
    
    # Парсим запрос
    print(f"\n🔍 Результат парсинга:")
    result = parser.parse(query)
    
    print(f"   ОКПД2: {result['okpd2']}")
    print(f"   Регион: {result['region']}")
    print(f"   Цена до: {result['price_max']}")
    print(f"   Диагностика: {result['diagnostics']}")
    
    # Проверяем поиск ключевых слов
    print(f"\n🔍 Поиск ключевых слов:")
    for keyword, okpd2_codes in parser.okpd2_dict.items():
        if keyword in lemmatized:
            print(f"   Найдено: {keyword} -> {okpd2_codes}")
    
    # Проверяем поиск регионов
    print(f"\n🔍 Поиск регионов:")
    for region_info in parser.regions_dict:
        canonical = region_info["canonical"]
        aliases = region_info["aliases"]
        
        if canonical.lower() in lemmatized:
            print(f"   Найдено каноническое: {canonical}")
        
        for alias in aliases:
            if alias.lower() in lemmatized:
                print(f"   Найдено по синониму: {alias} -> {canonical}")

if __name__ == "__main__":
    debug_parser()
