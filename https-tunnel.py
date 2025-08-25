#!/usr/bin/env python3
"""
Простой HTTPS туннель для тестирования Telegram Mini App
"""

import http.server
import socketserver
import ssl
import threading
import webbrowser
from urllib.parse import urlparse
import requests

# Конфигурация
LOCAL_PORT = 3000
HTTPS_PORT = 8443
CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"

def create_self_signed_cert():
    """Создает самоподписанный сертификат"""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from datetime import datetime, timedelta
        
        # Генерируем приватный ключ
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Создаем сертификат
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Moscow"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Moscow"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Zakupki Bot"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress("127.0.0.1"),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Сохраняем сертификат и ключ
        with open(CERT_FILE, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open(KEY_FILE, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print("✅ Самоподписанный сертификат создан")
        return True
        
    except ImportError:
        print("❌ Требуется cryptography: pip install cryptography")
        return False
    except Exception as e:
        print(f"❌ Ошибка создания сертификата: {e}")
        return False

def start_https_server():
    """Запускает HTTPS сервер"""
    try:
        # Создаем HTTP сервер
        handler = http.server.SimpleHTTPRequestHandler
        
        # Настраиваем HTTPS
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(CERT_FILE, KEY_FILE)
        
        with socketserver.TCPServer(("", HTTPS_PORT), handler) as httpd:
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            print(f"🔒 HTTPS сервер запущен на порту {HTTPS_PORT}")
            print(f"🌐 URL: https://localhost:{HTTPS_PORT}")
            httpd.serve_forever()
            
    except Exception as e:
        print(f"❌ Ошибка запуска HTTPS сервера: {e}")

def proxy_to_localhost():
    """Проксирует запросы на localhost:3000"""
    try:
        import http.server
        import urllib.request
        
        class ProxyHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                try:
                    # Проксируем на localhost:3000
                    url = f"http://localhost:{LOCAL_PORT}{self.path}"
                    response = urllib.request.urlopen(url)
                    
                    # Отправляем заголовки
                    self.send_response(response.status)
                    for header, value in response.getheaders():
                        self.send_header(header, value)
                    self.end_headers()
                    
                    # Отправляем содержимое
                    self.wfile.write(response.read())
                    
                except Exception as e:
                    self.send_error(500, f"Proxy error: {e}")
            
            def do_POST(self):
                try:
                    # Читаем тело запроса
                    content_length = int(self.headers.get('Content-Length', 0))
                    post_data = self.rfile.read(content_length)
                    
                    # Проксируем на localhost:3000
                    url = f"http://localhost:{LOCAL_PORT}{self.path}"
                    req = urllib.request.Request(url, data=post_data, method='POST')
                    
                    # Копируем заголовки
                    for header, value in self.headers.items():
                        if header.lower() not in ['host', 'content-length']:
                            req.add_header(header, value)
                    
                    response = urllib.request.urlopen(req)
                    
                    # Отправляем ответ
                    self.send_response(response.status)
                    for header, value in response.getheaders():
                        self.send_header(header, value)
                    self.end_headers()
                    
                    self.wfile.write(response.read())
                    
                except Exception as e:
                    self.send_error(500, f"Proxy error: {e}")
            
            def log_message(self, format, *args):
                print(f"🔀 Proxy: {format % args}")
        
        # Запускаем прокси
        with socketserver.TCPServer(("", HTTPS_PORT), ProxyHandler) as httpd:
            print(f"🔀 HTTPS прокси запущен на порту {HTTPS_PORT}")
            print(f"🌐 URL: https://localhost:{HTTPS_PORT}")
            print(f"📡 Проксирует на: http://localhost:{LOCAL_PORT}")
            httpd.serve_forever()
            
    except Exception as e:
        print(f"❌ Ошибка запуска прокси: {e}")

def main():
    print("🚀 Запуск HTTPS туннеля для Telegram Mini App")
    print("=" * 50)
    
    # Проверяем, запущен ли локальный сервер
    try:
        response = requests.get(f"http://localhost:{LOCAL_PORT}", timeout=5)
        if response.status_code == 200:
            print(f"✅ Локальный сервер работает на порту {LOCAL_PORT}")
        else:
            print(f"⚠️ Локальный сервер отвечает с кодом {response.status_code}")
    except:
        print(f"❌ Локальный сервер на порту {LOCAL_PORT} недоступен")
        print("Запустите: npm run dev")
        return
    
    print()
    print("🔧 Выберите режим:")
    print("1. Простой HTTPS сервер (статичные файлы)")
    print("2. HTTPS прокси на localhost:3000 (рекомендуется)")
    
    choice = input("\nВведите номер (1-2): ").strip()
    
    if choice == "1":
        if create_self_signed_cert():
            start_https_server()
        else:
            print("❌ Не удалось создать сертификат")
    elif choice == "2":
        proxy_to_localhost()
    else:
        print("❌ Неверный выбор")

if __name__ == "__main__":
    main()
