#!/usr/bin/env python3
"""
Автоматический тест бота ГосЗакупки
Показывает, как будут выглядеть сообщения
"""

import requests
import json

# Конфигурация бота
BOT_TOKEN = "8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw"
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

def create_mini_app_keyboard():
    """Создает клавиатуру с кнопкой Mini App"""
    return {
        "inline_keyboard": [
            [
                {
                    "text": "🚀 Открыть ГосЗакупки",
                    "web_app": {
                        "url": "http://localhost:3000"
                    }
                }
            ],
            [
                {
                    "text": "🔍 Поиск закупок",
                    "callback_data": "search"
                },
                {
                    "text": "⭐ Избранное",
                    "callback_data": "favorites"
                }
            ],
            [
                {
                    "text": "ℹ️ Помощь",
                    "callback_data": "help"
                }
            ]
        ]
    }

def get_updates():
    """Получает последние обновления от бота"""
    try:
        response = requests.get(f"{API_BASE}/getUpdates")
        result = response.json()
        
        if result.get("ok"):
            updates = result["result"]
            if updates:
                # Берем последний чат
                last_update = updates[-1]
                if "message" in last_update:
                    return last_update["message"]["chat"]["id"]
                elif "callback_query" in last_update:
                    return last_update["callback_query"]["message"]["chat"]["id"]
        
        return None
        
    except Exception as e:
        print(f"❌ Ошибка получения обновлений: {e}")
        return None

def send_message(chat_id, text, reply_markup=None):
    """Отправляет сообщение"""
    url = f"{API_BASE}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    
    if reply_markup:
        data["reply_markup"] = reply_markup
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        if result.get("ok"):
            print(f"✅ Сообщение отправлено в чат {chat_id}")
            return True
        else:
            print(f"❌ Ошибка отправки: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🤖 Автоматический тест бота ГосЗакупки")
    print("=" * 50)
    
    # Проверяем бота
    print("🧪 Проверяю бота...")
    try:
        response = requests.get(f"{API_BASE}/getMe")
        result = response.json()
        
        if result.get("ok"):
            bot_info = result["result"]
            print(f"✅ Бот работает: @{bot_info['username']} ({bot_info['first_name']})")
        else:
            print(f"❌ Бот не работает: {result}")
            return
            
    except Exception as e:
        print(f"❌ Ошибка проверки бота: {e}")
        return
    
    print("\n📱 Ищем активные чаты...")
    chat_id = get_updates()
    
    if not chat_id:
        print("❌ Активные чаты не найдены")
        print("\n📋 Инструкции:")
        print("1. Откройте @oborotn_bot в Telegram")
        print("2. Отправьте любое сообщение (например, 'привет')")
        print("3. Запустите этот скрипт снова")
        return
    
    print(f"✅ Найден чат: {chat_id}")
    
    # Отправляем тестовые сообщения
    print("\n🚀 Отправляю тестовые сообщения...")
    
    # 1. Приветствие
    welcome_text = """
🎉 <b>Добро пожаловать в ГосЗакупки!</b>

👋 Привет! Это тестовое сообщение от бота.

🔍 <b>Что умеет бот:</b>
• Поиск государственных закупок
• Фильтрация по регионам и категориям
• Отслеживание избранных закупок
• Уведомления о новых закупках

🚀 <b>Нажмите кнопку ниже, чтобы открыть приложение:</b>
    """
    
    keyboard = create_mini_app_keyboard()
    send_message(chat_id, welcome_text, keyboard)
    
    print("\n✅ Тест завершен!")
    print("\n📱 Теперь в Telegram:")
    print("• Откройте чат с ботом")
    print("• Нажмите на кнопку '🚀 Открыть ГосЗакупки'")
    print("• Должно открыться ваше приложение")
    
    print("\n🔧 Для настройки webhook:")
    print("• Получите HTTPS URL (localtunnel, ngrok, или хостинг)")
    print("• Запустите: python3 setup-webhook.py")

if __name__ == "__main__":
    main()
