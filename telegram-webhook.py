#!/usr/bin/env python3
"""
Telegram Webhook сервер для бота ГосЗакупки
Обрабатывает сообщения и показывает Mini App
"""

import json
import requests
from flask import Flask, request, jsonify
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация бота
BOT_TOKEN = "8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw"
BOT_USERNAME = "oborotn_bot"
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Создаем Flask приложение
app = Flask(__name__)

def send_telegram_message(chat_id, text, reply_markup=None):
    """Отправляет сообщение в Telegram"""
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
        return response.json()
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения: {e}")
        return None

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

def handle_start_command(chat_id, user_info):
    """Обрабатывает команду /start"""
    welcome_text = f"""
🎉 <b>Добро пожаловать в ГосЗакупки!</b>

👋 Привет, {user_info.get('first_name', 'пользователь')}!

🔍 <b>Что умеет бот:</b>
• Поиск государственных закупок
• Фильтрация по регионам и категориям
• Отслеживание избранных закупок
• Уведомления о новых закупках
• Детальная информация о закупках

🚀 <b>Нажмите кнопку ниже, чтобы открыть приложение:</b>
    """
    
    keyboard = create_mini_app_keyboard()
    send_telegram_message(chat_id, welcome_text, keyboard)

def handle_callback_query(callback_query):
    """Обрабатывает нажатия на inline кнопки"""
    chat_id = callback_query["message"]["chat"]["id"]
    data = callback_query["data"]
    
    if data == "search":
        text = "🔍 <b>Поиск закупок</b>\n\nОткройте приложение для поиска закупок с расширенными фильтрами."
        keyboard = create_mini_app_keyboard()
        send_telegram_message(chat_id, text, keyboard)
    
    elif data == "favorites":
        text = "⭐ <b>Избранное</b>\n\nОткройте приложение для просмотра избранных закупок."
        keyboard = create_mini_app_keyboard()
        send_telegram_message(chat_id, text, keyboard)
    
    elif data == "help":
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
        send_telegram_message(chat_id, help_text, keyboard)

def handle_message(message):
    """Обрабатывает входящие сообщения"""
    chat_id = message["chat"]["id"]
    user_info = message.get("from", {})
    text = message.get("text", "").strip()
    
    logger.info(f"Получено сообщение от {user_info.get('username', 'Unknown')}: {text}")
    
    if text == "/start":
        handle_start_command(chat_id, user_info)
    elif text.lower() in ["привет", "hello", "hi"]:
        welcome_text = f"👋 Привет, {user_info.get('first_name', 'пользователь')}! Нажмите кнопку ниже, чтобы открыть приложение ГосЗакупки."
        keyboard = create_mini_app_keyboard()
        send_telegram_message(chat_id, welcome_text, keyboard)
    else:
        # Для любого другого сообщения показываем главное меню
        text = "🔍 <b>ГосЗакупки</b>\n\nВыберите действие:"
        keyboard = create_mini_app_keyboard()
        send_telegram_message(chat_id, text, keyboard)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обрабатывает webhook от Telegram"""
    try:
        data = request.get_json()
        logger.info(f"Получен webhook: {data}")
        
        if "message" in data:
            handle_message(data["message"])
        elif "callback_query" in data:
            handle_callback_query(data["callback_query"])
        
        return jsonify({"status": "ok"})
    
    except Exception as e:
        logger.error(f"Ошибка обработки webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка здоровья сервера"""
    return jsonify({"status": "healthy", "bot": BOT_USERNAME})

def set_webhook(url):
    """Устанавливает webhook для бота"""
    webhook_url = f"{url}/webhook"
    
    try:
        response = requests.post(f"{API_BASE}/setWebhook", json={
            "url": webhook_url,
            "allowed_updates": ["message", "callback_query"]
        })
        
        result = response.json()
        if result.get("ok"):
            logger.info(f"Webhook успешно установлен: {webhook_url}")
            return True
        else:
            logger.error(f"Ошибка установки webhook: {result}")
            return False
            
    except Exception as e:
        logger.error(f"Ошибка установки webhook: {e}")
        return False

def delete_webhook():
    """Удаляет webhook"""
    try:
        response = requests.post(f"{API_BASE}/deleteWebhook")
        result = response.json()
        if result.get("ok"):
            logger.info("Webhook удален")
            return True
        else:
            logger.error(f"Ошибка удаления webhook: {result}")
            return False
            
    except Exception as e:
        logger.error(f"Ошибка удаления webhook: {e}")
        return False

def get_bot_info():
    """Получает информацию о боте"""
    try:
        response = requests.get(f"{API_BASE}/getMe")
        result = response.json()
        if result.get("ok"):
            bot_info = result["result"]
            logger.info(f"Бот: @{bot_info['username']} ({bot_info['first_name']})")
            return bot_info
        else:
            logger.error(f"Ошибка получения информации о боте: {result}")
            return None
            
    except Exception as e:
        logger.error(f"Ошибка получения информации о боте: {e}")
        return None

if __name__ == "__main__":
    # Получаем информацию о боте
    bot_info = get_bot_info()
    if not bot_info:
        print("❌ Не удалось получить информацию о боте")
        exit(1)
    
    print(f"🤖 Бот: @{bot_info['username']} ({bot_info['first_name']})")
    print(f"🔗 API: {API_BASE}")
    
    # Запускаем сервер
    print("🚀 Запуск webhook сервера...")
    print("📱 Отправьте /start вашему боту для тестирования")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
