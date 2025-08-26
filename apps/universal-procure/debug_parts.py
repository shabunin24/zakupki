#!/usr/bin/env python3
"""
Отладка поиска по частям
"""

import sys
from pathlib import Path

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, str(Path(__file__).parent))

from parser.ru_nlq import NLQParser

def debug_parts():
    """Отладка поиска по частям"""
    
    print("🔍 Отладка поиска по частям")
    print("=" * 60)
    
    parser = NLQParser()
    
    # Тестовый запрос
    query = "услуги по строительству дорог Крым от 5 до 20 млн"
    lemmatized = parser._lemmatize_text(parser._normalize_text(query))
    
    print(f"📝 Запрос: {query}")
    print(f"📝 Лемматизированный: {lemmatized}")
    
    # Проверяем поиск по частям
    print(f"\n🔍 Поиск по частям:")
    query_words = set(lemmatized.split())
    print(f"   Слова в запросе: {query_words}")
    
    for keyword, okpd2_codes in parser.okpd2_dict.items():
        keyword_words = keyword.split()
        print(f"\n   Ключевое слово: '{keyword}' -> {okpd2_codes}")
        print(f"   Слова ключевого слова: {keyword_words}")
        
        # Проверяем каждое слово
        all_found = True
        for word in keyword_words:
            if word in query_words:
                print(f"      ✅ '{word}' найдено в запросе")
            else:
                print(f"      ❌ '{word}' НЕ найдено в запросе")
                all_found = False
        
        if all_found:
            print(f"      🎯 ВСЕ слова найдены! Ключевое слово '{keyword}' подходит")
        else:
            print(f"      ⚠️  Не все слова найдены")
    
    # Проверяем конкретно "строительство дорог"
    print(f"\n🔍 Проверка 'строительство дорог':")
    keyword = "строительство дорог"
    if keyword in parser.okpd2_dict:
        keyword_words = keyword.split()
        print(f"   Ключевое слово '{keyword}' есть в справочнике")
        print(f"   Слова: {keyword_words}")
        print(f"   Есть ли 'строительство' в запросе: {'строительство' in query_words}")
        print(f"   Есть ли 'дорог' в запросе: {'дорог' in query_words}")
        
        if all(word in query_words for word in keyword_words):
            print(f"   ✅ ВСЕ слова найдены!")
        else:
            print(f"   ❌ Не все слова найдены")
    else:
        print(f"   ❌ Ключевое слово '{keyword}' НЕ найдено в справочнике")

if __name__ == "__main__":
    debug_parts()
