#!/usr/bin/env python3
"""
Автоматический тест поиска на GitHub Pages
"""

import requests
import time
import json

def test_search_functionality():
    """Тест функционала поиска на GitHub Pages"""
    print("🔍 Тест поиска на GitHub Pages")
    print("=" * 50)
    
    base_url = "https://shabunin24.github.io/zakupki"
    
    # Тест 1: Проверка загрузки основных файлов
    print("\n📁 Тест 1: Загрузка файлов")
    
    files_to_test = [
        ('script.js', 'JavaScript функции'),
        ('config.js', 'Конфигурация'),
        ('simple-test.html', 'Тестовая страница')
    ]
    
    for filename, description in files_to_test:
        try:
            response = requests.get(f"{base_url}/{filename}", timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {description}: загружен")
            else:
                print(f"   ❌ {description}: код {response.status_code}")
        except Exception as e:
            print(f"   ❌ {description}: ошибка {e}")
    
    # Тест 2: Проверка наличия ключевых функций
    print("\n⚙️ Тест 2: Проверка функций")
    
    try:
        response = requests.get(f"{base_url}/script.js", timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Проверяем наличие ключевых функций
            functions_to_check = [
                ('searchPurchases', 'Основная функция поиска'),
                ('mockPurchases', 'Тестовые данные'),
                ('performAdvancedSearch', 'Расширенный поиск'),
                ('getCurrentFilters', 'Получение фильтров')
            ]
            
            for func_name, description in functions_to_check:
                if func_name in content:
                    print(f"   ✅ {description}: найдена")
                else:
                    print(f"   ❌ {description}: не найдена")
        else:
            print(f"   ❌ Не удалось загрузить script.js: код {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Ошибка проверки функций: {e}")
    
    # Тест 3: Проверка данных
    print("\n📊 Тест 3: Проверка данных")
    
    try:
        response = requests.get(f"{base_url}/script.js", timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Ищем начало массива mockPurchases
            start_marker = "const mockPurchases = ["
            end_marker = "];"
            
            start_pos = content.find(start_marker)
            if start_pos != -1:
                # Ищем конец массива
                end_pos = content.find(end_marker, start_pos)
                if end_pos != -1:
                    purchases_data = content[start_pos:end_pos + 2]
                    
                    # Подсчитываем количество закупок
                    purchase_count = purchases_data.count('id:')
                    print(f"   ✅ Найдено закупок: {purchase_count}")
                    
                    # Проверяем структуру данных
                    has_title = 'title:' in purchases_data
                    has_price = 'price:' in purchases_data
                    has_category = 'category:' in purchases_data
                    has_region = 'region:' in purchases_data
                    
                    print(f"   ✅ Заголовки: {'да' if has_title else 'нет'}")
                    print(f"   ✅ Цены: {'да' if has_price else 'нет'}")
                    print(f"   ✅ Категории: {'да' if has_category else 'нет'}")
                    print(f"   ✅ Регионы: {'да' if has_region else 'нет'}")
                    
                else:
                    print("   ❌ Не удалось найти конец массива данных")
            else:
                print("   ❌ Не удалось найти массив mockPurchases")
                
        else:
            print(f"   ❌ Не удалось загрузить script.js: код {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Ошибка проверки данных: {e}")
    
    # Тест 4: Проверка тестовой страницы
    print("\n🧪 Тест 4: Тестовая страница")
    
    try:
        response = requests.get(f"{base_url}/simple-test.html", timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Проверяем наличие ключевых элементов
            elements_to_check = [
                ('Тест поиска ГосЗакупки', 'Заголовок страницы'),
                ('Проверить загрузку данных', 'Кнопка проверки данных'),
                ('Выполнить поиск', 'Кнопка поиска'),
                ('Поиск с фильтрами', 'Кнопка фильтрованного поиска'),
                ('Запустить все тесты', 'Кнопка комплексного теста')
            ]
            
            for element_text, description in elements_to_check:
                if element_text in content:
                    print(f"   ✅ {description}: найден")
                else:
                    print(f"   ❌ {description}: не найден")
                    
            # Проверяем наличие JavaScript функций
            js_functions = [
                ('checkData', 'Функция проверки данных'),
                ('performSearch', 'Функция поиска'),
                ('performFilteredSearch', 'Функция фильтрованного поиска'),
                ('runComprehensiveTest', 'Функция комплексного теста')
            ]
            
            for func_name, description in js_functions:
                if func_name in content:
                    print(f"   ✅ {description}: найдена")
                else:
                    print(f"   ❌ {description}: не найдена")
                    
        else:
            print(f"   ❌ Не удалось загрузить тестовую страницу: код {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Ошибка проверки тестовой страницы: {e}")
    
    # Тест 5: Проверка производительности
    print("\n⚡ Тест 5: Производительность")
    
    try:
        start_time = time.time()
        response = requests.get(f"{base_url}/simple-test.html", timeout=15)
        end_time = time.time()
        
        if response.status_code == 200:
            load_time = (end_time - start_time) * 1000
            print(f"   ✅ Время загрузки: {load_time:.0f}ms")
            
            if load_time < 1000:
                print("   📊 Оценка: Отлично")
            elif load_time < 2000:
                print("   📊 Оценка: Хорошо")
            elif load_time < 5000:
                print("   📊 Оценка: Удовлетворительно")
            else:
                print("   📊 Оценка: Медленно")
        else:
            print(f"   ❌ Страница не загрузилась: код {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Ошибка тестирования производительности: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 РЕКОМЕНДАЦИИ:")
    print("1. Откройте https://shabunin24.github.io/zakupki/simple-test.html")
    print("2. Нажмите 'Запустить все тесты'")
    print("3. Проверьте консоль браузера (F12) на ошибки")
    print("4. Попробуйте выполнить поиск по тексту 'компьютер'")

if __name__ == "__main__":
    test_search_functionality()
