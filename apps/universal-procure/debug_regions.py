#!/usr/bin/env python3
"""
Отладка поиска регионов
"""

import sys
from pathlib import Path

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, str(Path(__file__).parent))

from parser.ru_nlq import NLQParser

def debug_regions():
    """Отладка поиска регионов"""
    
    print("🔍 Отладка поиска регионов")
    print("=" * 60)
    
    parser = NLQParser()
    
    # Тестовый запрос
    query = "бумага А4 офисная Москва до 200 тыс руб"
    normalized = parser._normalize_text(query)
    lemmatized = parser._lemmatize_text(normalized)
    
    print(f"📝 Запрос: {query}")
    print(f"📝 Нормализованный: {normalized}")
    print(f"📝 Лемматизированный: {lemmatized}")
    
    # Проверяем поиск регионов в нормализованном тексте
    print(f"\n🔍 Поиск регионов в нормализованном тексте:")
    region_matches_normalized = []
    
    for region_info in parser.regions_dict:
        canonical = region_info["canonical"]
        aliases = region_info["aliases"]
        
        # Проверяем каноническое название
        if canonical.lower() in normalized:
            match_length = len(canonical.lower())
            is_city = "Город" in canonical
            region_matches_normalized.append((canonical, match_length, is_city, "canonical"))
            print(f"   Каноническое: {canonical} (длина: {match_length}, город: {is_city})")
        
        # Проверяем синонимы
        for alias in aliases:
            if alias.lower() in normalized:
                match_length = len(alias.lower())
                is_city = "Город" in canonical
                region_matches_normalized.append((canonical, match_length, is_city, f"alias: {alias}"))
                print(f"   Синоним: {alias} -> {canonical} (длина: {match_length}, город: {is_city})")
    
    # Проверяем поиск регионов в лемматизированном тексте
    print(f"\n🔍 Поиск регионов в лемматизированном тексте:")
    region_matches_lemmatized = []
    
    for region_info in parser.regions_dict:
        canonical = region_info["canonical"]
        aliases = region_info["aliases"]
        
        # Проверяем каноническое название
        if canonical.lower() in lemmatized:
            match_length = len(canonical.lower())
            is_city = "Город" in canonical
            region_matches_lemmatized.append((canonical, match_length, is_city, "canonical"))
            print(f"   Каноническое: {canonical} (длина: {match_length}, город: {is_city})")
        
        # Проверяем синонимы
        for alias in aliases:
            if alias.lower() in lemmatized:
                match_length = len(alias.lower())
                is_city = "Город" in canonical
                region_matches_lemmatized.append((canonical, match_length, is_city, f"alias: {alias}"))
                print(f"   Синоним: {alias} -> {canonical} (длина: {match_length}, город: {is_city})")
    
    # Результаты
    print(f"\n📊 Результаты для нормализованного текста:")
    if region_matches_normalized:
        region_matches_normalized.sort(key=lambda x: (x[2], x[1]), reverse=True)
        selected_normalized = region_matches_normalized[0][0]
        print(f"   🎯 Выбранный регион: {selected_normalized}")
    else:
        print(f"   ❌ Регионы не найдены")
    
    print(f"\n📊 Результаты для лемматизированного текста:")
    if region_matches_lemmatized:
        region_matches_lemmatized.sort(key=lambda x: (x[2], x[1]), reverse=True)
        selected_lemmatized = region_matches_lemmatized[0][0]
        print(f"   🎯 Выбранный регион: {selected_lemmatized}")
    else:
        print(f"   ❌ Регионы не найдены")

if __name__ == "__main__":
    debug_regions()
