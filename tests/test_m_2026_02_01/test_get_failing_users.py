from lessons.m_2026_02_01.lesson import get_failing_users
import pytest

@pytest.fixture
def students_data():
    """Фикстура с тестовыми данными пользователей и их оценок."""
    return {
        'Иванов': {'Математика': [2, 3, 2], 'Физика': [5, 5, 5]},
        'Петров': {'Математика': [5, 5, 5], 'Физика': [5, 4, 5]},
        'Попов': {'Математика': [4, 4, 3], 'Физика': [3, 2, 2]},
        'Кузнецов': {'Математика': [5, 1, 5], 'Физика': [3, 4, 4]}
    }


def test_get_failing_users(students_data):
    expected = ['Иванов', 'Попов']
    result = get_failing_users(students_data)
    assert expected == result
