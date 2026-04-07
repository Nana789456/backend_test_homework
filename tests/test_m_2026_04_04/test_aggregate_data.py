import pytest
from unittest.mock import patch, Mock
# from lessons.m_2026_04_04.homework import aggregate_data
from lessons.m_2026_04_04 import homework


# ---- Тесты для aggregate_data ----
def test_aggregate_data_without_mock():
    """Медленный тест: реальный вызов с time.sleep"""
    result = homework.aggregate_data(10)
    assert result["total"] == 1000

# # @patch("lessons.m_2026_04_04.homework.aggregate_data")
# def test_aggregate_data_with_mock():
#     """Быстрый тест: мок функции aggregate_data"""

#     with patch('lessons.m_2026_04_04.homework.aggregate_data') as mock_aggregate:
#     # with patch('lessons.m_2026_04_04.homework.aggregate_data') as mock_aggregate:
        
#         from lessons.m_2026_04_04.homework import aggregate_data
        
#         mock_aggregate.return_value = {"total": 100, "avg": 10}

#         result = aggregate_data(10)

#         assert result["total"] == 100
#         mock_aggregate.assert_called_once_with(10)


@patch("lessons.m_2026_04_04.homework.aggregate_data")
def test_aggregate_data_with_mock(mock_aggregate):
    """Быстрый тест: мок функции aggregate_data"""

    # with patch('lessons.m_2026_04_04.homework.aggregate_data') as mock_aggregate:
    mock_aggregate.return_value = {"total": 100, "avg": 10}

    result = homework.aggregate_data(10)

    assert result["total"] == 100
    mock_aggregate.assert_called_once_with(10)


def test_aggregate_data_with_mock_new():
    """Быстрый тест: мок функции aggregate_data"""

    with patch('lessons.m_2026_04_04.homework.aggregate_data') as mock_aggregate:
        mock_aggregate.return_value = {"total": 100, "avg": 10}

        result = homework.aggregate_data(10)

        assert result["total"] == 100
        mock_aggregate.assert_called_once_with(10)