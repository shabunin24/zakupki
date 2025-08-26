# 🔗 Настройка Webhook для Telegram бота

## 🎯 Цель
Настроить webhook для бота @oborotn_bot, чтобы он работал через GitHub и обновлялся автоматически.

## 🚀 Варианты настройки

### Вариант 1: Ngrok (для тестирования)
```bash
# Установка ngrok
brew install ngrok

# Запуск туннеля
ngrok http 5001

# Скопируйте полученный URL (например: https://abc123.ngrok.io)
# И установите webhook:
curl -X POST "https://api.telegram.org/bot8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://abc123.ngrok.io/webhook"}'
```

### Вариант 2: Heroku (бесплатный хостинг)
```bash
# Создайте Procfile
echo "web: python telegram-webhook.py" > Procfile

# Создайте requirements.txt
echo "flask==3.1.2
requests==2.32.5" > requirements.txt

# Разверните на Heroku
heroku create your-bot-name
git push heroku main

# Установите webhook
curl -X POST "https://api.telegram.org/bot8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-bot-name.herokuapp.com/webhook"}'
```

### Вариант 3: Vercel (бесплатный хостинг)
```bash
# Создайте vercel.json
echo '{
  "version": 2,
  "builds": [
    {
      "src": "telegram-webhook.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "telegram-webhook.py"
    }
  ]
}' > vercel.json

# Разверните на Vercel
vercel --prod

# Установите webhook
curl -X POST "https://api.telegram.org/bot8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-app.vercel.app/webhook"}'
```

### Вариант 4: Railway (бесплатный хостинг)
```bash
# Создайте railway.json
echo '{
  "build": {
    "builder": "nixpacks"
  },
  "deploy": {
    "startCommand": "python telegram-webhook.py",
    "restartPolicyType": "ON_FAILURE"
  }
}' > railway.json

# Разверните на Railway
railway up

# Установите webhook
curl -X POST "https://api.telegram.org/bot8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-app.railway.app/webhook"}'
```

## 🔧 Проверка webhook

### Проверить текущий webhook:
```bash
curl "https://api.telegram.org/bot8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw/getWebhookInfo"
```

### Удалить webhook:
```bash
curl -X POST "https://api.telegram.org/bot8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw/deleteWebhook"
```

## 📱 Тестирование

После настройки webhook:

1. **Отправьте `/start` боту @oborotn_bot**
2. **Попробуйте поиск:** напишите "бумага А4 Москва до 200 тыс"
3. **Проверьте кнопки:** нажмите "🔍 Поиск закупок"

## 🚨 Важные моменты

1. **HTTPS обязателен** - Telegram требует SSL сертификат
2. **Порт 443** - стандартный HTTPS порт
3. **Публичный доступ** - сервер должен быть доступен из интернета
4. **Стабильность** - выберите надежный хостинг

## 🎯 Рекомендации

- **Для тестирования:** используйте Ngrok
- **Для продакшена:** используйте Heroku, Vercel или Railway
- **Для масштабирования:** рассмотрите AWS, Google Cloud или DigitalOcean

## 📚 Полезные ссылки

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Ngrok](https://ngrok.com/)
- [Heroku](https://heroku.com/)
- [Vercel](https://vercel.com/)
- [Railway](https://railway.app/)
