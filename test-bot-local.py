#!/usr/bin/env python3
"""
Локальный тест бота ГосЗакупки без webhook
Показывает, как будут выглядеть сообщения бота
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
                        "url": "http://localhost:3000"  # Замените на ваш URL
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

def send_test_message(chat_id, text, reply_markup=None):
    """Отправляет тестовое сообщение"""
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

def test_start_command(chat_id):
    """Тестирует команду /start"""
    welcome_text = f"""
🎉 <b>Добро пожаловать в ГосЗакупки!</b>

👋 Привет, пользователь!

🔍 <b>Что умеет бот:</b>
• Поиск государственных закупок
• Фильтрация по регионам и категориям
• Отслеживание избранных закупок
• Уведомления о новых закупках
• Детальная информация о закупках

🚀 <b>Нажмите кнопку ниже, чтобы открыть приложение:</b>
    """
    
    keyboard = create_mini_app_keyboard()
    return send_test_message(chat_id, welcome_text, keyboard)

def test_search_response(chat_id):
    """Тестирует ответ на поиск"""
    text = "🔍 <b>Поиск закупок</b>\n\nОткройте приложение для поиска закупок с расширенными фильтрами."
    keyboard = create_mini_app_keyboard()
    return send_test_message(chat_id, text, keyboard)

def test_favorites_response(chat_id):
    """Тестирует ответ на избранное"""
    text = "⭐ <b>Избранное</b>\n\nОткройте приложение для просмотра избранных закупок."
    keyboard = create_mini_app_keyboard()
    return send_test_message(chat_id, text, keyboard)

def test_help_response(chat_id):
    """Тестирует справку"""
    help_text = """
ℹ️ <b>Справка по боту ГосЗакупки</b>

🔍 <b>Основные функции:</b>
• <b>Поиск закупок</b> - найдите интересующие вас закупки
• <b>Фильтры</b> - по региону, цене, статусу, методу закупки
• <b>Избранное</b> - сохраняйте важные закупки
• <b>Уведомления</b> - получайте уведомления о новых закупках

📱 <b>Как использовать:</b>
1. Нажмите "🚀 Открыть ГосЗакупки"
2. В открывшемся приложении используйте поиск и фильтры
3. Добавляйте закупки в избранное
4. Настраивайте уведомления

🌐 <b>Источники данных:</b>
• ЕИС (zakupki.gov.ru)
• Региональные порталы закупок
• Другие официальные источники

📞 <b>Поддержка:</b>
Если у вас есть вопросы, обратитесь к разработчику.
    """
    keyboard = create_mini_app_keyboard()
    return send_test_message(chat_id, help_text, keyboard)

def main():
    print("🧪 Локальный тест бота ГосЗакупки")
    print("=" * 40)
    
    # Запрашиваем ID чата для тестирования
    print("📱 Для тестирования бота нужно:")
    print("1. Откройте @oborotn_bot в Telegram")
    print("2. Отправьте любое сообщение")
    print("3. Скопируйте ID чата из URL или используйте @userinfobot")
    
    chat_id = input("\nВведите ID чата для тестирования: ").strip()
    
    if not chat_id:
        print("❌ ID чата не указан")
        return
    
    try:
        chat_id = int(chat_id)
    except ValueError:
        print("❌ ID чата должен быть числом")
        return
    
    print(f"\n🎯 Тестирую бота в чате {chat_id}")
    print("=" * 40)
    
    # Тестируем все функции
    print("\n1️⃣ Тестирую команду /start...")
    test_start_command(chat_id)
    
    print("\n2️⃣ Тестирую ответ на поиск...")
    test_search_response(chat_id)
    
    print("\n3️⃣ Тестирую ответ на избранное...")
    test_favorites_response(chat_id)
    
    print("\n4️⃣ Тестирую справку...")
    test_help_response(chat_id)
    
    print("\n✅ Тест завершен!")
    print("\n📱 Теперь в Telegram:")
    print("• Откройте чат с ботом")
    print("• Нажмите на кнопку '🚀 Открыть ГосЗакупки'")
    print("• Должно открыться ваше приложение")

if __name__ == "__main__":
    main()
