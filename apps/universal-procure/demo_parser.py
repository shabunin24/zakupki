#!/usr/bin/env python3
"""
Демонстрация работы парсера естественного языка
"""

import sys
from pathlib import Path

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, str(Path(__file__).parent))

from parser.ru_nlq import NLQParser

def demo_parser():
    """Демонстрирует работу парсера на примерах"""
    
    print("🚀 UniversalProcureSearch - Демонстрация парсера естественного языка")
    print("=" * 70)
    
    # Создаем парсер
    parser = NLQParser()
    
    # Примеры запросов из требований
    test_queries = [
        "бумага А4 офисная Москва до 200 тыс руб",
        "услуги по строительству дорог Крым от 5 до 20 млн",
        "поставка медоборудования Москва конкурс",
        "электромонтажные работы до 3 млн руб Санкт-Петербург новые за неделю",
        "строительство мостов в Краснодарском крае от 10 до 50 млн рублей конкурс",
        "канцелярские товары",
        "до 1 млн рублей",
        "в Москве",
        "электронный аукцион"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Пример {i}: {query}")
        print("-" * 50)
        
        try:
            # Парсим запрос
            result = parser.parse(query)
            
            # Выводим результат
            print(f"📊 Результат парсинга:")
            print(f"   Текст: {result['text']}")
            
            if result['okpd2']:
                print(f"   ОКПД2: {', '.join(result['okpd2'])}")
            
            if result['region']:
                print(f"   Регион: {', '.join(result['region'])}")
            
            if result['price_min'] is not None:
                print(f"   Цена от: {result['price_min']:,.0f} руб")
            
            if result['price_max'] is not None:
                print(f"   Цена до: {result['price_max']:,.0f} руб")
            
            if result['method']:
                print(f"   Метод: {', '.join(result['method'])}")
            
            if result['status']:
                print(f"   Статус: {', '.join(result['status'])}")
            
            if result['publish_date_from']:
                print(f"   Публикация с: {result['publish_date_from'].strftime('%Y-%m-%d')}")
            
            if result['deadline_from']:
                print(f"   Дедлайн с: {result['deadline_from'].strftime('%Y-%m-%d')}")
            
            if result['deadline_to']:
                print(f"   Дедлайн до: {result['deadline_to'].strftime('%Y-%m-%d')}")
            
            # Выводим диагностику
            if 'diagnostics' in result:
                diagnostics = result['diagnostics']
                print(f"   🔍 Диагностика:")
                if diagnostics['matched_keywords']:
                    print(f"      Ключевые слова: {', '.join(diagnostics['matched_keywords'])}")
                if diagnostics['regions_detected']:
                    print(f"      Регионы: {', '.join(diagnostics['regions_detected'])}")
                if diagnostics['method_detected']:
                    print(f"      Метод: {diagnostics['method_detected']}")
                if diagnostics['status_detected']:
                    print(f"      Статус: {diagnostics['status_detected']}")
                if diagnostics['date_rules']:
                    print(f"      Правила дат: {', '.join(diagnostics['date_rules'])}")
                
        except Exception as e:
            print(f"❌ Ошибка парсинга: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Демонстрация завершена!")
    print("\n💡 Попробуйте запустить тесты:")
    print("   pytest tests/ -v")
    print("\n🚀 Или запустите сервер:")
    print("   uvicorn app:app --reload")

if __name__ == "__main__":
    demo_parser()
