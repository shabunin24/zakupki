#!/usr/bin/env python3
"""
Автоматическая настройка Telegram Mini App на GitHub Pages
"""

import requests
import json

# Конфигурация
BOT_TOKEN = "8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw"
GITHUB_PAGES_URL = "https://shabunin24.github.io/zakupki/"

def test_mini_app_url():
    """Тестирует доступность Mini App URL"""
    print(f"🔍 Проверяю доступность: {GITHUB_PAGES_URL}")
    
    try:
        response = requests.get(GITHUB_PAGES_URL, timeout=10)
        if response.status_code == 200:
            print("✅ GitHub Pages доступен!")
            print(f"📄 Размер страницы: {len(response.text)} байт")
            return True
        else:
            print(f"❌ Ошибка HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def setup_menu_button():
    """Настраивает кнопку меню для Mini App"""
    print(f"\n🎯 Настраиваю кнопку меню...")
    
    # Создаем кнопку меню
    menu_button_data = {
        "type": "web_app",
        "text": "Открыть ГосЗакупки",
        "web_app": {
            "url": GITHUB_PAGES_URL
        }
    }
    
    # Отправляем команду для установки кнопки меню
    set_menu_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setChatMenuButton"
    
    try:
        response = requests.post(set_menu_url, json=menu_button_data)
        result = response.json()
        
        if result.get("ok"):
            print("✅ Кнопка меню настроена!")
            return True
        else:
            print(f"❌ Ошибка настройки кнопки: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def send_test_message():
    """Отправляет тестовое сообщение с кнопкой Mini App"""
    print(f"\n📤 Отправляю тестовое сообщение...")
    
    # Создаем inline клавиатуру с кнопкой Mini App
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "🚀 Открыть ГосЗакупки",
                    "web_app": {
                        "url": GITHUB_PAGES_URL
                    }
                }
            ]
        ]
    }
    
    # Данные для отправки сообщения
    message_data = {
        "chat_id": "794636253",  # Замените на ваш chat_id
        "text": "🎉 ГосЗакупки Mini App готов к работе!\n\nНажмите кнопку ниже, чтобы открыть приложение:",
        "reply_markup": json.dumps(keyboard)
    }
    
    # URL для отправки сообщения
    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    try:
        response = requests.post(send_url, json=message_data)
        result = response.json()
        
        if result.get("ok"):
            print("✅ Тестовое сообщение отправлено!")
            return True
        else:
            print(f"❌ Ошибка отправки: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def get_updates():
    """Получает последние обновления от бота"""
    print(f"\n📡 Получаю обновления от бота...")
    
    updates_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    
    try:
        response = requests.get(updates_url)
        result = response.json()
        
        if result.get("ok"):
            updates = result.get("result", [])
            print(f"📨 Получено обновлений: {len(updates)}")
            
            if updates:
                # Показываем последнее обновление
                last_update = updates[-1]
                if "message" in last_update:
                    chat_id = last_update["message"]["chat"]["id"]
                    print(f"💬 Последний chat_id: {chat_id}")
                    return chat_id
                elif "callback_query" in last_update:
                    chat_id = last_update["callback_query"]["message"]["chat"]["id"]
                    print(f"🔘 Последний callback chat_id: {chat_id}")
                    return chat_id
            
            print("📭 Нет новых сообщений")
            return None
        else:
            print(f"❌ Ошибка получения обновлений: {result.get('description')}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def main():
    print("🚀 Автоматическая настройка Telegram Mini App")
    print("=" * 50)
    
    # Шаг 1: Проверяем доступность GitHub Pages
    if not test_mini_app_url():
        print("❌ GitHub Pages недоступен! Проверьте настройки.")
        return
    
    # Шаг 2: Настраиваем кнопку меню
    if not setup_menu_button():
        print("❌ Не удалось настроить кнопку меню!")
        return
    
    # Шаг 3: Получаем chat_id для тестирования
    chat_id = get_updates()
    
    if chat_id:
        print(f"\n🎯 Найден chat_id: {chat_id}")
        print("📝 Обновите скрипт с этим chat_id для отправки тестового сообщения")
        
        # Обновляем скрипт с найденным chat_id
        with open("setup-mini-app-auto.py", "r") as f:
            content = f.read()
        
        content = content.replace("794636253", str(chat_id))
        
        with open("setup-mini-app-auto.py", "w") as f:
            f.write(content)
        
        print("✅ Скрипт обновлен! Теперь можно отправить тестовое сообщение")
        
        # Отправляем тестовое сообщение
        send_test_message()
    else:
        print("\n📱 Отправьте любое сообщение боту @oborotn_bot")
        print("📝 Затем запустите скрипт снова для получения chat_id")
    
    print(f"\n🎉 Настройка завершена!")
    print(f"🌐 Mini App URL: {GITHUB_PAGES_URL}")
    print(f"🤖 Бот: @oborotn_bot")

if __name__ == "__main__":
    main()
