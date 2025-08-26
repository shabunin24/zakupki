#!/usr/bin/env python3
"""
Автоматическое развертывание Telegram бота на Render.com
"""

import requests
import json
import os
import time

# Конфигурация
BOT_TOKEN = "8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw"
RENDER_API_KEY = "your_render_api_key"  # Замените на ваш API ключ

def create_render_service():
    """Создает сервис на Render.com"""
    
    headers = {
        "Authorization": f"Bearer {RENDER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    service_data = {
        "name": "telegram-bot-goszakupki",
        "type": "web_service",
        "env": "python",
        "region": "oregon",
        "plan": "free",
        "buildCommand": "pip install -r requirements.txt",
        "startCommand": "python telegram-webhook.py",
        "healthCheckPath": "/health",
        "autoDeploy": "yes"
    }
    
    try:
        response = requests.post(
            "https://api.render.com/v1/services",
            headers=headers,
            json=service_data
        )
        
        if response.status_code == 201:
            service = response.json()
            print(f"✅ Сервис создан: {service['service']['url']}")
            return service['service']['url']
        else:
            print(f"❌ Ошибка создания сервиса: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def set_webhook(webhook_url):
    """Устанавливает webhook для бота"""
    
    webhook_data = {
        "url": f"{webhook_url}/webhook",
        "allowed_updates": ["message", "callback_query"]
    }
    
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
            json=webhook_data
        )
        
        result = response.json()
        if result.get("ok"):
            print(f"✅ Webhook установлен: {webhook_data['url']}")
            return True
        else:
            print(f"❌ Ошибка установки webhook: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def check_webhook():
    """Проверяет текущий webhook"""
    
    try:
        response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo")
        result = response.json()
        
        if result.get("ok"):
            webhook_info = result["result"]
            if webhook_info.get("url"):
                print(f"✅ Webhook активен: {webhook_info['url']}")
                return webhook_info['url']
            else:
                print("❌ Webhook не установлен")
                return None
        else:
            print(f"❌ Ошибка получения информации: {result}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def main():
    """Основная функция"""
    
    print("🚀 Автоматическое развертывание Telegram бота на Render.com")
    print("=" * 60)
    
    # Проверяем текущий webhook
    print("\n🔍 Проверяем текущий webhook...")
    current_webhook = check_webhook()
    
    if current_webhook:
        print(f"📱 Бот уже настроен: {current_webhook}")
        return
    
    # Если нет API ключа Render, показываем инструкции
    if RENDER_API_KEY == "your_render_api_key":
        print("\n📋 Для автоматического развертывания:")
        print("1. Получите API ключ на https://render.com/docs/api")
        print("2. Замените 'your_render_api_key' в скрипте")
        print("3. Запустите скрипт снова")
        
        print("\n🔧 Ручное развертывание:")
        print("1. Перейдите на https://render.com")
        print("2. Создайте новый Web Service")
        print("3. Подключите ваш GitHub репозиторий")
        print("4. Укажите команду запуска: python telegram-webhook.py")
        print("5. После развертывания установите webhook:")
        
        print("\n📝 Команда для установки webhook:")
        print("curl -X POST 'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook' \\")
        print("  -H 'Content-Type: application/json' \\")
        print("  -d '{\"url\": \"https://your-service.onrender.com/webhook\"}'")
        
        return
    
    # Создаем сервис на Render
    print("\n🏗️ Создаем сервис на Render.com...")
    service_url = create_render_service()
    
    if not service_url:
        print("❌ Не удалось создать сервис")
        return
    
    # Ждем развертывания
    print("\n⏳ Ждем развертывания сервиса...")
    time.sleep(30)
    
    # Устанавливаем webhook
    print("\n🔗 Устанавливаем webhook...")
    if set_webhook(service_url):
        print("\n🎉 Бот успешно развернут и настроен!")
        print(f"📱 URL сервиса: {service_url}")
        print(f"🔗 Webhook: {service_url}/webhook")
        print("\n✅ Теперь отправьте /start вашему боту @oborotn_bot")
    else:
        print("❌ Не удалось установить webhook")

if __name__ == "__main__":
    main()
