#!/usr/bin/env python3
"""
Автоматическое включение GitHub Pages для репозитория
"""

import requests
import json

# Конфигурация
GITHUB_USERNAME = "shabunin24"
REPO_NAME = "zakupki"
TOKEN = "YOUR_GITHUB_TOKEN_HERE"  # Замените на ваш токен

def enable_github_pages():
    """Включение GitHub Pages"""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/pages"
    
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "source": {
            "branch": "main",
            "path": "/"
        }
    }
    
    try:
        print("🔧 Включаем GitHub Pages...")
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            print("✅ GitHub Pages успешно включен!")
            print("📱 URL будет доступен через несколько минут:")
            print(f"   https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/")
            return True
        elif response.status_code == 409:
            print("⚠️  GitHub Pages уже включен или в процессе активации")
            return True
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return False

def check_pages_status():
    """Проверка статуса GitHub Pages"""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/pages"
    
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("📊 Статус GitHub Pages:")
            print(f"   URL: {data.get('url', 'Не указан')}")
            print(f"   Статус: {data.get('status', 'Неизвестен')}")
            print(f"   Источник: {data.get('source', {}).get('branch', 'Не указан')}")
            return data
        else:
            print(f"❌ Не удалось получить статус: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка проверки статуса: {e}")
        return None

def main():
    print("🚀 Активация GitHub Pages для Telegram Mini App")
    print(f"📁 Репозиторий: {GITHUB_USERNAME}/{REPO_NAME}")
    print()
    
    # Включаем GitHub Pages
    if enable_github_pages():
        print()
        print("⏳ Ждем активации...")
        
        # Проверяем статус
        import time
        time.sleep(5)
        
        print()
        check_pages_status()
        
        print()
        print("📱 Следующие шаги:")
        print("1. Подождите 5-10 минут для полной активации")
        print("2. Проверьте доступность по URL выше")
        print("3. Настройте Mini App через @BotFather")
        print("4. Протестируйте бота в Telegram")
    else:
        print("❌ Не удалось включить GitHub Pages")

if __name__ == "__main__":
    main()
