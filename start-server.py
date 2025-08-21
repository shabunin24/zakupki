#!/usr/bin/env python3
"""
Простой HTTP сервер для тестирования Telegram Mini App
Запускает локальный сервер на порту 8000
"""

import http.server
import socketserver
import webbrowser
import os
from urllib.parse import urlparse

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Добавляем CORS заголовки для тестирования
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Обработка preflight запросов
        self.send_response(200)
        self.end_headers()

def main():
    # Проверяем наличие файлов
    required_files = ['index.html', 'styles.css', 'script.js', 'config.js']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Отсутствуют файлы: {', '.join(missing_files)}")
        return
    
    # Создаем сервер
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"🚀 Сервер запущен на http://localhost:{PORT}")
        print(f"📱 Откройте http://localhost:{PORT}/test.html для тестирования")
        print(f"🔗 Основное приложение: http://localhost:{PORT}/index.html")
        print("⏹️  Нажмите Ctrl+C для остановки сервера")
        print()
        
        # Открываем браузер автоматически
        try:
            webbrowser.open(f'http://localhost:{PORT}/test.html')
        except:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Сервер остановлен")

if __name__ == "__main__":
    main()
