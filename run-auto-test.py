#!/usr/bin/env python3
"""
Автоматическое тестирование функционала Telegram Mini App ГосЗакупки
"""

import requests
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def test_basic_functionality():
    """Тест базового функционала через HTTP запросы"""
    print("🔍 Тест 1: Базовый функционал (HTTP)")
    
    base_url = "http://localhost:8000"
    
    # Тест доступности главной страницы
    try:
        response = requests.get(f"{base_url}/index.html", timeout=5)
        main_page_ok = response.status_code == 200
        print(f"   Главная страница: {'✅' if main_page_ok else '❌'}")
    except Exception as e:
        print(f"   Главная страница: ❌ Ошибка: {e}")
        main_page_ok = False
    
    # Тест доступности тестовой страницы
    try:
        response = requests.get(f"{base_url}/test.html", timeout=5)
        test_page_ok = response.status_code == 200
        print(f"   Тестовая страница: {'✅' if test_page_ok else '❌'}")
    except Exception as e:
        print(f"   Тестовая страница: ❌ Ошибка: {e}")
        test_page_ok = False
    
    # Тест доступности CSS
    try:
        response = requests.get(f"{base_url}/styles.css", timeout=5)
        css_ok = response.status_code == 200
        print(f"   CSS стили: {'✅' if css_ok else '❌'}")
    except Exception as e:
        print(f"   CSS стили: ❌ Ошибка: {e}")
        css_ok = False
    
    # Тест доступности JavaScript
    try:
        response = requests.get(f"{base_url}/script.js", timeout=5)
        js_ok = response.status_code == 200
        print(f"   JavaScript: {'✅' if js_ok else '❌'}")
    except Exception as e:
        print(f"   JavaScript: ❌ Ошибка: {e}")
        js_ok = False
    
    # Тест доступности конфигурации
    try:
        response = requests.get(f"{base_url}/config.js", timeout=5)
        config_ok = response.status_code == 200
        print(f"   Конфигурация: {'✅' if config_ok else '❌'}")
    except Exception as e:
        print(f"   Конфигурация: ❌ Ошибка: {e}")
        config_ok = False
    
    return {
        'main_page': main_page_ok,
        'test_page': test_page_ok,
        'css': css_ok,
        'javascript': js_ok,
        'config': config_ok
    }

def test_telegram_bot_api():
    """Тест Telegram Bot API"""
    print("\n🤖 Тест 2: Telegram Bot API")
    
    bot_token = "8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw"
    api_url = f"https://api.telegram.org/bot{bot_token}/getMe"
    
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data['result']
                print(f"   ✅ Бот работает: @{bot_info['username']}")
                print(f"      Имя: {bot_info['first_name']}")
                print(f"      ID: {bot_info['id']}")
                return True
            else:
                print(f"   ❌ Ошибка бота: {data.get('description', 'Неизвестно')}")
                return False
        else:
            print(f"   ❌ API вернул код: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Ошибка подключения к API: {e}")
        return False

def test_github_pages():
    """Тест GitHub Pages"""
    print("\n🌐 Тест 3: GitHub Pages")
    
    try:
        response = requests.get("https://shabunin24.github.io/zakupki/", timeout=10)
        if response.status_code == 200:
            print("   ✅ GitHub Pages работает")
            return True
        else:
            print(f"   ⚠️  GitHub Pages вернул код: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ GitHub Pages недоступен: {e}")
        return False

def test_selenium_functionality():
    """Тест функционала через Selenium"""
    print("\n🧪 Тест 4: Функционал через браузер")
    
    try:
        # Настройка Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("http://localhost:8000/test.html")
        
        # Ждем загрузки страницы
        time.sleep(3)
        
        # Проверяем наличие основных элементов
        elements_to_check = [
            ("Заголовок", "h1", "ГосЗакупки"),
            ("Поиск", ".search-input", ""),
            ("Меню", ".main-menu", ""),
            ("Навигация", ".bottom-nav", "")
        ]
        
        results = {}
        for name, selector, expected_text in elements_to_check:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                if expected_text:
                    found = expected_text in element.text
                else:
                    found = element.is_displayed()
                
                results[name] = found
                print(f"   {name}: {'✅' if found else '❌'}")
            except Exception as e:
                results[name] = False
                print(f"   {name}: ❌ Ошибка: {e}")
        
        # Проверяем JavaScript функции
        js_tests = [
            ("mockPurchases", "typeof mockPurchases !== 'undefined' && mockPurchases.length > 0"),
            ("searchPurchases", "typeof searchPurchases === 'function'"),
            ("addToFavorites", "typeof addToFavorites === 'function'"),
            ("showPurchaseDetails", "typeof showPurchaseDetails === 'function'")
        ]
        
        js_results = {}
        for name, test_code in js_tests:
            try:
                result = driver.execute_script(f"return {test_code}")
                js_results[name] = result
                print(f"   {name}: {'✅' if result else '❌'}")
            except Exception as e:
                js_results[name] = False
                print(f"   {name}: ❌ Ошибка: {e}")
        
        driver.quit()
        
        return {
            'ui_elements': results,
            'javascript_functions': js_results
        }
        
    except Exception as e:
        print(f"   ❌ Ошибка Selenium: {e}")
        return None

