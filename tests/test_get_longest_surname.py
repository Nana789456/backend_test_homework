from lessons.m_2026_01_18.lesson2 import get_longest_surname
import pytest

@pytest.fixture
def students():
    return ['Иванов', 'Петренко', 'Сидорова123', 'Абрамян', 'Ван']

def test_get_longest_surname(students):
    expected = 'Сидорова123'
    result = get_longest_surname(students)
    assert expected == result