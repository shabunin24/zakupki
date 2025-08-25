#!/usr/bin/env python3
"""
Тестирование прямого Mini App для GitHub Pages
"""

import requests
import json

# Конфигурация
BOT_TOKEN = "8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw"
DIRECT_URL = "https://shabunin24.github.io/zakupki/direct-mini-app.html"

def send_direct_mini_app():
    """Отправляет кнопку с прямым Mini App"""
    print(f"🚀 Отправляю прямой Mini App для GitHub Pages...")
    
    # Создаем inline клавиатуру с прямым URL
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "🎯 Прямой Mini App (GitHub Pages)",
                    "web_app": {
                        "url": DIRECT_URL
                    }
                }
            ],
            [
                {
                    "text": "🔧 Самодостаточный Mini App",
                    "web_app": {
                        "url": "https://shabunin24.github.io/zakupki/standalone-mini-app.html"
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
        "text": "🎯 **ПРЯМОЙ MINI APP ДЛЯ GITHUB PAGES ГОТОВ!**\n\nСоздал специальную версию для GitHub Pages:\n\n1️⃣ **Прямой Mini App** - специально для GitHub Pages!\n2️⃣ **Самодостаточный Mini App** - полная версия\n3️⃣ **Основной Mini App** - пока не работает\n\nПопробуйте ПРЯМОЙ вариант - он должен работать на GitHub Pages!",
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard)
    }
    
    # URL для отправки сообщения
    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    try:
        response = requests.post(send_url, json=message_data)
        result = response.json()
        
        if result.get("ok"):
            print("✅ Прямой Mini App отправлен!")
            print(f"🎯 Прямой URL: {DIRECT_URL}")
            return True
        else:
            print(f"❌ Ошибка отправки: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🎯 Тестирование прямого Mini App для GitHub Pages")
    print("=" * 50)
    
    print(f"🎯 Прямой URL: {DIRECT_URL}")
    print(f"🔧 Самодостаточный URL: https://shabunin24.github.io/zakupki/standalone-mini-app.html")
    print(f"🌐 Основной URL: https://shabunin24.github.io/zakupki/")
    
    # Отправляем прямой Mini App
    if send_direct_mini_app():
        print("\n🎉 Готово! Теперь у вас есть 6 вариантов:")
        print("1. 🎯 Прямой Mini App (GitHub Pages)")
        print("2. 🔧 Самодостаточный Mini App")
        print("3. 🔧 Простой Mini App")
        print("4. 🔧 GitHub Raw Mini App")
        print("5. 🔧 Временный Mini App")
        print("6. 🌐 Основной Mini App (пока не работает)")
        print("\n🤖 Попробуйте ПРЯМОЙ вариант в Telegram!")
    else:
        print("\n❌ Ошибка отправки!")

if __name__ == "__main__":
    main()
