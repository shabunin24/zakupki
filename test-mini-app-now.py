#!/usr/bin/env python3
"""
Немедленное тестирование Telegram Mini App
"""

import requests
import json

# Конфигурация
BOT_TOKEN = "8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw"
GITHUB_PAGES_URL = "https://shabunin24.github.io/zakupki/"

def send_mini_app_button():
    """Отправляет кнопку Mini App для тестирования"""
    print(f"🚀 Отправляю кнопку Mini App...")
    
    # Создаем inline клавиатуру с кнопкой Mini App
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "🚀 Открыть ГосЗакупки СЕЙЧАС",
                    "web_app": {
                        "url": GITHUB_PAGES_URL
                    }
                }
            ],
            [
                {
                    "text": "🔄 Проверить статус",
                    "callback_data": "check_status"
                }
            ]
        ]
    }
    
    # Данные для отправки сообщения
    message_data = {
        "chat_id": "794636253",
        "text": "🎯 **ТЕСТИРОВАНИЕ MINI APP**\n\nНажмите кнопку ниже, чтобы открыть приложение прямо сейчас:\n\n⚠️ Если Mini App не загрузится, нажмите 'Проверить статус'",
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard)
    }
    
    # URL для отправки сообщения
    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    try:
        response = requests.post(send_url, json=message_data)
        result = response.json()
        
        if result.get("ok"):
            print("✅ Тестовое сообщение отправлено!")
            print(f"📱 Mini App URL: {GITHUB_PAGES_URL}")
            return True
        else:
            print(f"❌ Ошибка отправки: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🚀 Немедленное тестирование Telegram Mini App")
    print("=" * 50)
    
    print(f"🌐 URL для тестирования: {GITHUB_PAGES_URL}")
    print("\n📋 Инструкция:")
    print("1. Получите сообщение с кнопкой")
    print("2. Нажмите '🚀 Открыть ГосЗакупки СЕЙЧАС'")
    print("3. Если не загрузится, нажмите '🔄 Проверить статус'")
    
    # Отправляем кнопку
    if send_mini_app_button():
        print("\n🎉 Готово! Проверяйте Mini App в Telegram!")
        print(f"🤖 Бот: @oborotn_bot")
    else:
        print("\n❌ Ошибка отправки!")

if __name__ == "__main__":
    main()
