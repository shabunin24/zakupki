#!/usr/bin/env python3
"""
Скрипт для принудительного обновления GitHub Pages
"""

import os
import subprocess
import time

def run_command(command, description):
    """Выполняет команду и выводит результат"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} выполнено успешно")
            if result.stdout:
                print(f"📤 Вывод: {result.stdout.strip()}")
        else:
            print(f"❌ {description} не выполнено")
            if result.stderr:
                print(f"🚨 Ошибка: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Ошибка выполнения команды: {e}")
        return False

def main():
    print("🚀 Принудительное обновление GitHub Pages")
    print("=" * 50)
    
    # Проверяем статус git
    if not run_command("git status", "Проверка статуса Git"):
        print("❌ Не удалось проверить статус Git")
        return
    
    # Добавляем все изменения
    if not run_command("git add .", "Добавление изменений в Git"):
        print("❌ Не удалось добавить изменения")
        return
    
    # Проверяем, есть ли изменения для коммита
    result = subprocess.run("git diff --cached --name-only", shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print("ℹ️ Нет изменений для коммита")
    else:
        print(f"📝 Изменения для коммита:\n{result.stdout}")
        
        # Коммитим изменения
        if not run_command('git commit -m "🔄 Принудительное обновление GitHub Pages"', "Создание коммита"):
            print("❌ Не удалось создать коммит")
            return
    
    # Отправляем изменения на GitHub
    if not run_command("git push origin main", "Отправка изменений на GitHub"):
        print("❌ Не удалось отправить изменения")
        return
    
    print("\n⏳ Ожидание обновления GitHub Pages...")
    print("💡 GitHub Pages обычно обновляется в течение 1-5 минут")
    
    # Проверяем обновление через несколько минут
    for i in range(3):
        print(f"\n🔄 Проверка обновления #{i+1}...")
        time.sleep(60)  # Ждем 1 минуту
        
        # Проверяем, обновилась ли страница
        try:
            import requests
            response = requests.get("https://shabunin24.github.io/zakupki/", timeout=10)
            if "🏛️ ГосЗакупки" in response.text:
                print("✅ GitHub Pages обновлен! Новый интерфейс доступен!")
                break
            else:
                print("⏳ GitHub Pages еще не обновился...")
        except Exception as e:
            print(f"⚠️ Не удалось проверить обновление: {e}")
    
    print("\n🎯 Что делать дальше:")
    print("1. Подождите 5-10 минут для полного обновления")
    print("2. Откройте https://shabunin24.github.io/zakupki/")
    print("3. Проверьте, что видите новый интерфейс")
    print("4. Протестируйте в Telegram боте @oborotn_bot")
    
    print("\n🔗 Полезные ссылки:")
    print("• GitHub Pages: https://shabunin24.github.io/zakupki/")
    print("• Избранное: https://shabunin24.github.io/zakupki/favorites.html")
    print("• Детали закупки: https://shabunin24.github.io/zakupki/purchase-detail.html")

if __name__ == "__main__":
    main()
