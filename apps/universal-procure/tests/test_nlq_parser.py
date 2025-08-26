import pytest
import sys
from pathlib import Path

# Добавляем родительскую директорию в путь для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))

from parser.ru_nlq import NLQParser

class TestNLQParser:
    """Тесты для парсера естественного языка"""
    
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.parser = NLQParser()
    
    def test_paper_a4_office_moscow(self):
        """Тест: 'бумага А4 офисная Москва до 200 тыс руб'"""
        query = "бумага А4 офисная Москва до 200 тыс руб"
        result = self.parser.parse(query)
        
        assert "17.23.13.110" in result["okpd2"]
        assert "Город Москва" in result["region"]
        assert result["price_max"] == 200000
        assert result["text"] == query
        
        # Проверяем диагностику
        assert "бумага а4" in result["diagnostics"]["matched_keywords"]
        assert "17.23.13.110" in result["diagnostics"]["matched_okpd2"]
        assert "Город Москва" in result["diagnostics"]["regions_detected"]
        assert result["diagnostics"]["price_max"] == 200000
    
    def test_road_construction_crimea_price_range(self):
        """Тест: 'услуги по строительству дорог Крым от 5 до 20 млн'"""
        query = "услуги по строительству дорог Крым от 5 до 20 млн"
        result = self.parser.parse(query)
        
        assert "42.11.*" in result["okpd2"]
        assert "Республика Крым" in result["region"]
        assert result["price_min"] == 5000000
        assert result["price_max"] == 20000000
        
        # Проверяем диагностику
        assert "строительство дорог" in result["diagnostics"]["matched_keywords"]
        assert "Республика Крым" in result["diagnostics"]["regions_detected"]
        assert result["diagnostics"]["price_min"] == 5000000
        assert result["diagnostics"]["price_max"] == 20000000
    
    def test_medical_equipment_moscow_competition(self):
        """Тест: 'поставка медоборудования Москва конкурс'"""
        query = "поставка медоборудования Москва конкурс"
        result = self.parser.parse(query)
        
        assert "26.60.*" in result["okpd2"]
        assert "Город Москва" in result["region"]
        assert "конкурс" in result["method"]
        
        # Проверяем диагностику
        assert "медоборудование" in result["diagnostics"]["matched_keywords"]
        assert "Город Москва" in result["diagnostics"]["regions_detected"]
        assert result["diagnostics"]["method_detected"] == "конкурс"
    
    def test_electrical_works_spb_new_week(self):
        """Тест: 'электромонтажные работы до 3 млн руб Санкт-Петербург новые за неделю'"""
        query = "электромонтажные работы до 3 млн руб Санкт-Петербург новые за неделю"
        result = self.parser.parse(query)
        
        assert "43.21.*" in result["okpd2"]
        assert result["price_max"] == 3000000
        assert "Город Санкт-Петербург" in result["region"]
        assert result["publish_date_from"] is not None
        
        # Проверяем диагностику
        assert "электромонтажные работы" in result["diagnostics"]["matched_keywords"]
        assert "Город Санкт-Петербург" in result["diagnostics"]["regions_detected"]
        assert result["diagnostics"]["price_max"] == 3000000
        assert "new_last_7_days_default" in result["diagnostics"]["date_rules"]
    
    def test_computers_printers_spb_auction_new_3_days(self):
        """Тест: 'компьютеры и принтеры санкт-петербург электронный аукцион новые за 3 дня'"""
        query = "компьютеры и принтеры санкт-петербург электронный аукцион новые за 3 дня"
        result = self.parser.parse(query)
        
        assert "26.20.*" in result["okpd2"]  # компьютеры
        assert "26.30.*" in result["okpd2"]  # принтеры
        assert "Город Санкт-Петербург" in result["region"]
        assert "аукцион" in result["method"]
        assert result["publish_date_from"] is not None
        
        # Проверяем диагностику
        assert "компьютеры" in result["diagnostics"]["matched_keywords"]
        assert "принтеры" in result["diagnostics"]["matched_keywords"]
        assert "Город Санкт-Петербург" in result["diagnostics"]["regions_detected"]
        assert result["diagnostics"]["method_detected"] == "аукцион"
        assert "new_last_7_days_default" in result["diagnostics"]["date_rules"]
    
    def test_road_repair_crimea_price_range(self):
        """Тест: 'ремонт дорог крым от 5 до 20 млн'"""
        query = "ремонт дорог крым от 5 до 20 млн"
        result = self.parser.parse(query)
        
        assert "42.11.*" in result["okpd2"]
        assert "Республика Крым" in result["region"]
        assert result["price_min"] == 5000000
        assert result["price_max"] == 20000000
        
        # Проверяем диагностику
        assert "ремонт дорог" in result["diagnostics"]["matched_keywords"]
        assert "Республика Крым" in result["diagnostics"]["regions_detected"]
        assert result["diagnostics"]["price_min"] == 5000000
        assert result["diagnostics"]["price_max"] == 20000000
    
    def test_security_services_rostov(self):
        """Тест: 'охрана помещений ростов-на-дону'"""
        query = "охрана помещений ростов-на-дону"
        result = self.parser.parse(query)
        
        assert "80.10.*" in result["okpd2"] or "80.20.*" in result["okpd2"]
        assert "Ростовская область" in result["region"]
        
        # Проверяем диагностику
        assert "охрана" in result["diagnostics"]["matched_keywords"]
        assert "Ростовская область" in result["diagnostics"]["regions_detected"]
    
    def test_medical_equipment_competition_moscow_next_week_deadline(self):
        """Тест: 'мед оборудование конкурс москва дедлайн на следующей неделе'"""
        query = "мед оборудование конкурс москва дедлайн на следующей неделе"
        result = self.parser.parse(query)
        
        assert "26.60.*" in result["okpd2"]
        assert "конкурс" in result["method"]
        assert "Город Москва" in result["region"]
        assert result["deadline_from"] is not None
        assert result["deadline_to"] is not None
        
        # Проверяем диагностику
        assert "мед оборудование" in result["diagnostics"]["matched_keywords"]
        assert result["diagnostics"]["method_detected"] == "конкурс"
        assert "Город Москва" in result["diagnostics"]["regions_detected"]
        assert "deadline_next_week" in result["diagnostics"]["date_rules"]
    
    def test_simple_text_query(self):
        """Тест простого текстового запроса"""
        query = "канцелярские товары"
        result = self.parser.parse(query)
        
        assert len(result["okpd2"]) > 0
        assert result["text"] == query
        
        # Проверяем диагностику
        assert "канцелярия" in result["diagnostics"]["matched_keywords"]
    
    def test_price_only_query(self):
        """Тест запроса только с ценой"""
        query = "до 1 млн рублей"
        result = self.parser.parse(query)
        
        assert result["price_max"] == 1000000
        assert result["text"] == query
        
        # Проверяем диагностику
        assert result["diagnostics"]["price_max"] == 1000000
    
    def test_region_only_query(self):
        """Тест запроса только с регионом"""
        query = "в Москве"
        result = self.parser.parse(query)
        
        assert "Город Москва" in result["region"]
        assert result["text"] == query
        
        # Проверяем диагностику
        assert "Город Москва" in result["diagnostics"]["regions_detected"]
    
    def test_method_only_query(self):
        """Тест запроса только с методом закупки"""
        query = "электронный аукцион"
        result = self.parser.parse(query)
        
        assert "аукцион" in result["method"]
        assert result["text"] == query
        
        # Проверяем диагностику
        assert result["diagnostics"]["method_detected"] == "аукцион"
    
    def test_complex_query(self):
        """Тест сложного составного запроса"""
        query = "строительство мостов в Краснодарском крае от 10 до 50 млн рублей конкурс"
        result = self.parser.parse(query)
        
        assert "42.13.*" in result["okpd2"]
        assert "Краснодарский край" in result["region"]
        assert result["price_min"] == 10000000
        assert result["price_max"] == 50000000
        assert "конкурс" in result["method"]
        
        # Проверяем диагностику
        assert "строительство дорог" in result["diagnostics"]["matched_keywords"]
        assert "Краснодарский край" in result["diagnostics"]["regions_detected"]
        assert result["diagnostics"]["price_min"] == 10000000
        assert result["diagnostics"]["price_max"] == 50000000
        assert result["diagnostics"]["method_detected"] == "конкурс"
    
    def test_empty_query(self):
        """Тест пустого запроса"""
        query = ""
        result = self.parser.parse(query)
        
        assert result["text"] == ""
        assert result["okpd2"] == []
        assert result["region"] == []
        assert result["price_min"] is None
        assert result["price_max"] is None
        
        # Проверяем диагностику
        assert result["diagnostics"]["matched_keywords"] == []
        assert result["diagnostics"]["matched_okpd2"] == []
        assert result["diagnostics"]["regions_detected"] == []
    
    def test_price_patterns(self):
        """Тест различных паттернов цен"""
        test_cases = [
            ("до 500 тыс", 500000),
            ("от 2 млн", 2000000),
            ("100 тыс рублей", 100000),
            ("5 миллионов", 5000000),
            ("от 1.5 до 3 млн", (1500000, 3000000))
        ]
        
        for query, expected in test_cases:
            result = self.parser.parse(query)
            if isinstance(expected, tuple):
                assert result["price_min"] == expected[0]
                assert result["price_max"] == expected[1]
                assert result["diagnostics"]["price_min"] == expected[0]
                assert result["diagnostics"]["price_max"] == expected[1]
            else:
                if "до" in query:
                    assert result["price_max"] == expected
                    assert result["diagnostics"]["price_max"] == expected
                elif "от" in query:
                    assert result["price_min"] == expected
                    assert result["diagnostics"]["price_min"] == expected
                else:
                    assert result["price_max"] == expected
                    assert result["diagnostics"]["price_max"] == expected
    
    def test_region_synonyms(self):
        """Тест региональных синонимов"""
        test_cases = [
            ("крым", "Республика Крым"),
            ("спб", "Город Санкт-Петербург"),
            ("питер", "Город Санкт-Петербург"),
            ("москва", "Город Москва"),
            ("ростов-на-дону", "Ростовская область")
        ]
        
        for synonym, region in test_cases:
            result = self.parser.parse(f"закупка в {synonym}")
            assert region in result["region"]
            assert region in result["diagnostics"]["regions_detected"]
    
    def test_status_keywords(self):
        """Тест ключевых слов статусов"""
        test_cases = [
            ("новые закупки", "announced"),
            ("прием заявок открыт", "accepting"),
            ("за неделю", "new_last_7_days_default"),
            ("за месяц", "new_last_30_days_default")
        ]
        
        for query, status in test_cases:
            result = self.parser.parse(query)
            if "неделю" in query or "месяц" in query:
                assert status in result["diagnostics"]["date_rules"]
            else:
                assert status in result["status"]
                assert result["diagnostics"]["status_detected"] == status
    
    def test_lemmatization(self):
        """Тест лемматизации"""
        query = "канцелярские товары для офиса"
        result = self.parser.parse(query)
        
        # Проверяем, что лемматизация работает
        assert "канцелярия" in result["diagnostics"]["matched_keywords"]
        assert len(result["okpd2"]) > 0
    
    def test_next_week_deadline(self):
        """Тест дедлайна на следующей неделе"""
        query = "закупка с дедлайном на следующей неделе"
        result = self.parser.parse(query)
        
        assert result["deadline_from"] is not None
        assert result["deadline_to"] is not None
        assert "deadline_next_week" in result["diagnostics"]["date_rules"]
    
    def test_deadline_in_days(self):
        """Тест дедлайна через N дней"""
        query = "закупка с дедлайном через 5 дней"
        result = self.parser.parse(query)
        
        assert result["deadline_from"] is not None
        assert "deadline_in_5_days" in result["diagnostics"]["date_rules"]

if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v"])
