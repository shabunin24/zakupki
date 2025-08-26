#!/bin/bash

# Скрипт для запуска UniversalProcureSearch сервера
echo "🚀 Запуск UniversalProcureSearch сервера..."

# Активируем виртуальное окружение
source ".venv/bin/activate"

# Переходим в папку с приложением
cd "apps/universal-procure"

# Запускаем сервер
echo "📍 Сервер запускается на http://localhost:8000"
echo "📝 Для остановки нажмите Ctrl+C"
echo ""

python3 app.py
