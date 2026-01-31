from lessons.m_2026_01_18.lesson3 import get_latest_book_and_year
import pytest

@pytest.fixture
def books():
    return {
        '1984': 1949,
        'Мастер и Маргарита': 1967,
        'Гарри Поттер': 1997,
        'Пикник на обочине': 1972
        }

def test_get_latest_book_and_year(books):
    expected = {'Гарри Поттер': 1997}
    result = get_latest_book_and_year(books)
    assert expected == result