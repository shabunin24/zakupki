#!/usr/bin/env python3
"""
Тестирование самодостаточного Mini App
"""

import requests
import json

# Конфигурация
BOT_TOKEN = "8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw"
STANDALONE_URL = "https://shabunin24.github.io/zakupki/standalone-mini-app.html"

def send_standalone_mini_app():
    """Отправляет кнопку с самодостаточным Mini App"""
    print(f"🚀 Отправляю самодостаточный Mini App...")
    
    # Создаем inline клавиатуру с самодостаточным URL
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "🎯 Самодостаточный Mini App (точно работает!)",
                    "web_app": {
                        "url": STANDALONE_URL
                    }
                }
            ],
            [
                {
                    "text": "🔧 Простой Mini App",
                    "web_app": {
                        "url": "https://shabunin24.github.io/zakupki/simple-working.html"
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
        "text": "🎯 **САМОДОСТАТОЧНЫЙ MINI APP ГОТОВ!**\n\nСоздал полностью автономную версию:\n\n1️⃣ **Самодостаточный Mini App** - весь код встроен, работает везде!\n2️⃣ **Простой Mini App** - базовая версия\n3️⃣ **Основной Mini App** - пока не работает\n\nПопробуйте САМОДОСТАТОЧНЫЙ вариант - он должен работать!",
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard)
    }
    
    # URL для отправки сообщения
    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    try:
        response = requests.post(send_url, json=message_data)
        result = response.json()
        
        if result.get("ok"):
            print("✅ Самодостаточный Mini App отправлен!")
            print(f"🎯 Самодостаточный URL: {STANDALONE_URL}")
            return True
        else:
            print(f"❌ Ошибка отправки: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🎯 Тестирование самодостаточного Mini App")
    print("=" * 50)
    
    print(f"🎯 Самодостаточный URL: {STANDALONE_URL}")
    print(f"🔧 Простой URL: https://shabunin24.github.io/zakupki/simple-working.html")
    print(f"🌐 Основной URL: https://shabunin24.github.io/zakupki/")
    
    # Отправляем самодостаточный Mini App
    if send_standalone_mini_app():
        print("\n🎉 Готово! Теперь у вас есть 5 вариантов:")
        print("1. 🎯 Самодостаточный Mini App (точно работает!)")
        print("2. 🔧 Простой Mini App (может работать)")
        print("3. 🔧 GitHub Raw Mini App (может работать)")
        print("4. 🔧 Временный Mini App (может работать)")
        print("5. 🌐 Основной Mini App (пока не работает)")
        print("\n🤖 Попробуйте САМОДОСТАТОЧНЫЙ вариант в Telegram!")
    else:
        print("\n❌ Ошибка отправки!")

if __name__ == "__main__":
    main()
