#!/usr/bin/env python3
"""
Мониторинг статуса GitHub Pages
"""

import requests
import time
import os

# Конфигурация
GITHUB_USERNAME = "shabunin24"
REPO_NAME = "zakupki"
TOKEN = "YOUR_GITHUB_TOKEN_HERE"  # Замените на ваш токен

def check_pages_status():
    """Проверка статуса GitHub Pages через API"""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/pages"
    
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"❌ API вернул код: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка API: {e}")
        return None

def check_pages_url():
    """Проверка доступности GitHub Pages по URL"""
    url = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/"
    
    try:
        response = requests.get(url, timeout=10)
        return response.status_code
    except Exception as e:
        return f"Ошибка: {e}"

def main():
    print("🔍 МОНИТОРИНГ GITHUB PAGES")
    print("=" * 50)
    print(f"📁 Репозиторий: {GITHUB_USERNAME}/{REPO_NAME}")
    print(f"🌐 Ожидаемый URL: https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/")
    print()
    
    check_count = 0
    max_checks = 20  # Максимум 20 проверок
    
    while check_count < max_checks:
        check_count += 1
        current_time = time.strftime("%H:%M:%S")
        
        print(f"🔍 Проверка #{check_count} [{current_time}]")
        
        # Проверяем статус через API
        api_status = check_pages_status()
        if api_status:
            status = api_status.get('status', 'Неизвестен')
            print(f"   📊 API статус: {status}")
            
            if status == 'built':
                print("✅ GitHub Pages готов!")
                break
            elif status == 'building':
                print("⏳ GitHub Pages в процессе сборки...")
            elif status == 'errored':
                print("❌ Ошибка сборки GitHub Pages")
                break
        else:
            print("   ❌ Не удалось получить статус API")
        
        # Проверяем доступность по URL
        url_status = check_pages_url()
        if url_status == 200:
            print("✅ GitHub Pages доступен по URL!")
            break
        elif isinstance(url_status, int):
            print(f"   🌐 URL статус: {url_status}")
        else:
            print(f"   🌐 URL ошибка: {url_status}")
        
        print()
        
        if check_count < max_checks:
            print("⏳ Ждем 30 секунд до следующей проверки...")
            time.sleep(30)
    
    print()
    print("📊 ФИНАЛЬНЫЙ СТАТУС")
    print("=" * 50)
    
    # Финальная проверка
    final_api = check_pages_status()
    final_url = check_pages_url()
    
    if final_api:
        print(f"📊 API статус: {final_api.get('status', 'Неизвестен')}")
        print(f"🌐 URL статус: {final_url}")
        
        if final_url == 200:
            print("🎉 GITHUB PAGES АКТИВИРОВАН!")
            print()
            print("📱 СЛЕДУЮЩИЕ ШАГИ:")
            print("1. ✅ GitHub Pages готов")
            print("2. 🔧 Настройте Mini App через @BotFather")
            print("3. 🧪 Протестируйте бота в Telegram")
            print()
            print("🔗 Полезные ссылки:")
            print(f"   • GitHub Pages: https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/")
            print(f"   • GitHub репозиторий: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
            print("   • BotFather: @BotFather")
        else:
            print("⏳ GitHub Pages еще не готов")
            print("   Подождите еще несколько минут и проверьте снова")
    else:
        print("❌ Не удалось получить статус GitHub Pages")

if __name__ == "__main__":
    main()
