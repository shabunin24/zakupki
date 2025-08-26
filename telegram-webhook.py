#!/usr/bin/env python3
"""
Telegram Webhook сервер для бота ГосЗакупки
Обрабатывает сообщения и показывает Mini App
Интегрирован с GitHub Pages
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

# GitHub Pages URL
GITHUB_PAGES_URL = "https://shabunin24.github.io/zakupki"

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
                        "url": f"{GITHUB_PAGES_URL}/"
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

def create_search_keyboard():
    """Создает клавиатуру для поиска"""
    return {
        "inline_keyboard": [
            [
                {
                    "text": "📝 Ввести запрос",
                    "callback_data": "input_query"
                }
            ],
            [
                {
                    "text": "🔍 Быстрый поиск",
                    "callback_data": "quick_search"
                }
            ],
            [
                {
                    "text": "⬅️ Назад",
                    "callback_data": "back_to_main"
                }
            ]
        ]
    }

def create_quick_search_keyboard():
    """Создает клавиатуру для быстрого поиска"""
    return {
        "inline_keyboard": [
            [
                {
                    "text": "📄 Канцелярия",
                    "callback_data": "search_office"
                },
                {
                    "text": "🏗️ Строительство",
                    "callback_data": "search_construction"
                }
            ],
            [
                {
                    "text": "💻 IT услуги",
                    "callback_data": "search_it"
                },
                {
                    "text": "🏥 Медицина",
                    "callback_data": "search_medical"
                }
            ],
            [
                {
                    "text": "⬅️ Назад",
                    "callback_data": "back_to_search"
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
• Поиск государственных закупок по естественному языку
• Фильтрация по регионам и категориям
• Отслеживание избранных закупок
• Уведомления о новых закупках
• Детальная информация о закупках

🚀 <b>Нажмите кнопку ниже, чтобы открыть приложение:</b>
    """
    
    keyboard = create_mini_app_keyboard()
    send_telegram_message(chat_id, welcome_text, keyboard)

def handle_search_query(chat_id, query):
    """Обрабатывает поисковый запрос"""
    # Формируем ответ с ссылкой на поиск
    response_text = f"🔍 <b>Поиск закупок:</b> <i>'{query}'</i>\n\n"
    response_text += "📱 <b>Откройте приложение для поиска с вашим запросом</b>\n\n"
    response_text += "💡 <b>Приложение автоматически:</b>\n"
    response_text += "• Поймет ваш запрос на естественном языке\n"
    response_text += "• Определит категорию товаров/услуг\n"
    response_text += "• Найдет подходящие регионы\n"
    response_text += "• Покажет ценовые диапазоны\n"
    response_text += "• Отфильтрует по методам закупок"
    
    # Создаем клавиатуру для открытия приложения с поиском
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "🚀 Открыть поиск",
                    "web_app": {
                        "url": f"{GITHUB_PAGES_URL}/?search={query}"
                    }
                }
            ],
            [
                {
                    "text": "🔍 Новый поиск",
                    "callback_data": "search"
                }
            ]
        ]
    }
    
    send_telegram_message(chat_id, response_text, keyboard)

def handle_callback_query(callback_query):
    """Обрабатывает нажатия на inline кнопки"""
    chat_id = callback_query["message"]["chat"]["id"]
    data = callback_query["data"]
    
    if data == "search":
        text = "🔍 <b>Поиск закупок</b>\n\nВыберите способ поиска:"
        keyboard = create_search_keyboard()
        send_telegram_message(chat_id, text, keyboard)
        
    elif data == "input_query":
        text = "📝 <b>Введите ваш запрос</b>\n\nПримеры:\n• бумага А4 офисная Москва до 200 тыс руб\n• услуги по строительству дорог Крым от 5 до 20 млн\n• поставка медоборудования Москва конкурс\n\n<i>Просто напишите ваш запрос в чат</i>"
        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "⬅️ Назад",
                        "callback_data": "back_to_search"
                    }
                ]
            ]
        }
        send_telegram_message(chat_id, text, keyboard)
        
    elif data == "quick_search":
        text = "🔍 <b>Быстрый поиск</b>\n\nВыберите категорию:"
        keyboard = create_quick_search_keyboard()
        send_telegram_message(chat_id, text, keyboard)
        
    elif data == "search_office":
        handle_search_query(chat_id, "канцелярские товары")
        
    elif data == "search_construction":
        handle_search_query(chat_id, "услуги по строительству дорог")
        
    elif data == "search_it":
        handle_search_query(chat_id, "IT услуги разработка программного обеспечения")
        
    elif data == "search_medical":
        handle_search_query(chat_id, "медицинское оборудование")
        
    elif data == "back_to_search":
        text = "🔍 <b>Поиск закупок</b>\n\nВыберите способ поиска:"
        keyboard = create_search_keyboard()
        send_telegram_message(chat_id, text, keyboard)
        
    elif data == "back_to_main":
        text = "🔍 <b>ГосЗакупки</b>\n\nВыберите действие:"
        keyboard = create_mini_app_keyboard()
        send_telegram_message(chat_id, text, keyboard)
        
    elif data == "favorites":
        text = "⭐ <b>Избранные закупки</b>\n\nОткройте приложение для просмотра избранных закупок:"
        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "🚀 Открыть избранное",
                        "web_app": {
                            "url": f"{GITHUB_PAGES_URL}/favorites"
                        }
                    }
                ],
                [
                    {
                        "text": "⬅️ Назад",
                        "callback_data": "back_to_main"
                    }
                ]
            ]
        }
        send_telegram_message(chat_id, text, keyboard)
        
    elif data == "help":
        help_text = """
ℹ️ <b>Помощь по использованию бота</b>

🔍 <b>Поиск закупок:</b>
• Напишите запрос на естественном языке
• Используйте быстрые категории
• Фильтруйте по региону, цене, методу

📱 <b>Mini App:</b>
• Полнофункциональное веб-приложение
• Расширенные фильтры
• Сохранение избранного
• Уведомления

💡 <b>Примеры запросов:</b>
• "бумага А4 офисная Москва до 200 тыс руб"
• "услуги по строительству дорог Крым от 5 до 20 млн"
• "поставка медоборудования Москва конкурс"

🆘 <b>Поддержка:</b>
Если у вас есть вопросы, обратитесь к разработчику.
        """
        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "🚀 Открыть приложение",
                        "web_app": {
                            "url": f"{GITHUB_PAGES_URL}/"
                        }
                    }
                ],
                [
                    {
                        "text": "⬅️ Назад",
                        "callback_data": "back_to_main"
                    }
                ]
            ]
        }
        send_telegram_message(chat_id, help_text, keyboard)

def handle_message(message):
    """Обрабатывает входящие сообщения"""
    chat_id = message["chat"]["id"]
    
    if "text" in message:
        text = message["text"]
        
        if text.startswith("/start"):
            user_info = message.get("from", {})
            handle_start_command(chat_id, user_info)
        else:
            # Обрабатываем как поисковый запрос
            handle_search_query(chat_id, text)
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
    return jsonify({
        "status": "healthy", 
        "bot": BOT_USERNAME,
        "github_pages": GITHUB_PAGES_URL
    })

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
    print(f"🌐 GitHub Pages: {GITHUB_PAGES_URL}")
    
    # Запускаем сервер
    print("🚀 Запуск webhook сервера...")
    print("📱 Отправьте /start вашему боту для тестирования")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
