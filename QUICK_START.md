# 🚀 Быстрый запуск Telegram бота ГосЗакупки

## ⚡ За 5 минут к работающему боту!

### 🎯 Что у вас уже есть:
- ✅ Бот полностью обновлен и готов
- ✅ GitHub Pages настроен
- ✅ Все файлы для развертывания созданы
- ✅ Автоматические скрипты готовы

### 🚀 Вариант 1: Render.com (рекомендуется)

#### Шаг 1: Развертывание
1. Перейдите на [https://render.com](https://render.com)
2. Нажмите "New +" → "Web Service"
3. Подключите GitHub репозиторий: `shabunin24/zakupki`
4. Настройки:
   - **Name:** `telegram-bot-goszakupki`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python telegram-webhook.py`
5. Нажмите "Create Web Service"

#### Шаг 2: Установка webhook
После развертывания (5-10 минут) скопируйте URL сервиса и выполните:

```bash
curl -X POST 'https://api.telegram.org/bot8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw/setWebhook' \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://your-service.onrender.com/webhook"}'
```

### 🚀 Вариант 2: Heroku

#### Шаг 1: Установка CLI
```bash
brew install heroku/brew/heroku
```

#### Шаг 2: Развертывание
```bash
heroku create your-bot-name
git push heroku main
```

#### Шаг 3: Установка webhook
```bash
curl -X POST 'https://api.telegram.org/bot8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw/setWebhook' \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://your-bot-name.herokuapp.com/webhook"}'
```

### 🚀 Вариант 3: Vercel

#### Шаг 1: Установка CLI
```bash
npm i -g vercel
```

#### Шаг 2: Развертывание
```bash
vercel --prod
```

#### Шаг 3: Установка webhook
```bash
curl -X POST 'https://api.telegram.org/bot8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw/setWebhook' \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://your-app.vercel.app/webhook"}'
```

## 🧪 Тестирование

### 1. Проверьте webhook:
```bash
curl 'https://api.telegram.org/bot8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw/getWebhookInfo'
```

### 2. Отправьте `/start` боту @oborotn_bot

### 3. Попробуйте поиск: "бумага А4 Москва до 200 тыс"

## 🔧 Автоматизация

### Запустите скрипт настройки:
```bash
./setup-webhook.sh
```

### Автоматическое развертывание на Render:
```bash
python3 deploy-render.py
```
*(Требует API ключ Render)*

## 🎉 Результат

После настройки ваш бот будет:
- ✅ Получать сообщения от пользователей
- ✅ Отвечать с новыми функциями поиска
- ✅ Открывать красивый поиск через GitHub Pages
- ✅ Автоматически обновляться при изменениях в GitHub

## 🆘 Если что-то не работает

### Проверьте:
1. **Webhook установлен** - используйте команду проверки выше
2. **Сервис запущен** - проверьте статус на хостинге
3. **Логи сервиса** - посмотрите ошибки в консоли хостинга

### Полезные команды:
```bash
# Удалить webhook
curl -X POST 'https://api.telegram.org/bot8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw/deleteWebhook'

# Проверить бота
curl 'https://api.telegram.org/bot8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw/getMe'
```

## 📱 Готово!

**Ваш бот готов к работе и будет обновляться автоматически! 🚀**

Просто выберите один из вариантов развертывания выше, и через 5-10 минут у вас будет работающий бот с новыми функциями.
