from lessons.m_2026_01_18.lesson1 import get_user_with_min_average_value
import pytest


@pytest.fixture
def users_marks():
    """Фикстура с тестовыми данными пользователей и их оценок."""
    return {
        'user1': [3, 1, 2],
        'user2': [5, 5, 5],
        'user3': [5, 4, 5],
        'user4': [2, 1, 2],
        }


def test_get_user_with_min_average_value(users_marks):
    expected = 'user4'
    result = get_user_with_min_average_value(users_marks)
    assert expected == result