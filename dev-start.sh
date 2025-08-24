#!/bin/bash

echo "🚀 Запуск проекта ГосЗакупки в режиме разработки..."

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

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не установлен. Установите Python 3 и попробуйте снова."
    exit 1
fi

echo "✅ Проверки пройдены"

# Установка зависимостей frontend
echo "📦 Установка зависимостей frontend..."
npm install

# Установка зависимостей backend
echo "🐍 Установка зависимостей backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения Python..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
cd ..

echo ""
echo "🎯 Режим разработки готов!"
echo ""
echo "📱 Для запуска frontend выполните: npm run dev"
echo "🔧 Для запуска backend выполните: cd backend && source venv/bin/activate && python main.py"
echo ""
echo "📋 Полезные команды:"
echo "  npm run dev          # Запуск frontend dev сервера"
echo "  npm run build        # Сборка frontend"
echo "  npm run lint         # Проверка кода"
echo "  npm run type-check   # Проверка типов"
echo ""
echo "🔍 Frontend будет доступен по адресу: http://localhost:3000"
echo "🔍 Backend будет доступен по адресу: http://localhost:8000"
