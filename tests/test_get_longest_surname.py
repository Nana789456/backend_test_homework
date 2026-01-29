from lessons.m_2026_01_18.lesson2 import get_longest_surname


def test_get_longest_surname():
    surnames = ['Иванов', 'Петренко', 'Сидорова123', 'Абрамян', 'Ван']
    expected = 'Сидорова123'
    result = get_longest_surname(surnames)
    assert expected == result