#!/bin/bash

# Скрипт для запуска обновленного Telegram бота ГосЗакупки
echo "🤖 Запуск обновленного Telegram бота ГосЗакупки..."

# Проверяем, что API поиска запущен
echo "🔍 Проверяем API поиска..."
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ API поиска работает на порту 8000"
else
    echo "❌ API поиска не запущен на порту 8000"
    echo "🚀 Сначала запустите API поиска:"
    echo "   ./start-procure-server.sh"
    exit 1
fi

# Активируем виртуальное окружение
source ".venv/bin/activate"

# Устанавливаем webhook для бота
echo "🔗 Устанавливаем webhook для бота..."
python3 -c "
import requests
import json

bot_token = '8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw'
webhook_url = 'https://your-domain.com/webhook'  # Замените на ваш домен

response = requests.post(f'https://api.telegram.org/bot{bot_token}/setWebhook', json={
    'url': webhook_url,
    'allowed_updates': ['message', 'callback_query']
})

result = response.json()
if result.get('ok'):
    print(f'✅ Webhook установлен: {webhook_url}')
else:
    print(f'❌ Ошибка установки webhook: {result}')
"

echo ""
echo "🚀 Запуск webhook сервера на порту 5000..."
echo "📱 Отправьте /start вашему боту @oborotn_bot для тестирования"
echo ""

# Запускаем бота
python3 telegram-webhook.py
