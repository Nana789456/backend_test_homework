from lessons.m_2026_01_18.lesson4 import get_failing_users


def test_get_failing_users():
    user_marks = {
        'user1': [3, 1, 2],
        'user2': [5, 5, 5],
        'user3': [5, 4, 5],
        'user4': [2, 1, 2],
        'user5': [3, 2, 2]
        }
    expected = {'user1': [3, 1, 2], 'user4': [2, 1, 2], 'user5': [3, 2, 2]}
    result = get_failing_users(user_marks)
    assert expected == result
