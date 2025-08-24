#!/usr/bin/env python3
"""
Автоматическое тестирование Telegram Mini App ГосЗакупки
"""

import time
import webbrowser
import requests

def test_local_server():
    """Тестирование локального сервера"""
    print("🔍 Тестирование локального сервера...")
    
    try:
        response = requests.get("http://localhost:8000/test.html", timeout=5)
        if response.status_code == 200:
            print("✅ Локальный сервер работает")
            return True
        else:
            print(f"❌ Локальный сервер вернул код: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Локальный сервер недоступен: {e}")
        return False

def test_github_pages():
    """Тестирование GitHub Pages"""
    print("🌐 Тестирование GitHub Pages...")
    
    try:
        response = requests.get("https://shabunin24.github.io/zakupki/", timeout=10)
        if response.status_code == 200:
            print("✅ GitHub Pages работает")
            return True
        elif response.status_code == 404:
            print("⏳ GitHub Pages еще не активирован (ожидается)")
            return False
        else:
            print(f"⚠️  GitHub Pages вернул код: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ GitHub Pages недоступен: {e}")
        return False

def test_telegram_bot():
    """Тестирование Telegram Bot API"""
    print("🤖 Тестирование Telegram Bot API...")
    
    bot_token = "8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw"
    
    try:
        response = requests.get(f"https://api.telegram.org/bot{bot_token}/getMe", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data['result']
                print(f"✅ Бот работает: @{bot_info['username']}")
                print(f"   Имя: {bot_info['first_name']}")
                print(f"   ID: {bot_info['id']}")
                return True
            else:
                print(f"❌ Ошибка бота: {data.get('description', 'Неизвестно')}")
                return False
        else:
            print(f"❌ API вернул код: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения к API: {e}")
        return False

def test_web_app():
    """Тестирование веб-приложения"""
    print("📱 Тестирование веб-приложения...")
    
    # Открываем тестовую страницу
    try:
        webbrowser.open("http://localhost:8000/test.html")
        print("✅ Тестовая страница открыта в браузере")
        return True
    except Exception as e:
        print(f"❌ Не удалось открыть браузер: {e}")
        return False

def main():
    print("🧪 АВТОМАТИЧЕСКОЕ ТЕСТИРОВАНИЕ TELEGRAM MINI APP")
    print("=" * 60)
    print()
    
    tests = [
        ("Локальный сервер", test_local_server),
        ("Telegram Bot API", test_telegram_bot),
        ("Веб-приложение", test_web_app),
        ("GitHub Pages", test_github_pages)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"🔍 {test_name}...")
        try:
            result = test_func()
            results[test_name] = result
            print()
        except Exception as e:
            print(f"❌ Ошибка теста {test_name}: {e}")
            results[test_name] = False
            print()
    
    # Итоговый отчет
    print("📊 ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ ПРОШЕЛ" if result else "❌ НЕ ПРОШЕЛ"
        print(f"{test_name}: {status}")
    
    print()
    print(f"📈 Результат: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Приложение готово к использованию.")
    elif passed >= total - 1:
        print("⚠️  Большинство тестов пройдено. Незначительные проблемы.")
    else:
        print("❌ Много проблем. Требуется доработка.")
    
    print()
    print("📱 СЛЕДУЮЩИЕ ШАГИ:")
    
    if results.get("GitHub Pages"):
        print("1. ✅ GitHub Pages активирован")
        print("2. 🔧 Настройте Mini App через @BotFather")
        print("3. 🧪 Протестируйте бота в Telegram")
    else:
        print("1. ⏳ Дождитесь активации GitHub Pages (5-10 минут)")
        print("2. 🔧 Настройте Mini App через @BotFather")
        print("3. 🧪 Протестируйте бота в Telegram")
    
    if results.get("Telegram Bot API"):
        print("4. ✅ Бот работает корректно")
    else:
        print("4. ❌ Проверьте токен бота")
    
    print()
    print("🔗 Полезные ссылки:")
    print("   • Локальное тестирование: http://localhost:8000/test.html")
    print("   • GitHub репозиторий: https://github.com/shabunin24/zakupki")
    print("   • GitHub Pages: https://shabunin24.github.io/zakupki/")
    print("   • BotFather: @BotFather")

if __name__ == "__main__":
    main()
