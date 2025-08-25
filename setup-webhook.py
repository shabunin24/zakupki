#!/usr/bin/env python3
"""
Скрипт для настройки webhook для бота ГосЗакупки
"""

import requests
import json

# Конфигурация бота
BOT_TOKEN = "8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw"
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_webhook_info():
    """Получает информацию о текущем webhook"""
    try:
        response = requests.get(f"{API_BASE}/getWebhookInfo")
        result = response.json()
        
        if result.get("ok"):
            webhook_info = result["result"]
            print("📊 Текущий webhook:")
            print(f"   URL: {webhook_info.get('url', 'Не установлен')}")
            print(f"   Ожидающие обновления: {webhook_info.get('pending_update_count', 0)}")
            return webhook_info
        else:
            print(f"❌ Ошибка получения webhook: {result}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def set_webhook(url):
    """Устанавливает webhook"""
    webhook_url = f"{url}/webhook"
    
    try:
        print(f"🔧 Устанавливаю webhook: {webhook_url}")
        
        response = requests.post(f"{API_BASE}/setWebhook", json={
            "url": webhook_url,
            "allowed_updates": ["message", "callback_query"]
        })
        
        result = response.json()
        if result.get("ok"):
            print("✅ Webhook успешно установлен!")
            return True
        else:
            print(f"❌ Ошибка установки webhook: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def delete_webhook():
    """Удаляет webhook"""
    try:
        print("🗑️ Удаляю webhook...")
        
        response = requests.post(f"{API_BASE}/deleteWebhook")
        result = response.json()
        
        if result.get("ok"):
            print("✅ Webhook удален!")
            return True
        else:
            print(f"❌ Ошибка удаления webhook: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_bot():
    """Тестирует бота"""
    try:
        print("🧪 Тестирую бота...")
        
        response = requests.get(f"{API_BASE}/getMe")
        result = response.json()
        
        if result.get("ok"):
            bot_info = result["result"]
            print(f"✅ Бот работает: @{bot_info['username']} ({bot_info['first_name']})")
            return True
        else:
            print(f"❌ Ошибка бота: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🤖 Настройка webhook для бота ГосЗакупки")
    print("=" * 50)
    
    # Тестируем бота
    if not test_bot():
        print("❌ Бот не работает, проверьте токен")
        return
    
    print()
    
    # Показываем текущий webhook
    get_webhook_info()
    
    print()
    print("🔧 Выберите действие:")
    print("1. Установить webhook (localhost:5000)")
    print("2. Установить webhook (ngrok)")
    print("3. Удалить webhook")
    print("4. Проверить статус")
    print("5. Выход")
    
    while True:
        choice = input("\nВведите номер (1-5): ").strip()
        
        if choice == "1":
            # Устанавливаем webhook для localhost
            set_webhook("http://localhost:5000")
            print("\n📱 Теперь запустите webhook сервер:")
            print("   python3 telegram-webhook.py")
            print("\n📱 И отправьте /start вашему боту @oborotn_bot")
            
        elif choice == "2":
            # Устанавливаем webhook для ngrok
            ngrok_url = input("Введите URL ngrok (например, https://abc123.ngrok.io): ").strip()
            if ngrok_url:
                set_webhook(ngrok_url)
            else:
                print("❌ URL не указан")
                
        elif choice == "3":
            delete_webhook()
            
        elif choice == "4":
            print()
            get_webhook_info()
            
        elif choice == "5":
            print("👋 До свидания!")
            break
            
        else:
            print("❌ Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
