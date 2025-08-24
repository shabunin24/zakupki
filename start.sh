#!/bin/bash

echo "🚀 Запуск проекта ГосЗакупки..."

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker и попробуйте снова."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Установите Docker Compose и попробуйте снова."
    exit 1
fi

# Проверка наличия Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js не установлен. Установите Node.js и попробуйте снова."
    exit 1
fi

# Проверка версии Node.js
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Требуется Node.js версии 18 или выше. Текущая версия: $(node -v)"
    exit 1
fi

echo "✅ Проверки пройдены"

# Сборка frontend
echo "📦 Сборка frontend..."
cd frontend || mkdir -p frontend
npm install
npm run build
cd ..

# Создание необходимых папок
mkdir -p logs
mkdir -p ssl

# Запуск через Docker Compose
echo "🐳 Запуск через Docker Compose..."
docker-compose up -d

echo "⏳ Ожидание запуска сервисов..."
sleep 10

# Проверка статуса сервисов
echo "📊 Статус сервисов:"
docker-compose ps

echo ""
echo "🎉 Проект запущен!"
echo ""
echo "📱 Frontend: http://localhost"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API документация: http://localhost:8000/docs"
echo "💾 База данных: localhost:5432"
echo "🔴 Redis: localhost:6379"
echo ""
echo "📋 Полезные команды:"
echo "  docker-compose logs -f backend    # Логи backend"
echo "  docker-compose logs -f celery     # Логи Celery"
echo "  docker-compose down               # Остановка всех сервисов"
echo "  docker-compose restart backend    # Перезапуск backend"
echo ""
echo "🔍 Для остановки проекта выполните: docker-compose down"
