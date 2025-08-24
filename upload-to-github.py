#!/usr/bin/env python3
"""
Автоматическая загрузка Telegram Mini App в GitHub репозиторий
"""

import os
import requests
import json
import base64
from pathlib import Path

# Конфигурация
GITHUB_USERNAME = "shabunin24"
REPO_NAME = "zakupki"
BRANCH = "main"

# Файлы для загрузки
FILES_TO_UPLOAD = [
    "index.html",
    "styles.css", 
    "script.js",
    "config.js",
    "README.md",
    "QUICKSTART.md",
    "package.json",
    "start-server.py",
    "test.html",
    ".gitignore"
]

def create_github_token():
    """Создание GitHub токена через веб-интерфейс"""
    print("🔐 Для загрузки в GitHub нужен Personal Access Token")
    print("📝 Создайте токен по ссылке:")
    print(f"https://github.com/settings/tokens/new?description=Zakupki%20Bot&scopes=repo")
    print()
    print("✅ Выберите права 'repo' (полный доступ к репозиториям)")
    print("📋 Скопируйте токен и вставьте его ниже:")
    
    token = input("🔑 Введите ваш GitHub токен: ").strip()
    return token

def upload_file_to_github(token, file_path, content, message):
    """Загрузка файла в GitHub через API"""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{file_path}"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "message": message,
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
        "branch": BRANCH
    }
    
    try:
        response = requests.put(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            print(f"✅ {file_path} - загружен успешно")
            return True
        else:
            print(f"❌ {file_path} - ошибка: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
    except Exception as e:
        print(f"❌ {file_path} - исключение: {e}")
        return False

def main():
    print("🚀 Автоматическая загрузка Telegram Mini App в GitHub")
    print(f"📁 Репозиторий: {GITHUB_USERNAME}/{REPO_NAME}")
    print()
    
    # Получаем токен
    token = create_github_token()
    if not token:
        print("❌ Токен не введен. Загрузка отменена.")
        return
    
    print()
    print("📤 Начинаем загрузку файлов...")
    print()
    
    success_count = 0
    total_files = len(FILES_TO_UPLOAD)
    
    for filename in FILES_TO_UPLOAD:
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                message = f"🚀 Добавлен {filename} - Telegram Mini App ГосЗакупки"
                
                if upload_file_to_github(token, filename, content, message):
                    success_count += 1
                
            except Exception as e:
                print(f"❌ Ошибка чтения {filename}: {e}")
        else:
            print(f"⚠️  Файл {filename} не найден")
    
    print()
    print("📊 Результат загрузки:")
    print(f"✅ Успешно: {success_count}/{total_files}")
    print(f"❌ Ошибок: {total_files - success_count}")
    
    if success_count > 0:
        print()
        print("🎉 Загрузка завершена!")
        print(f"🌐 Ваше приложение доступно по адресу:")
        print(f"   https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
        print()
        print("📱 Следующие шаги:")
        print("1. Включите GitHub Pages в настройках репозитория")
        print("2. Получите HTTPS URL для Mini App")
        print("3. Настройте бота через @BotFather")
    else:
        print()
        print("❌ Загрузка не удалась. Проверьте токен и права доступа.")

if __name__ == "__main__":
    main()
