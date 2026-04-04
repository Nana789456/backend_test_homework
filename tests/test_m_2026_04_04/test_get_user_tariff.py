import pytest
from unittest.mock import patch, Mock

# ---- Тесты для get_user_tariff ----
def test_get_user_tariff_without_mock():
    """Тест с реальным запросом к сети"""
    result = get_user_tariff(1)
    assert result in ["premium", "free"]

@patch("requests.get")
def test_get_user_tariff_with_mock(mock_get):
    """Тест с моком requests.get"""
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    result = get_user_tariff(1)

    mock_get.assert_called_once_with(
        "https://httpbin.org/delay/1",
        params={"user_id": 1}
    )
    assert result == "free"