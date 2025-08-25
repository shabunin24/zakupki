#!/usr/bin/env python3
"""
Тестирование временного Mini App URL
"""

import requests
import json

# Конфигурация
BOT_TOKEN = "8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw"
TEMP_URL = "https://shabunin24.github.io/zakupki/temp-working.html"

def send_temp_mini_app():
    """Отправляет кнопку с временным URL"""
    print(f"🚀 Отправляю временный Mini App...")
    
    # Создаем inline клавиатуру с временным URL
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "🔧 Временный Mini App (рабочий)",
                    "web_app": {
                        "url": TEMP_URL
                    }
                }
            ],
            [
                {
                    "text": "🌐 Основной Mini App",
                    "web_app": {
                        "url": "https://shabunin24.github.io/zakupki/"
                    }
                }
            ],
            [
                {
                    "text": "🔄 Проверить оба",
                    "callback_data": "check_both"
                }
            ]
        ]
    }
    
    # Данные для отправки сообщения
    message_data = {
        "chat_id": "794636253",
        "text": "🔧 **РЕШЕНИЕ ПРОБЛЕМЫ БЕЛОГО ЭКРАНА**\n\nGitHub Pages еще не обновился, поэтому создал временное решение:\n\n1️⃣ **Временный Mini App** - должен работать СЕЙЧАС\n2️⃣ **Основной Mini App** - покажет белый экран\n\nПопробуйте временный вариант!",
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard)
    }
    
    # URL для отправки сообщения
    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    try:
        response = requests.post(send_url, json=message_data)
        result = response.json()
        
        if result.get("ok"):
            print("✅ Временный Mini App отправлен!")
            print(f"🔧 Временный URL: {TEMP_URL}")
            return True
        else:
            print(f"❌ Ошибка отправки: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🔧 Тестирование временного Mini App")
    print("=" * 50)
    
    print(f"🔧 Временный URL: {TEMP_URL}")
    print(f"🌐 Основной URL: https://shabunin24.github.io/zakupki/")
    
    # Отправляем временный Mini App
    if send_temp_mini_app():
        print("\n🎉 Готово! Теперь у вас есть 2 варианта:")
        print("1. 🔧 Временный Mini App (должен работать)")
        print("2. 🌐 Основной Mini App (пока белый экран)")
        print("\n🤖 Проверяйте в Telegram!")
    else:
        print("\n❌ Ошибка отправки!")

if __name__ == "__main__":
    main()
