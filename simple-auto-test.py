#!/usr/bin/env python3
"""
Упрощенное автоматическое тестирование функционала Telegram Mini App ГосЗакупки
"""

import requests
import time
import json

def test_basic_functionality():
    """Тест базового функционала через HTTP запросы"""
    print("🔍 Тест 1: Базовый функционал (HTTP)")
    
    base_url = "http://localhost:8000"
    
    # Тест доступности главной страницы
    try:
        response = requests.get(f"{base_url}/index.html", timeout=5)
        main_page_ok = response.status_code == 200
        print(f"   Главная страница: {'✅' if main_page_ok else '❌'}")
        
        if main_page_ok:
            content = response.text
            # Проверяем наличие ключевых элементов
            has_title = "ГосЗакупки" in content
            has_search = "search-input" in content
            has_menu = "main-menu" in content
            has_nav = "bottom-nav" in content
            
            print(f"      Заголовок: {'✅' if has_title else '❌'}")
            print(f"      Поиск: {'✅' if has_search else '❌'}")
            print(f"      Меню: {'✅' if has_menu else '❌'}")
            print(f"      Навигация: {'✅' if has_nav else '❌'}")
            
            main_page_score = sum([has_title, has_search, has_menu, has_nav])
            main_page_total = 4
        else:
            main_page_score = 0
            main_page_total = 4
            
    except Exception as e:
        print(f"   Главная страница: ❌ Ошибка: {e}")
        main_page_ok = False
        main_page_score = 0
        main_page_total = 4
    
    # Тест доступности тестовой страницы
    try:
        response = requests.get(f"{base_url}/test.html", timeout=5)
        test_page_ok = response.status_code == 200
        print(f"   Тестовая страница: {'✅' if test_page_ok else '❌'}")
        
        if test_page_ok:
            content = response.text
            has_test_buttons = "test-btn" in content
            has_auto_test = "auto-test.js" in content
            print(f"      Тестовые кнопки: {'✅' if has_test_buttons else '❌'}")
            print(f"      Автотест: {'✅' if has_auto_test else '❌'}")
            
            test_page_score = sum([has_test_buttons, has_auto_test])
            test_page_total = 2
        else:
            test_page_score = 0
            test_page_total = 2
            
    except Exception as e:
        print(f"   Тестовая страница: ❌ Ошибка: {e}")
        test_page_ok = False
        test_page_score = 0
        test_page_total = 2
    
    # Тест доступности CSS
    try:
        response = requests.get(f"{base_url}/styles.css", timeout=5)
        css_ok = response.status_code == 200
        print(f"   CSS стили: {'✅' if css_ok else '❌'}")
        
        if css_ok:
            content = response.text
            has_ios_style = "apple-system" in content or "BlinkMacSystemFont" in content
            has_colors = "#007AFF" in content
            has_responsive = "@media" in content
            
            print(f"      iOS стиль: {'✅' if has_ios_style else '❌'}")
            print(f"      Цвета: {'✅' if has_colors else '❌'}")
            print(f"      Адаптивность: {'✅' if has_responsive else '❌'}")
            
            css_score = sum([has_ios_style, has_colors, has_responsive])
            css_total = 3
        else:
            css_score = 0
            css_total = 3
            
    except Exception as e:
        print(f"   CSS стили: ❌ Ошибка: {e}")
        css_ok = False
        css_score = 0
        css_total = 3
    
    # Тест доступности JavaScript
    try:
        response = requests.get(f"{base_url}/script.js", timeout=5)
        js_ok = response.status_code == 200
        print(f"   JavaScript: {'✅' if js_ok else '❌'}")
        
        if js_ok:
            content = response.text
            has_search = "searchPurchases" in content
            has_favorites = "addToFavorites" in content
            has_applications = "submitApplication" in content
            has_modals = "showModal" in content
            has_notifications = "showNotification" in content
            
            print(f"      Поиск: {'✅' if has_search else '❌'}")
            print(f"      Избранное: {'✅' if has_favorites else '❌'}")
            print(f"      Заявки: {'✅' if has_applications else '❌'}")
            print(f"      Модальные окна: {'✅' if has_modals else '❌'}")
            print(f"      Уведомления: {'✅' if has_notifications else '❌'}")
            
            js_score = sum([has_search, has_favorites, has_applications, has_modals, has_notifications])
            js_total = 5
        else:
            js_score = 0
            js_total = 5
            
    except Exception as e:
        print(f"   JavaScript: ❌ Ошибка: {e}")
        js_ok = False
        js_score = 0
        js_total = 5
    
    # Тест доступности конфигурации
    try:
        response = requests.get(f"{base_url}/config.js", timeout=5)
        config_ok = response.status_code == 200
        print(f"   Конфигурация: {'✅' if config_ok else '❌'}")
        
        if config_ok:
            content = response.text
            has_token = "8203311811" in content
            has_api_url = "api.telegram.org" in content
            has_webapp_url = "shabunin24.github.io" in content
            
            print(f"      Токен бота: {'✅' if has_token else '❌'}")
            print(f"      API URL: {'✅' if has_api_url else '❌'}")
            print(f"      WebApp URL: {'✅' if has_webapp_url else '❌'}")
            
            config_score = sum([has_token, has_api_url, has_webapp_url])
            config_total = 3
        else:
            config_score = 0
            config_total = 3
            
    except Exception as e:
        print(f"   Конфигурация: ❌ Ошибка: {e}")
        config_ok = False
        config_score = 0
        config_total = 3
    
    return {
        'main_page': {'ok': main_page_ok, 'score': main_page_score, 'total': main_page_total},
        'test_page': {'ok': test_page_ok, 'score': test_page_score, 'total': test_page_total},
        'css': {'ok': css_ok, 'score': css_score, 'total': css_total},
        'javascript': {'ok': js_ok, 'score': js_score, 'total': js_total},
        'config': {'ok': config_ok, 'score': config_score, 'total': config_total}
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
            
            content = response.text
            has_title = "ГосЗакупки" in content
            has_telegram = "telegram-web-app.js" in content
            has_config = "config.js" in content
            
            print(f"      Заголовок: {'✅' if has_title else '❌'}")
            print(f"      Telegram API: {'✅' if has_telegram else '❌'}")
            print(f"      Конфигурация: {'✅' if has_config else '❌'}")
            
            return True
        else:
            print(f"   ⚠️  GitHub Pages вернул код: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ GitHub Pages недоступен: {e}")
        return False

def test_advanced_features():
    """Тест расширенных функций через HTTP"""
    print("\n🚀 Тест 4: Расширенные функции")
    
    base_url = "http://localhost:8000"
    
    # Тест поиска закупок
    try:
        response = requests.get(f"{base_url}/test.html", timeout=5)
        if response.status_code == 200:
            content = response.text
            
            # Проверяем наличие расширенных функций
            has_advanced_search = "Расширенный поиск" in content
            has_filters = "Фильтры поиска" in content
            has_quick_filters = "Быстрые фильтры" in content
            has_stats = "Статистика" in content
            
            print(f"   Расширенный поиск: {'✅' if has_advanced_search else '❌'}")
            print(f"   Фильтры: {'✅' if has_filters else '❌'}")
            print(f"   Быстрые фильтры: {'✅' if has_quick_filters else '❌'}")
            print(f"   Статистика: {'✅' if has_stats else '❌'}")
            
            advanced_score = sum([has_advanced_search, has_filters, has_quick_filters, has_stats])
            advanced_total = 4
            
            return {'score': advanced_score, 'total': advanced_total}
        else:
            return {'score': 0, 'total': 4}
    except Exception as e:
        print(f"   ❌ Ошибка тестирования расширенных функций: {e}")
        return {'score': 0, 'total': 4}

def run_comprehensive_test():
    """Запуск комплексного тестирования"""
    print("🚀 КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ TELEGRAM MINI APP ГосЗакупки")
    print("=" * 70)
    
    # Запускаем все тесты
    basic_results = test_basic_functionality()
    bot_api_ok = test_telegram_bot_api()
    github_pages_ok = test_github_pages()
    advanced_results = test_advanced_features()
    
    # Итоговый отчет
    print("\n📊 ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ")
    print("=" * 70)
    
    # Подсчет результатов
    total_score = 0
    total_possible = 0
    
    print("🔍 ДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ:")
    for test_name, test_data in basic_results.items():
        score = test_data['score']
        total = test_data['total']
        percentage = (score / total) * 100 if total > 0 else 0
        
        print(f"   {test_name}: {score}/{total} ({percentage:.1f}%)")
        total_score += score
        total_possible += total
    
    # Добавляем результаты других тестов
    total_possible += 1  # Bot API
    if bot_api_ok:
        total_score += 1
    
    total_possible += 1  # GitHub Pages
    if github_pages_ok:
        total_score += 1
    
    # Расширенные функции
    advanced_score = advanced_results['score']
    advanced_total = advanced_results['total']
    total_score += advanced_score
    total_possible += advanced_total
    
    print(f"   Telegram Bot API: {'1/1 (100.0%)' if bot_api_ok else '0/1 (0.0%)'}")
    print(f"   GitHub Pages: {'1/1 (100.0%)' if github_pages_ok else '0/1 (0.0%)'}")
    print(f"   Расширенные функции: {advanced_score}/{advanced_total} ({(advanced_score/advanced_total)*100:.1f}%)")
    
    # Общая оценка
    success_rate = (total_score / total_possible) * 100
    
    print(f"\n📈 ОБЩИЙ РЕЗУЛЬТАТ: {total_score}/{total_possible} ({success_rate:.1f}%)")
    
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
        for test_name, test_data in basic_results.items():
            if test_data['score'] < test_data['total']:
                missing = test_data['total'] - test_data['score']
                print(f"   • {test_name} - не хватает {missing} из {test_data['total']} функций")
        
        # API проблемы
        if not bot_api_ok:
            print("   • Telegram Bot API - не отвечает")
        if not github_pages_ok:
            print("   • GitHub Pages - не активирован")
        
        # Расширенные функции
        if advanced_results['score'] < advanced_results['total']:
            missing = advanced_results['total'] - advanced_results['score']
            print(f"   • Расширенные функции - не хватает {missing} из {advanced_results['total']}")
    
    return {
        'success_rate': success_rate,
        'total_score': total_score,
        'total_possible': total_possible,
        'details': {
            'basic': basic_results,
            'bot_api': bot_api_ok,
            'github_pages': github_pages_ok,
            'advanced': advanced_results
        }
    }

if __name__ == "__main__":
    try:
        results = run_comprehensive_test()
        print(f"\n✅ Тестирование завершено. Успешность: {results['success_rate']:.1f}%")
        
        # Сохраняем результаты в файл
        with open('test_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("📄 Результаты сохранены в test_results.json")
        
    except KeyboardInterrupt:
        print("\n⏹️  Тестирование прервано пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка тестирования: {e}")
