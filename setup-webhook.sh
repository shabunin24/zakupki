#!/bin/bash

# Скрипт для настройки webhook Telegram бота
echo "🔗 Настройка webhook для Telegram бота ГосЗакупки"
echo "=================================================="

# Проверяем текущий webhook
echo ""
echo "🔍 Проверяем текущий webhook..."
WEBHOOK_INFO=$(curl -s "https://api.telegram.org/bot8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw/getWebhookInfo")
echo "Текущий webhook: $WEBHOOK_INFO"

echo ""
echo "📋 Варианты настройки webhook:"
echo ""
echo "1️⃣ Ngrok (быстрое тестирование):"
echo "   - Установите ngrok: brew install ngrok"
echo "   - Зарегистрируйтесь на https://ngrok.com"
echo "   - Получите authtoken и настройте: ngrok config add-authtoken YOUR_TOKEN"
echo "   - Запустите: ngrok http 5001"
echo "   - Скопируйте HTTPS URL и установите webhook"
echo ""
echo "2️⃣ Render.com (бесплатный хостинг):"
echo "   - Перейдите на https://render.com"
echo "   - Создайте новый Web Service"
echo "   - Подключите GitHub репозиторий: shabunin24/zakupki"
echo "   - Команда запуска: python telegram-webhook.py"
echo "   - После развертывания установите webhook"
echo ""
echo "3️⃣ Heroku (бесплатный хостинг):"
echo "   - Установите Heroku CLI"
echo "   - Создайте приложение: heroku create your-bot-name"
echo "   - Разверните: git push heroku main"
echo "   - Установите webhook"
echo ""
echo "4️⃣ Vercel (бесплатный хостинг):"
echo "   - Установите Vercel CLI: npm i -g vercel"
echo "   - Разверните: vercel --prod"
echo "   - Установите webhook"
echo ""

echo "🚀 После развертывания используйте команду:"
echo ""
echo "curl -X POST 'https://api.telegram.org/bot8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw/setWebhook' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"url\": \"https://your-service-url.com/webhook\"}'"
echo ""

echo "🔧 Проверить webhook:"
echo "curl 'https://api.telegram.org/bot8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw/getWebhookInfo'"
echo ""

echo "🗑️ Удалить webhook:"
echo "curl -X POST 'https://api.telegram.org/bot8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw/deleteWebhook'"
echo ""

echo "📱 После настройки webhook отправьте /start боту @oborotn_bot"
