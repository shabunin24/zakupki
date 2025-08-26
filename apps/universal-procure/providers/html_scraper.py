import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup

class HTMLScraperProvider:
    """
    Провайдер для скрейпинга HTML страниц zakupki.gov.ru
    Fallback-решение когда API недоступен
    """
    
    def __init__(self):
        self.base_url = "https://zakupki.gov.ru"
        self.session = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    async def __aenter__(self):
        """Асинхронный контекстный менеджер - вход"""
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронный контекстный менеджер - выход"""
        if self.session:
            await self.session.close()
    
    async def search(self, filters: Dict[str, Any], limit: int = 20) -> List[Dict[str, Any]]:
        """
        Поиск закупок через скрейпинг HTML страниц
        
        Args:
            filters: Словарь с фильтрами
            limit: Максимальное количество результатов
            
        Returns:
            Список закупок
        """
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.headers)
        
        try:
            # Формируем URL для поиска
            search_url = self._build_search_url(filters)
            
            # Получаем страницу результатов
            async with self.session.get(search_url, timeout=30) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}: {response.reason}")
                
                html_content = await response.text()
                
                # Парсим результаты
                results = self._parse_search_results(html_content, limit)
                
                return results
                
        except Exception as e:
            # В случае ошибки возвращаем пустой список
            print(f"Ошибка скрейпинга: {e}")
            return []
    
    def _build_search_url(self, filters: Dict[str, Any]) -> str:
        """Строит URL для поиска на основе фильтров"""
        base_url = f"{self.base_url}/epz/order/extendedsearch/results.html"
        
        params = []
        
        # Добавляем текстовый поиск
        if filters.get("text"):
            params.append(f"searchString={filters['text']}")
        
        # Добавляем фильтр по цене
        if filters.get("price_min"):
            params.append(f"priceFromGeneral={filters['price_min']}")
        
        if filters.get("price_max"):
            params.append(f"priceToGeneral={filters['price_max']}")
        
        # Добавляем фильтр по региону
        if filters.get("region"):
            # Здесь нужно маппить названия регионов в коды
            pass
        
        # Добавляем фильтр по методу закупки
        if filters.get("method"):
            # Здесь нужно маппить методы в коды
            pass
        
        if params:
            base_url += "?" + "&".join(params)
        
        return base_url
    
    def _parse_search_results(self, html_content: str, limit: int) -> List[Dict[str, Any]]:
        """Парсит HTML страницу с результатами поиска"""
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        try:
            # Ищем таблицу с результатами
            results_table = soup.find('table', {'class': 'search-registry'})
            if not results_table:
                return results
            
            # Ищем строки с закупками
            rows = results_table.find_all('tr', {'class': 'dataRow'})
            
            for i, row in enumerate(rows):
                if i >= limit:
                    break
                
                try:
                    purchase = self._parse_purchase_row(row)
                    if purchase:
                        results.append(purchase)
                except Exception as e:
                    print(f"Ошибка парсинга строки {i}: {e}")
                    continue
            
        except Exception as e:
            print(f"Ошибка парсинга результатов: {e}")
        
        return results
    
    def _parse_purchase_row(self, row) -> Optional[Dict[str, Any]]:
        """Парсит строку с закупкой"""
        try:
            # Извлекаем основные данные из строки
            cells = row.find_all('td')
            if len(cells) < 5:
                return None
            
            # Базовые данные (заглушка)
            purchase = {
                "id": f"scraped:{len(cells)}",
                "title": cells[0].get_text(strip=True) if cells[0] else "Название не указано",
                "description": "Описание закупки",
                "customer": cells[1].get_text(strip=True) if len(cells) > 1 and cells[1] else "Заказчик не указан",
                "region": "Регион не указан",
                "okpd2": [],
                "price": 0.0,
                "currency": "RUB",
                "method": "Метод не указан",
                "status": "announced",
                "publish_dt": datetime.now(),
                "bid_deadline_dt": None,
                "url": "",
                "documents": []
            }
            
            return purchase
            
        except Exception as e:
            print(f"Ошибка парсинга строки закупки: {e}")
            return None
    
    async def get_purchase_details(self, purchase_url: str) -> Optional[Dict[str, Any]]:
        """
        Получает детальную информацию о закупке
        
        Args:
            purchase_url: URL страницы закупки
            
        Returns:
            Детали закупки или None
        """
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.headers)
        
        try:
            async with self.session.get(purchase_url, timeout=30) as response:
                if response.status != 200:
                    return None
                
                html_content = await response.text()
                
                # Парсим детали закупки
                details = self._parse_purchase_details(html_content)
                
                return details
                
        except Exception as e:
            print(f"Ошибка получения деталей закупки: {e}")
            return None
    
    def _parse_purchase_details(self, html_content: str) -> Dict[str, Any]:
        """Парсит HTML страницу с деталями закупки"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        details = {
            "description": "",
            "okpd2": [],
            "price": 0.0,
            "method": "",
            "status": "",
            "documents": []
        }
        
        try:
            # Извлекаем описание
            desc_elem = soup.find('div', {'class': 'description'})
            if desc_elem:
                details["description"] = desc_elem.get_text(strip=True)
            
            # Извлекаем цену
            price_elem = soup.find('span', {'class': 'price'})
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                # Парсим цену из текста
                import re
                price_match = re.search(r'(\d+(?:\.\d+)?)', price_text)
                if price_match:
                    details["price"] = float(price_match.group(1))
            
            # Извлекаем документы
            docs_elem = soup.find('div', {'class': 'documents'})
            if docs_elem:
                doc_links = docs_elem.find_all('a')
                for link in doc_links:
                    doc_title = link.get_text(strip=True)
                    doc_url = link.get('href', '')
                    if doc_title and doc_url:
                        details["documents"].append({
                            "title": doc_title,
                            "url": doc_url if doc_url.startswith('http') else f"{self.base_url}{doc_url}"
                        })
            
        except Exception as e:
            print(f"Ошибка парсинга деталей закупки: {e}")
        
        return details
