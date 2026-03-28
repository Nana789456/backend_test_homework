from unittest.mock import patch
from lessons.m_2026_03_28.homework import get_weather
import requests

def test_get_weather():
    mock_response = {"temp": 25, "condition": "sunny"}
    
    # Подменяем реальную функцию requests.get на мок
    with patch('requests.get') as mock_get:
        # Настраиваем мок: что он должен вернуть
        mock_get.return_value.json.return_value = mock_response
        
        # Вызываем нашу функцию
        result = get_weather("Moscow")
        
        # Проверяем результат
        assert result == {"temp": 25, "condition": "sunny"}
        # Проверяем, что функция вызвала requests.get ровно 1 раз
        mock_get.assert_called_once()