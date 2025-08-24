# ГосЗакупки - Telegram Mini App

Telegram Mini App для агрегации государственных закупок с возможностью поиска, фильтрации, избранного и уведомлений.

## 🚀 Возможности

- **Поиск закупок** по названию, региону, цене, статусу
- **Фильтрация** по различным критериям
- **Избранное** для отслеживания интересующих закупок
- **Уведомления** об изменениях статуса и дедлайнах
- **Детальная информация** о закупках с документами
- **Мобильный интерфейс** оптимизированный для Telegram

## 🏗️ Архитектура

```
[Telegram Bot] <-> [MiniApp (React/TS)] <-> [Backend API (FastAPI)] <-> [PostgreSQL]
                                               |                
                                               +-> [Redis] (кэш, очереди)
                                               +-> [Celery] (парсеры, планировщик)
                                               +-> [Парсеры] (ЕИС, госзакупки.ру)
```

## 🛠️ Технологии

### Frontend
- React 18 + TypeScript
- Vite для сборки
- Tailwind CSS для стилизации
- Telegram WebApp SDK
- React Router для навигации
- Zustand для управления состоянием

### Backend
- FastAPI (Python)
- PostgreSQL + SQLAlchemy
- Redis для кэширования
- Celery для фоновых задач
- Парсеры для различных источников госзакупок

## 📦 Установка и запуск

### Предварительные требования

- Node.js 18+
- Python 3.9+
- PostgreSQL
- Redis

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd zakupki-telegram-mini-app
```

### 2. Frontend

```bash
# Установка зависимостей
npm install

# Запуск в режиме разработки
npm run dev

# Сборка для продакшена
npm run build
```

### 3. Backend

```bash
cd backend

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp .env.example .env
# Отредактируйте .env файл с вашими настройками

# Запуск базы данных и Redis
# (убедитесь что PostgreSQL и Redis запущены)

# Запуск FastAPI сервера
python main.py

# В отдельном терминале запуск Celery
celery -A app.tasks.celery_app worker --loglevel=info

# В отдельном терминале запуск планировщика
celery -A app.tasks.celery_app beat --loglevel=info
```

### 4. Настройка базы данных

```bash
cd backend

# Создание миграций
alembic revision --autogenerate -m "Initial migration"

# Применение миграций
alembic upgrade head
```

### 5. Настройка Telegram Bot

1. Создайте бота через @BotFather
2. Получите токен бота
3. Добавьте токен в `.env` файл
4. Настройте webhook URL

## 🔧 Конфигурация

### Переменные окружения (.env)

```env
# База данных
DATABASE_URL=postgresql://user:password@localhost:5432/zakupki_db

# Redis
REDIS_URL=redis://localhost:6379

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Безопасность
SECRET_KEY=your-secret-key-here
```

## 📱 Использование

1. Откройте бота в Telegram
2. Нажмите кнопку "Открыть приложение"
3. Используйте поиск и фильтры для поиска закупок
4. Добавляйте интересующие закупки в избранное
5. Получайте уведомления об изменениях

## 🔍 API Endpoints

### Закупки
- `GET /api/v1/purchases/` - Список закупок
- `GET /api/v1/purchases/search` - Поиск закупок
- `GET /api/v1/purchases/{id}` - Детали закупки
- `POST /api/v1/purchases/{id}/favorite` - Избранное

### Пользователи
- `GET /api/v1/users/profile` - Профиль пользователя
- `PUT /api/v1/users/settings` - Настройки пользователя

## 🚀 Развертывание

### Frontend (Vercel/Netlify)

```bash
npm run build
# Загрузите папку dist на ваш хостинг
```

### Backend (Docker)

```bash
docker-compose up -d
```

## 🤝 Разработка

### Структура проекта

```
├── src/                    # Frontend исходный код
│   ├── components/        # React компоненты
│   ├── pages/            # Страницы приложения
│   ├── hooks/            # Кастомные хуки
│   ├── contexts/         # React контексты
│   └── types/            # TypeScript типы
├── backend/               # Backend код
│   ├── app/              # Основной код приложения
│   ├── models/           # Модели базы данных
│   ├── services/         # Бизнес-логика
│   └── tasks/            # Фоновые задачи
└── docs/                 # Документация
```

### Команды разработки

```bash
# Frontend
npm run dev          # Запуск dev сервера
npm run build        # Сборка
npm run lint         # Проверка кода
npm run type-check   # Проверка типов

# Backend
python main.py       # Запуск FastAPI
celery worker        # Запуск Celery worker
alembic upgrade      # Применение миграций
```

## 📊 Мониторинг

- **Health Check**: `/health`
- **API документация**: `/docs` (Swagger UI)
- **Метрики**: Prometheus + Grafana (опционально)

## 🔒 Безопасность

- Валидация Telegram WebApp данных
- JWT токены для API
- Rate limiting
- CORS настройки

## 📝 Лицензия

MIT License

## 🤝 Поддержка

Если у вас есть вопросы или предложения, создайте issue в репозитории.

## 🚧 TODO

- [ ] Интеграция с реальными API госзакупок
- [ ] Система уведомлений
- [ ] Админ-панель
- [ ] Аналитика и метрики
- [ ] Мобильное приложение
- [ ] Интеграция с другими мессенджерами
