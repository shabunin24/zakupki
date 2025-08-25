#!/usr/bin/env python3
"""
Настройка webhook для Telegram Mini App на GitHub Pages
"""

import requests
import json
import os

# Конфигурация
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Замените на ваш токен
GITHUB_PAGES_URL = "https://shabunin24.github.io/zakupki/"

def setup_webhook():
    """Настраивает webhook для бота"""
    webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    
    # URL для webhook (ваш сервер)
    webhook_data = {
        "url": "YOUR_WEBHOOK_URL_HERE",  # Замените на ваш webhook URL
        "allowed_updates": ["message", "callback_query"],
        "drop_pending_updates": True
    }
    
    try:
        response = requests.post(webhook_url, json=webhook_data)
        result = response.json()
        
        if result.get("ok"):
            print("✅ Webhook успешно настроен!")
            print(f"📡 URL: {result.get('result', {}).get('url', 'N/A')}")
        else:
            print(f"❌ Ошибка настройки webhook: {result.get('description')}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def setup_mini_app():
    """Настраивает Mini App URL в боте"""
    print(f"🎯 Mini App URL: {GITHUB_PAGES_URL}")
    print("\n📋 Что нужно сделать:")
    print("1. Откройте @BotFather в Telegram")
    print("2. Отправьте команду: /mybots")
    print("3. Выберите вашего бота")
    print("4. Bot Settings → Menu Button")
    print("5. Введите URL:", GITHUB_PAGES_URL)
    print("6. Введите текст кнопки: 'Открыть ГосЗакупки'")

def test_bot():
    """Тестирует подключение к боту"""
    test_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    
    try:
        response = requests.get(test_url)
        result = response.json()
        
        if result.get("ok"):
            bot_info = result.get("result", {})
            print("✅ Бот подключен!")
            print(f"🤖 Имя: {bot_info.get('first_name')}")
            print(f"📝 Username: @{bot_info.get('username')}")
            print(f"🆔 ID: {bot_info.get('id')}")
        else:
            print(f"❌ Ошибка подключения: {result.get('description')}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def main():
    print("🚀 Настройка Telegram Mini App Webhook")
    print("=" * 50)
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Сначала замените BOT_TOKEN на ваш токен!")
        print("📝 Получите токен у @BotFather")
        return
    
    print("\n🔧 Выберите действие:")
    print("1. Тестировать подключение к боту")
    print("2. Настроить webhook")
    print("3. Настроить Mini App URL")
    print("4. Все действия")
    
    choice = input("\nВведите номер (1-4): ").strip()
    
    if choice == "1":
        test_bot()
    elif choice == "2":
        setup_webhook()
    elif choice == "3":
        setup_mini_app()
    elif choice == "4":
        test_bot()
        print("\n" + "="*30 + "\n")
        setup_webhook()
        print("\n" + "="*30 + "\n")
        setup_mini_app()
    else:
        print("❌ Неверный выбор")

if __name__ == "__main__":
    main()
