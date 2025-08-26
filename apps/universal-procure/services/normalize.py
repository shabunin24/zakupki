from typing import Dict, Any, List, Optional
from datetime import datetime

class DataNormalizer:
    """
    Сервис нормализации данных закупок
    Приводит данные от разных провайдеров к единому формату
    """
    
    def __init__(self):
        # Маппинг статусов к стандартным
        self.status_mapping = {
            "прием заявок": "accepting",
            "прием предложений": "accepting",
            "прием котировок": "accepting",
            "объявлен": "announced",
            "опубликован": "announced",
            "завершен": "completed",
            "завершена": "completed",
            "отменен": "cancelled",
            "отменена": "cancelled",
            "приостановлен": "suspended",
            "приостановлена": "suspended"
        }
        
        # Маппинг методов закупки
        self.method_mapping = {
            "электронный аукцион": "Электронный аукцион",
            "аукцион": "Электронный аукцион",
            "конкурс": "Конкурс",
            "запрос котировок": "Запрос котировок",
            "запрос предложений": "Запрос предложений",
            "единственный поставщик": "У единственного поставщика",
            "у единственного поставщика": "У единственного поставщика"
        }
    
    def normalize_purchase(self, purchase_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Нормализует данные закупки к стандартному формату
        
        Args:
            purchase_data: Сырые данные закупки
            
        Returns:
            Нормализованные данные или None если ошибка
        """
        try:
            normalized = {
                "id": self._normalize_id(purchase_data.get("id", "")),
                "title": self._normalize_title(purchase_data.get("title", "")),
                "description": self._normalize_description(purchase_data.get("description", "")),
                "customer": self._normalize_customer(purchase_data.get("customer", "")),
                "region": self._normalize_region(purchase_data.get("region", "")),
                "okpd2": self._normalize_okpd2(purchase_data.get("okpd2", [])),
                "price": self._normalize_price(purchase_data.get("price", 0)),
                "currency": self._normalize_currency(purchase_data.get("currency", "RUB")),
                "method": self._normalize_method(purchase_data.get("method", "")),
                "status": self._normalize_status(purchase_data.get("status", "")),
                "publish_dt": self._normalize_datetime(purchase_data.get("publish_dt")),
                "bid_deadline_dt": self._normalize_datetime(purchase_data.get("bid_deadline_dt")),
                "url": self._normalize_url(purchase_data.get("url", "")),
                "documents": self._normalize_documents(purchase_data.get("documents", []))
            }
            
            return normalized
            
        except Exception as e:
            print(f"Ошибка нормализации закупки: {e}")
            return None
    
    def _normalize_id(self, id_value: Any) -> str:
        """Нормализует ID закупки"""
        if not id_value:
            return f"unknown:{datetime.now().timestamp()}"
        return str(id_value)
    
    def _normalize_title(self, title: Any) -> str:
        """Нормализует название закупки"""
        if not title:
            return "Название не указано"
        return str(title).strip()
    
    def _normalize_description(self, description: Any) -> str:
        """Нормализует описание закупки"""
        if not description:
            return "Описание не указано"
        return str(description).strip()
    
    def _normalize_customer(self, customer: Any) -> str:
        """Нормализует название заказчика"""
        if not customer:
            return "Заказчик не указан"
        return str(customer).strip()
    
    def _normalize_region(self, region: Any) -> str:
        """Нормализует название региона"""
        if not region:
            return "Регион не указан"
        return str(region).strip()
    
    def _normalize_okpd2(self, okpd2: Any) -> List[str]:
        """Нормализует коды ОКПД2"""
        if not okpd2:
            return []
        
        if isinstance(okpd2, str):
            return [okpd2.strip()]
        elif isinstance(okpd2, list):
            return [str(code).strip() for code in okpd2 if code]
        else:
            return [str(okpd2).strip()]
    
    def _normalize_price(self, price: Any) -> float:
        """Нормализует цену закупки"""
        try:
            if isinstance(price, (int, float)):
                return float(price)
            elif isinstance(price, str):
                # Убираем все кроме цифр и точки
                import re
                price_str = re.sub(r'[^\d.]', '', price)
                return float(price_str) if price_str else 0.0
            else:
                return 0.0
        except (ValueError, TypeError):
            return 0.0
    
    def _normalize_currency(self, currency: Any) -> str:
        """Нормализует валюту"""
        if not currency:
            return "RUB"
        
        currency_str = str(currency).upper().strip()
        if currency_str in ["RUB", "РУБ", "РУБЛЬ", "РУБЛИ", "РУБЛЕЙ"]:
            return "RUB"
        elif currency_str in ["USD", "ДОЛЛАР", "ДОЛЛАРЫ", "ДОЛЛАРОВ"]:
            return "USD"
        elif currency_str in ["EUR", "ЕВРО"]:
            return "EUR"
        else:
            return "RUB"  # По умолчанию рубли
    
    def _normalize_method(self, method: Any) -> str:
        """Нормализует метод закупки"""
        if not method:
            return "Метод не указан"
        
        method_str = str(method).strip()
        return self.method_mapping.get(method_str.lower(), method_str)
    
    def _normalize_status(self, status: Any) -> str:
        """Нормализует статус закупки"""
        if not status:
            return "announced"
        
        status_str = str(status).strip().lower()
        return self.status_mapping.get(status_str, status_str)
    
    def _normalize_datetime(self, dt_value: Any) -> Optional[datetime]:
        """Нормализует дату/время"""
        if not dt_value:
            return None
        
        if isinstance(dt_value, datetime):
            return dt_value
        elif isinstance(dt_value, str):
            try:
                # Пробуем разные форматы даты
                formats = [
                    "%Y-%m-%dT%H:%M:%S",
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%d",
                    "%d.%m.%Y",
                    "%d/%m/%Y"
                ]
                
                for fmt in formats:
                    try:
                        return datetime.strptime(dt_value, fmt)
                    except ValueError:
                        continue
                
                # Если ничего не подошло, возвращаем None
                return None
                
            except Exception:
                return None
        else:
            return None
    
    def _normalize_url(self, url: Any) -> str:
        """Нормализует URL закупки"""
        if not url:
            return ""
        
        url_str = str(url).strip()
        if not url_str.startswith(("http://", "https://")):
            url_str = "https://" + url_str
        
        return url_str
    
    def _normalize_documents(self, documents: Any) -> List[Dict[str, str]]:
        """Нормализует список документов"""
        if not documents:
            return []
        
        normalized_docs = []
        
        if isinstance(documents, list):
            for doc in documents:
                if isinstance(doc, dict):
                    title = doc.get("title", "")
                    url = doc.get("url", "")
                    if title and url:
                        normalized_docs.append({
                            "title": str(title).strip(),
                            "url": self._normalize_url(url)
                        })
                elif isinstance(doc, str):
                    # Если документ - просто строка, считаем её названием
                    normalized_docs.append({
                        "title": str(doc).strip(),
                        "url": ""
                    })
        
        return normalized_docs
