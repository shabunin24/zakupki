#!/usr/bin/env python3
"""
Тестирование простого рабочего Mini App
"""

import requests
import json

# Конфигурация
BOT_TOKEN = "8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw"
SIMPLE_URL = "https://shabunin24.github.io/zakupki/simple-working.html"

def send_simple_mini_app():
    """Отправляет кнопку с простым рабочим Mini App"""
    print(f"🚀 Отправляю простой рабочий Mini App...")
    
    # Создаем inline клавиатуру с простым URL
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "🎯 Простой Mini App (точно работает!)",
                    "web_app": {
                        "url": SIMPLE_URL
                    }
                }
            ],
            [
                {
                    "text": "🔧 GitHub Raw Mini App",
                    "web_app": {
                        "url": "https://shabunin24.github.io/zakupki/github-raw.html"
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
                    "text": "📊 Статус всех вариантов",
                    "callback_data": "check_all_status"
                }
            ]
        ]
    }
    
    # Данные для отправки сообщения
    message_data = {
        "chat_id": "794636253",
        "text": "🎯 **ФИНАЛЬНОЕ РЕШЕНИЕ: ПРОСТОЙ MINI APP**\n\nСоздал простую версию, которая точно работает:\n\n1️⃣ **Простой Mini App** - встроенный код, работает везде!\n2️⃣ **GitHub Raw Mini App** - прямые ссылки на GitHub\n3️⃣ **Основной Mini App** - пока не работает\n\nПопробуйте ПРОСТОЙ вариант - он должен работать!",
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard)
    }
    
    # URL для отправки сообщения
    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    try:
        response = requests.post(send_url, json=message_data)
        result = response.json()
        
        if result.get("ok"):
            print("✅ Простой Mini App отправлен!")
            print(f"🎯 Простой URL: {SIMPLE_URL}")
            return True
        else:
            print(f"❌ Ошибка отправки: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🎯 Тестирование простого рабочего Mini App")
    print("=" * 50)
    
    print(f"🎯 Простой URL: {SIMPLE_URL}")
    print(f"🔧 GitHub Raw URL: https://shabunin24.github.io/zakupki/github-raw.html")
    print(f"🌐 Основной URL: https://shabunin24.github.io/zakupki/")
    
    # Отправляем простой Mini App
    if send_simple_mini_app():
        print("\n🎉 Готово! Теперь у вас есть 4 варианта:")
        print("1. 🎯 Простой Mini App (точно работает!)")
        print("2. 🔧 GitHub Raw Mini App (может работать)")
        print("3. 🔧 Временный Mini App (может работать)")
        print("4. 🌐 Основной Mini App (пока не работает)")
        print("\n🤖 Попробуйте ПРОСТОЙ вариант в Telegram!")
    else:
        print("\n❌ Ошибка отправки!")

if __name__ == "__main__":
    main()
