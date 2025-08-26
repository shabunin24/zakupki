import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random

class APIOpenProvider:
    """
    Провайдер для работы с открытыми API закупок
    Пока содержит mock-данные для тестирования
    """
    
    def __init__(self):
        self.mock_data = self._generate_mock_data()
    
    async def search(self, filters: Dict[str, Any], limit: int = 20) -> List[Dict[str, Any]]:
        """
        Поиск закупок по фильтрам
        
        Args:
            filters: Словарь с фильтрами
            limit: Максимальное количество результатов
            
        Returns:
            Список закупок
        """
        # Имитируем задержку API
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        # Применяем фильтры к mock-данным
        filtered_data = self._apply_filters(self.mock_data, filters)
        
        # Возвращаем ограниченное количество результатов
        return filtered_data[:limit]
    
    def _generate_mock_data(self) -> List[Dict[str, Any]]:
        """Генерирует mock-данные закупок для тестирования"""
        mock_purchases = [
            {
                "id": "zakupki:001",
                "title": "Закупка канцелярских товаров для школ",
                "description": "Бумага А4, ручки, папки, тетради для образовательных учреждений",
                "customer": "ГУП Республики Крым 'Крымский центр закупок'",
                "region": "Республика Крым",
                "okpd2": ["17.23.13.110", "17.23.13.120"],
                "price": 250000.00,
                "currency": "RUB",
                "method": "Электронный аукцион",
                "status": "accepting",
                "publish_dt": datetime.now() - timedelta(days=2),
                "bid_deadline_dt": datetime.now() + timedelta(days=8),
                "url": "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=001",
                "documents": [
                    {"title": "Техническое задание.pdf", "url": "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=001&doc=1"},
                    {"title": "Проект контракта.pdf", "url": "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=001&doc=2"}
                ]
            },
            {
                "id": "zakupki:002",
                "title": "Поставка медицинского оборудования для больниц",
                "description": "Медицинское оборудование для диагностики и лечения",
                "customer": "Департамент здравоохранения города Москвы",
                "region": "Москва",
                "okpd2": ["26.60", "33.10"],
                "price": 8500000.00,
                "currency": "RUB",
                "method": "Конкурс",
                "status": "announced",
                "publish_dt": datetime.now() - timedelta(days=1),
                "bid_deadline_dt": datetime.now() + timedelta(days=15),
                "url": "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=002",
                "documents": [
                    {"title": "Техническое задание.pdf", "url": "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=002&doc=1"}
                ]
            },
            {
                "id": "zakupki:003",
                "title": "Строительство автомобильных дорог в Краснодарском крае",
                "description": "Строительство и ремонт автомобильных дорог регионального значения",
                "customer": "Министерство транспорта и дорожного хозяйства Краснодарского края",
                "region": "Краснодарский край",
                "okpd2": ["42.11", "42.12"],
                "price": 15000000.00,
                "currency": "RUB",
                "method": "Электронный аукцион",
                "status": "accepting",
                "publish_dt": datetime.now() - timedelta(days=3),
                "bid_deadline_dt": datetime.now() + timedelta(days=12),
                "url": "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=003",
                "documents": [
                    {"title": "Проектная документация.pdf", "url": "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=003&doc=1"},
                    {"title": "Сметная документация.pdf", "url": "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=003&doc=2"}
                ]
            },
            {
                "id": "zakupki:004",
                "title": "Электромонтажные работы в Санкт-Петербурге",
                "description": "Электромонтажные работы в жилых и общественных зданиях",
                "customer": "Комитет по энергетике и инженерному обеспечению Санкт-Петербурга",
                "region": "Санкт-Петербург",
                "okpd2": ["43.21"],
                "price": 2800000.00,
                "currency": "RUB",
                "method": "Запрос котировок",
                "status": "accepting",
                "publish_dt": datetime.now() - timedelta(days=5),
                "bid_deadline_dt": datetime.now() + timedelta(days=10),
                "url": "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=004",
                "documents": [
                    {"title": "Техническое задание.pdf", "url": "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=004&doc=1"}
                ]
            },
            {
                "id": "zakupki:005",
                "title": "Поставка офисной бумаги А4 в Москве",
                "description": "Бумага А4 офисная, белая, 80 г/м², 500 листов",
                "customer": "АО 'Московский офис'",
                "region": "Москва",
                "okpd2": ["17.23.13.110"],
                "price": 180000.00,
                "currency": "RUB",
                "method": "У единственного поставщика",
                "status": "announced",
                "publish_dt": datetime.now() - timedelta(days=1),
                "bid_deadline_dt": None,
                "url": "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=005",
                "documents": [
                    {"title": "Техническое задание.pdf", "url": "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=005&doc=1"}
                ]
            }
        ]
        
        return mock_purchases
    
    def _apply_filters(self, data: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Применяет фильтры к данным закупок"""
        filtered_data = data.copy()
        
        # Фильтр по ОКПД2
        if filters.get("okpd2"):
            okpd2_codes = filters["okpd2"]
            filtered_data = [
                item for item in filtered_data
                if any(code in item["okpd2"] for code in okpd2_codes)
            ]
        
        # Фильтр по региону
        if filters.get("region"):
            regions = filters["region"]
            filtered_data = [
                item for item in filtered_data
                if item["region"] in regions
            ]
        
        # Фильтр по цене
        if filters.get("price_min") is not None:
            filtered_data = [
                item for item in filtered_data
                if item["price"] >= filters["price_min"]
            ]
        
        if filters.get("price_max") is not None:
            filtered_data = [
                item for item in filtered_data
                if item["price"] <= filters["price_max"]
            ]
        
        # Фильтр по методу закупки
        if filters.get("method"):
            methods = filters["method"]
            filtered_data = [
                item for item in filtered_data
                if item["method"] in methods
            ]
        
        # Фильтр по статусу
        if filters.get("status"):
            statuses = filters["status"]
            filtered_data = [
                item for item in filtered_data
                if item["status"] in statuses
            ]
        
        # Фильтр по датам
        if filters.get("date_from"):
            date_from = filters["date_from"]
            if date_from == "last_7_days":
                cutoff_date = datetime.now() - timedelta(days=7)
                filtered_data = [
                    item for item in filtered_data
                    if item["publish_dt"] >= cutoff_date
                ]
            elif date_from == "last_30_days":
                cutoff_date = datetime.now() - timedelta(days=30)
                filtered_data = [
                    item for item in filtered_data
                    if item["publish_dt"] >= cutoff_date
                ]
        
        return filtered_data
