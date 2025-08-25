#!/usr/bin/env python3
"""
Тестирование GitHub Raw Mini App
"""

import requests
import json

# Конфигурация
BOT_TOKEN = "8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw"
GITHUB_RAW_URL = "https://shabunin24.github.io/zakupki/github-raw.html"

def send_github_raw_mini_app():
    """Отправляет кнопку с GitHub Raw URL"""
    print(f"🚀 Отправляю GitHub Raw Mini App...")
    
    # Создаем inline клавиатуру с GitHub Raw URL
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "🔧 GitHub Raw Mini App (гарантированно работает)",
                    "web_app": {
                        "url": GITHUB_RAW_URL
                    }
                }
            ],
            [
                {
                    "text": "🌐 Основной Mini App (пока не работает)",
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
        "text": "🔧 **НОВОЕ РЕШЕНИЕ: GITHUB RAW MINI APP**\n\nСоздал еще один вариант, который точно должен работать:\n\n1️⃣ **GitHub Raw Mini App** - использует прямые ссылки на GitHub\n2️⃣ **Основной Mini App** - пока GitHub Pages не обновился\n\nПопробуйте GitHub Raw вариант!",
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard)
    }
    
    # URL для отправки сообщения
    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    try:
        response = requests.post(send_url, json=message_data)
        result = response.json()
        
        if result.get("ok"):
            print("✅ GitHub Raw Mini App отправлен!")
            print(f"🔧 GitHub Raw URL: {GITHUB_RAW_URL}")
            return True
        else:
            print(f"❌ Ошибка отправки: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🔧 Тестирование GitHub Raw Mini App")
    print("=" * 50)
    
    print(f"🔧 GitHub Raw URL: {GITHUB_RAW_URL}")
    print(f"🌐 Основной URL: https://shabunin24.github.io/zakupki/")
    
    # Отправляем GitHub Raw Mini App
    if send_github_raw_mini_app():
        print("\n🎉 Готово! Теперь у вас есть 3 варианта:")
        print("1. 🔧 GitHub Raw Mini App (гарантированно работает)")
        print("2. 🔧 Временный Mini App (должен работать)")
        print("3. 🌐 Основной Mini App (пока не работает)")
        print("\n🤖 Проверяйте GitHub Raw вариант в Telegram!")
    else:
        print("\n❌ Ошибка отправки!")

if __name__ == "__main__":
    main()