def run_comprehensive_test():
    """Запуск комплексного тестирования"""
    print("🚀 КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ TELEGRAM MINI APP ГосЗакупки")
    print("=" * 70)
    
    # Запускаем все тесты
    basic_results = test_basic_functionality()
    bot_api_ok = test_telegram_bot_api()
    github_pages_ok = test_github_pages()
    selenium_results = test_selenium_functionality()
    
    # Итоговый отчет
    print("\n📊 ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ")
    print("=" * 70)
    
    # Подсчет результатов
    basic_tests = sum(basic_results.values())
    basic_total = len(basic_results)
    
    print(f"🔍 Базовый функционал: {basic_tests}/{basic_total} ✅")
    print(f"🤖 Telegram Bot API: {'✅' if bot_api_ok else '❌'}")
    print(f"🌐 GitHub Pages: {'✅' if github_pages_ok else '❌'}")
    
    if selenium_results:
        ui_tests = sum(selenium_results['ui_elements'].values())
        ui_total = len(selenium_results['ui_elements'])
        js_tests = sum(selenium_results['javascript_functions'].values())
        js_total = len(selenium_results['javascript_functions'])
        
        print(f"🧪 UI элементы: {ui_tests}/{ui_total} ✅")
        print(f"⚙️  JavaScript функции: {js_tests}/{js_total} ✅")
    
    # Общая оценка
    total_passed = basic_tests + (1 if bot_api_ok else 0) + (1 if github_pages_ok else 0)
    if selenium_results:
        total_passed += ui_tests + js_tests
        total_tests = basic_total + 2 + ui_total + js_total
    else:
        total_tests = basic_total + 2
    
    success_rate = (total_passed / total_tests) * 100
    
    print(f"\n📈 ОБЩИЙ РЕЗУЛЬТАТ: {total_passed}/{total_tests} ({success_rate:.1f}%)")
    
    # Рекомендации
    print("\n💡 РЕКОМЕНДАЦИИ:")
    if success_rate >= 90:
        print("🎉 Отличный результат! Приложение готово к использованию.")
    elif success_rate >= 70:
        print("⚠️  Хороший результат. Незначительные проблемы требуют исправления.")
    elif success_rate >= 50:
        print("❌ Средний результат. Требуется доработка основных функций.")
    else:
        print("🚨 Критический результат. Требуется серьезная доработка.")
    
    # Детали проблем
    if success_rate < 100:
        print("\n🔧 ПРОБЛЕМЫ ДЛЯ ИСПРАВЛЕНИЯ:")
        
        # Базовые проблемы
        for test_name, passed in basic_results.items():
            if not passed:
                print(f"   • {test_name} - недоступен")
        
        # API проблемы
        if not bot_api_ok:
            print("   • Telegram Bot API - не отвечает")
        if not github_pages_ok:
            print("   • GitHub Pages - не активирован")
        
        # Selenium проблемы
        if selenium_results:
            for test_name, passed in selenium_results['ui_elements'].items():
                if not passed:
                    print(f"   • UI элемент '{test_name}' - не найден")
            
            for test_name, passed in selenium_results['javascript_functions'].items():
                if not passed:
                    print(f"   • JavaScript функция '{test_name}' - не работает")
    
    return {
        'success_rate': success_rate,
        'total_passed': total_passed,
        'total_tests': total_tests,
        'details': {
            'basic': basic_results,
            'bot_api': bot_api_ok,
            'github_pages': github_pages_ok,
            'selenium': selenium_results
        }
    }

if __name__ == "__main__":
    try:
        results = run_comprehensive_test()
        print(f"\n✅ Тестирование завершено. Успешность: {results['success_rate']:.1f}%")
    except KeyboardInterrupt:
        print("\n⏹️  Тестирование прервано пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка тестирования: {e}")
