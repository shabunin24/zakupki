#!/usr/bin/env python3
"""
Диагностика ошибки поиска по слову "краска"
"""

import requests
import json

def debug_search_error():
    """Диагностика ошибки поиска"""
    print("🔍 Диагностика ошибки поиска по слову 'краска'")
    print("=" * 60)
    
    base_url = "https://shabunin24.github.io/zakupki"
    
    # Тест 1: Проверяем, есть ли закупки с "краска"
    print("\n📊 Тест 1: Поиск закупок с 'краска'")
    
    try:
        response = requests.get(f"{base_url}/script.js", timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Ищем закупки с краской
            if 'краска' in content.lower():
                print("   ✅ Слово 'краска' найдено в данных")
                
                # Ищем контекст
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'краска' in line.lower():
                        print(f"   📍 Строка {i+1}: {line.strip()[:100]}...")
            else:
                print("   ❌ Слово 'краска' не найдено в данных")
                
        else:
            print(f"   ❌ Не удалось загрузить script.js: код {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Ошибка поиска: {e}")
    
    # Тест 2: Проверяем функцию поиска
    print("\n⚙️ Тест 2: Анализ функции поиска")
    
    try:
        response = requests.get(f"{base_url}/script.js", timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Ищем функцию searchPurchases
            search_func_start = content.find('function searchPurchases')
            if search_func_start != -1:
                # Ищем конец функции (примерно)
                search_func_end = content.find('}', search_func_start)
                if search_func_end != -1:
                    search_func = content[search_func_start:search_func_end + 100]
                    print("   ✅ Функция searchPurchases найдена")
                    
                    # Проверяем наличие потенциальных проблем
                    if 'mockPurchases.forEach' in search_func:
                        print("   ✅ Использует mockPurchases.forEach")
                    else:
                        print("   ❌ Не использует mockPurchases.forEach")
                        
                    if 'toLowerCase()' in search_func:
                        print("   ✅ Использует toLowerCase() для поиска")
                    else:
                        print("   ❌ Не использует toLowerCase()")
                        
                    if 'includes(' in search_func:
                        print("   ✅ Использует includes() для поиска")
                    else:
                        print("   ❌ Не использует includes()")
                        
                else:
                    print("   ❌ Не удалось найти конец функции")
            else:
                print("   ❌ Функция searchPurchases не найдена")
                
        else:
            print(f"   ❌ Не удалось загрузить script.js: код {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Ошибка анализа функции: {e}")
    
    # Тест 3: Проверяем данные mockPurchases
    print("\n📋 Тест 3: Анализ данных mockPurchases")
    
    try:
        response = requests.get(f"{base_url}/script.js", timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Ищем начало массива
            start_marker = "const mockPurchases = ["
            start_pos = content.find(start_marker)
            
            if start_pos != -1:
                # Ищем конец массива
                end_pos = content.find("];", start_pos)
                if end_pos != -1:
                    purchases_data = content[start_pos:end_pos + 2]
                    
                    # Подсчитываем закупки
                    purchase_count = purchases_data.count('id:')
                    print(f"   ✅ Найдено закупок: {purchase_count}")
                    
                    # Проверяем каждую закупку на наличие проблем
                    lines = purchases_data.split('\n')
                    for i, line in enumerate(lines):
                        if 'id:' in line:
                            # Ищем потенциальные проблемы в строке
                            if 'undefined' in line:
                                print(f"   ⚠️ Строка {i+1}: содержит 'undefined'")
                            if 'null' in line:
                                print(f"   ⚠️ Строка {i+1}: содержит 'null'")
                            if 'NaN' in line:
                                print(f"   ⚠️ Строка {i+1}: содержит 'NaN'")
                                
                else:
                    print("   ❌ Не удалось найти конец массива")
            else:
                print("   ❌ Не удалось найти массив mockPurchases")
                
        else:
            print(f"   ❌ Не удалось загрузить script.js: код {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Ошибка анализа данных: {e}")
    
    # Тест 4: Проверяем тестовую страницу
    print("\n🧪 Тест 4: Проверка тестовой страницы")
    
    try:
        response = requests.get(f"{base_url}/simple-test.html", timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Проверяем наличие обработчиков ошибок
            if 'try {' in content and 'catch' in content:
                print("   ✅ Обработчики ошибок присутствуют")
            else:
                print("   ❌ Обработчики ошибок отсутствуют")
                
            if 'console.error' in content:
                print("   ✅ Логирование ошибок присутствует")
            else:
                print("   ❌ Логирование ошибок отсутствует")
                
        else:
            print(f"   ❌ Не удалось загрузить тестовую страницу: код {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Ошибка проверки тестовой страницы: {e}")
    
    # Тест 5: Создаем тестовый поиск
    print("\n🔍 Тест 5: Тестовый поиск")
    
    try:
        # Имитируем поиск по слову "краска"
        test_data = [
            {"id": 1, "title": "Поставка красок", "category": "Товары", "region": "Москва"},
            {"id": 2, "title": "Услуги по покраске", "category": "Услуги", "region": "СПб"},
            {"id": 3, "title": "Строительные работы", "category": "Работы", "region": "Новосибирск"}
        ]
        
        # Простой поиск
        results = []
        search_term = "краска"
        
        for item in test_data:
            if (search_term.lower() in item["title"].lower() or 
                search_term.lower() in item["category"].lower() or
                search_term.lower() in item["region"].lower()):
                results.append(item)
        
        print(f"   ✅ Тестовый поиск: найдено {len(results)} результатов")
        
        if results:
            for item in results:
                print(f"      - {item['title']} ({item['category']}, {item['region']})")
        else:
            print("      - Результатов не найдено")
            
    except Exception as e:
        print(f"   ❌ Ошибка тестового поиска: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 РЕКОМЕНДАЦИИ ПО ИСПРАВЛЕНИЮ:")
    print("1. Откройте консоль браузера (F12)")
    print("2. Попробуйте поиск по слову 'краска'")
    print("3. Скопируйте точный текст ошибки")
    print("4. Проверьте, есть ли закупки с краской в данных")
    print("5. Убедитесь, что функция searchPurchases корректно обрабатывает пустые результаты")

if __name__ == "__main__":
    debug_search_error()
