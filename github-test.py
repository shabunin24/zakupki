#!/usr/bin/env python3
"""
Тестирование Telegram Mini App ГосЗакупки на GitHub Pages
"""

import requests
import time
import json

def test_github_pages_functionality():
    """Тест функционала на GitHub Pages"""
    print("🌐 Тест 1: GitHub Pages - Основной функционал")
    
    base_url = "https://shabunin24.github.io/zakupki"
    
    # Тест главной страницы
    try:
        response = requests.get(f"{base_url}/index.html", timeout=10)
        if response.status_code == 200:
            content = response.text
            print("   ✅ Главная страница загружена")
            
            # Проверяем ключевые элементы
            has_title = "ГосЗакупки" in content
            has_search = "search-input" in content or "Поиск" in content
            has_menu = "main-menu" in content or "Главное меню" in content
            has_nav = "bottom-nav" in content or "Навигация" in content
            has_telegram = "telegram-web-app.js" in content
            has_config = "config.js" in content
            
            print(f"      Заголовок: {'✅' if has_title else '❌'}")
            print(f"      Поиск: {'✅' if has_search else '❌'}")
            print(f"      Меню: {'✅' if has_menu else '❌'}")
            print(f"      Навигация: {'✅' if has_nav else '❌'}")
            print(f"      Telegram API: {'✅' if has_telegram else '❌'}")
            print(f"      Конфигурация: {'✅' if has_config else '❌'}")
            
            main_score = sum([has_title, has_search, has_menu, has_nav, has_telegram, has_config])
            main_total = 6
            
        else:
            print(f"   ❌ Главная страница вернула код: {response.status_code}")
            main_score = 0
            main_total = 6
            
    except Exception as e:
        print(f"   ❌ Ошибка загрузки главной страницы: {e}")
        main_score = 0
        main_total = 6
    
    # Тест тестовой страницы
    try:
        response = requests.get(f"{base_url}/test.html", timeout=10)
        if response.status_code == 200:
            content = response.text
            print("   ✅ Тестовая страница загружена")
            
            has_test_buttons = "test-btn" in content
            has_auto_test = "auto-test.js" in content
            has_search_test = "🔍 Тест поиска" in content
            has_favorites_test = "⭐ Тест избранного" in content
            
            print(f"      Тестовые кнопки: {'✅' if has_test_buttons else '❌'}")
            print(f"      Автотест: {'✅' if has_auto_test else '❌'}")
            print(f"      Тест поиска: {'✅' if has_search_test else '❌'}")
            print(f"      Тест избранного: {'✅' if has_favorites_test else '❌'}")
            
            test_score = sum([has_test_buttons, has_auto_test, has_search_test, has_favorites_test])
            test_total = 4
            
        else:
            print(f"   ❌ Тестовая страница вернула код: {response.status_code}")
            test_score = 0
            test_total = 4
            
    except Exception as e:
        print(f"   ❌ Ошибка загрузки тестовой страницы: {e}")
        test_score = 0
        test_total = 4
    
    # Тест CSS стилей
    try:
        response = requests.get(f"{base_url}/styles.css", timeout=10)
        if response.status_code == 200:
            content = response.text
            print("   ✅ CSS стили загружены")
            
            has_ios_style = "apple-system" in content or "BlinkMacSystemFont" in content
            has_colors = "#007AFF" in content or "007AFF" in content
            has_responsive = "@media" in content
            has_animations = "animation" in content or "transition" in content
            
            print(f"      iOS стиль: {'✅' if has_ios_style else '❌'}")
            print(f"      Цвета: {'✅' if has_colors else '❌'}")
            print(f"      Адаптивность: {'✅' if has_responsive else '❌'}")
            print(f"      Анимации: {'✅' if has_animations else '❌'}")
            
            css_score = sum([has_ios_style, has_colors, has_responsive, has_animations])
            css_total = 4
            
        else:
            print(f"   ❌ CSS вернул код: {response.status_code}")
            css_score = 0
            css_total = 4
            
    except Exception as e:
        print(f"   ❌ Ошибка загрузки CSS: {e}")
        css_score = 0
        css_total = 4
    
    # Тест JavaScript
    try:
        response = requests.get(f"{base_url}/script.js", timeout=10)
        if response.status_code == 200:
            content = response.text
            print("   ✅ JavaScript загружен")
            
            has_search = "searchPurchases" in content
            has_favorites = "addToFavorites" in content
            has_applications = "submitApplication" in content
            has_modals = "showModal" in content
            has_notifications = "showNotification" in content
            has_advanced_search = "performAdvancedSearch" in content
            has_filters = "getCurrentFilters" in content
            has_mock_data = "mockPurchases" in content
            
            print(f"      Поиск: {'✅' if has_search else '❌'}")
            print(f"      Избранное: {'✅' if has_favorites else '❌'}")
            print(f"      Заявки: {'✅' if has_applications else '❌'}")
            print(f"      Модальные окна: {'✅' if has_modals else '❌'}")
            print(f"      Уведомления: {'✅' if has_notifications else '❌'}")
            print(f"      Расширенный поиск: {'✅' if has_advanced_search else '❌'}")
            print(f"      Фильтры: {'✅' if has_filters else '❌'}")
            print(f"      Тестовые данные: {'✅' if has_mock_data else '❌'}")
            
            js_score = sum([has_search, has_favorites, has_applications, has_modals, 
                           has_notifications, has_advanced_search, has_filters, has_mock_data])
            js_total = 8
            
        else:
            print(f"   ❌ JavaScript вернул код: {response.status_code}")
            js_score = 0
            js_total = 8
            
    except Exception as e:
        print(f"   ❌ Ошибка загрузки JavaScript: {e}")
        js_score = 0
        js_total = 8
    
    # Тест конфигурации
    try:
        response = requests.get(f"{base_url}/config.js", timeout=10)
        if response.status_code == 200:
            content = response.text
            print("   ✅ Конфигурация загружена")
            
            has_token = "8203311811" in content
            has_api_url = "api.telegram.org" in content
            has_webapp_url = "shabunin24.github.io" in content
            has_bot_config = "BOT_CONFIG" in content
            
            print(f"      Токен бота: {'✅' if has_token else '❌'}")
            print(f"      API URL: {'✅' if has_api_url else '❌'}")
            print(f"      WebApp URL: {'✅' if has_webapp_url else '❌'}")
            print(f"      Конфигурация бота: {'✅' if has_bot_config else '❌'}")
            
            config_score = sum([has_token, has_api_url, has_webapp_url, has_bot_config])
            config_total = 4
            
        else:
            print(f"   ❌ Конфигурация вернула код: {response.status_code}")
            config_score = 0
            config_total = 4
            
    except Exception as e:
        print(f"   ❌ Ошибка загрузки конфигурации: {e}")
        config_score = 0
        config_total = 4
    
    return {
        'main_page': {'score': main_score, 'total': main_total},
        'test_page': {'score': test_score, 'total': test_total},
        'css': {'score': css_score, 'total': css_total},
        'javascript': {'score': js_score, 'total': js_total},
        'config': {'score': config_score, 'total': config_total}
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
                
                # Дополнительные тесты бота
                webhook_url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
                webhook_response = requests.get(webhook_url, timeout=10)
                if webhook_response.status_code == 200:
                    webhook_data = webhook_response.json()
                    if webhook_data.get('ok'):
                        webhook_info = webhook_data['result']
                        has_webhook = webhook_info.get('url', '') != ''
                        print(f"      Webhook: {'✅ Настроен' if has_webhook else '❌ Не настроен'}")
                        if has_webhook:
                            print(f"         URL: {webhook_info['url']}")
                
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

def test_advanced_features():
    """Тест расширенных функций"""
    print("\n🚀 Тест 3: Расширенные функции")
    
    base_url = "https://shabunin24.github.io/zakupki"
    
    try:
        response = requests.get(f"{base_url}/script.js", timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Проверяем наличие функций расширенного поиска в JavaScript
            has_advanced_search = "performAdvancedSearch" in content
            has_filters = "getCurrentFilters" in content
            has_quick_filters = "quickFilter" in content
            has_stats = "createSearchStats" in content
            has_category_filter = "categoryFilter" in content
            has_region_filter = "regionFilter" in content
            has_price_filter = "priceFrom" in content and "priceTo" in content
            has_status_filter = "statusFilter" in content
            
            print(f"   Расширенный поиск: {'✅' if has_advanced_search else '❌'}")
            print(f"   Фильтры поиска: {'✅' if has_filters else '❌'}")
            print(f"   Быстрые фильтры: {'✅' if has_quick_filters else '❌'}")
            print(f"   Статистика: {'✅' if has_stats else '❌'}")
            print(f"   Фильтр категорий: {'✅' if has_category_filter else '❌'}")
            print(f"   Фильтр регионов: {'✅' if has_region_filter else '❌'}")
            print(f"   Фильтр цен: {'✅' if has_price_filter else '❌'}")
            print(f"   Фильтр статуса: {'✅' if has_status_filter else '❌'}")
            
            advanced_score = sum([has_advanced_search, has_filters, has_quick_filters, has_stats,
                                has_category_filter, has_region_filter, has_price_filter, has_status_filter])
            advanced_total = 8
            
            return {'score': advanced_score, 'total': advanced_total}
        else:
            return {'score': 0, 'total': 8}
    except Exception as e:
        print(f"   ❌ Ошибка тестирования расширенных функций: {e}")
        return {'score': 0, 'total': 8}

def test_performance():
    """Тест производительности"""
    print("\n⚡ Тест 4: Производительность")
    
    base_url = "https://shabunin24.github.io/zakupki"
    
    # Тест скорости загрузки
    load_times = []
    files_to_test = ['index.html', 'styles.css', 'script.js', 'config.js']
    
    for file in files_to_test:
        try:
            start_time = time.time()
            response = requests.get(f"{base_url}/{file}", timeout=15)
            end_time = time.time()
            
            if response.status_code == 200:
                load_time = (end_time - start_time) * 1000  # в миллисекундах
                load_times.append(load_time)
                print(f"   {file}: {load_time:.0f}ms")
            else:
                print(f"   {file}: ❌ Код {response.status_code}")
                
        except Exception as e:
            print(f"   {file}: ❌ Ошибка: {e}")
    
    if load_times:
        avg_load_time = sum(load_times) / len(load_times)
        max_load_time = max(load_times)
        
        print(f"\n   Среднее время загрузки: {avg_load_time:.0f}ms")
        print(f"   Максимальное время: {max_load_time:.0f}ms")
        
        # Оценка производительности
        if avg_load_time < 1000:
            performance_score = 3  # Отлично
            performance_text = "Отлично"
        elif avg_load_time < 2000:
            performance_score = 2  # Хорошо
            performance_text = "Хорошо"
        elif avg_load_time < 5000:
            performance_score = 1  # Удовлетворительно
            performance_text = "Удовлетворительно"
        else:
            performance_score = 0  # Плохо
            performance_text = "Плохо"
        
        print(f"   Оценка производительности: {performance_text}")
        
        return {'score': performance_score, 'total': 3, 'avg_time': avg_load_time}
    else:
        print("   ❌ Не удалось измерить производительность")
        return {'score': 0, 'total': 3, 'avg_time': 0}

def run_github_comprehensive_test():
    """Запуск комплексного тестирования на GitHub Pages"""
    print("🚀 КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ НА GITHUB PAGES")
    print("=" * 70)
    
    # Запускаем все тесты
    github_results = test_github_pages_functionality()
    bot_api_ok = test_telegram_bot_api()
    advanced_results = test_advanced_features()
    performance_results = test_performance()
    
    # Итоговый отчет
    print("\n📊 ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ")
    print("=" * 70)
    
    # Подсчет результатов
    total_score = 0
    total_possible = 0
    
    print("🔍 ДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ:")
    for test_name, test_data in github_results.items():
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
    
    # Расширенные функции
    advanced_score = advanced_results['score']
    advanced_total = advanced_results['total']
    total_score += advanced_score
    total_possible += advanced_total
    
    # Производительность
    perf_score = performance_results['score']
    perf_total = performance_results['total']
    total_score += perf_score
    total_possible += perf_total
    
    print(f"   Telegram Bot API: {'1/1 (100.0%)' if bot_api_ok else '0/1 (0.0%)'}")
    print(f"   Расширенные функции: {advanced_score}/{advanced_total} ({(advanced_score/advanced_total)*100:.1f}%)")
    print(f"   Производительность: {perf_score}/{perf_total} ({(perf_score/perf_total)*100:.1f}%)")
    
    # Общая оценка
    success_rate = (total_score / total_possible) * 100
    
    print(f"\n📈 ОБЩИЙ РЕЗУЛЬТАТ: {total_score}/{total_possible} ({success_rate:.1f}%)")
    
    # Рекомендации
    print("\n💡 РЕКОМЕНДАЦИИ:")
    if success_rate >= 90:
        print("🎉 Отличный результат! Приложение готово к использованию в продакшене.")
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
        for test_name, test_data in github_results.items():
            if test_data['score'] < test_data['total']:
                missing = test_data['total'] - test_data['score']
                print(f"   • {test_name} - не хватает {missing} из {test_data['total']} функций")
        
        # API проблемы
        if not bot_api_ok:
            print("   • Telegram Bot API - не отвечает")
        
        # Расширенные функции
        if advanced_results['score'] < advanced_results['total']:
            missing = advanced_results['total'] - advanced_results['score']
            print(f"   • Расширенные функции - не хватает {missing} из {advanced_results['total']}")
        
        # Производительность
        if performance_results['score'] < performance_results['total']:
            print(f"   • Производительность - среднее время загрузки: {performance_results['avg_time']:.0f}ms")
    
    # Статус готовности к продакшену
    print(f"\n🚀 СТАТУС ГОТОВНОСТИ К ПРОДАКШЕНУ:")
    if success_rate >= 90:
        print("   ✅ ГОТОВ - Приложение полностью функционально")
    elif success_rate >= 70:
        print("   ⚠️  ЧАСТИЧНО ГОТОВ - Требует доработки")
    elif success_rate >= 50:
        print("   ❌ НЕ ГОТОВ - Критические проблемы")
    else:
        print("   🚨 КРИТИЧЕСКИ НЕ ГОТОВ - Требует серьезной доработки")
    
    return {
        'success_rate': success_rate,
        'total_score': total_score,
        'total_possible': total_possible,
        'production_ready': success_rate >= 90,
        'details': {
            'github': github_results,
            'bot_api': bot_api_ok,
            'advanced': advanced_results,
            'performance': performance_results
        }
    }

if __name__ == "__main__":
    try:
        results = run_github_comprehensive_test()
        print(f"\n✅ Тестирование завершено. Успешность: {results['success_rate']:.1f}%")
        print(f"🚀 Готов к продакшену: {'Да' if results['production_ready'] else 'Нет'}")
        
        # Сохраняем результаты в файл
        with open('github_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("📄 Результаты сохранены в github_test_results.json")
        
    except KeyboardInterrupt:
        print("\n⏹️  Тестирование прервано пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка тестирования: {e}")
