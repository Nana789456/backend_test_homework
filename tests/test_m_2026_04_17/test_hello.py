from unittest.mock import patch

from lessons.m_2026_04_04.homework import hello

def test_problem_import_before_patch1():
    """❌ НЕПРАВИЛЬНО: импорт функции до применения патча"""
    # Функция уже импортирована вверху файла: from homework import hello
    
    with patch('lessons.m_2026_04_04.homework.hello') as mock_hello:
        mock_hello.return_value = "mocked"
        
        # hello всё ещё указывает на реальную функцию!
        result = hello()  # ❌ Вызовется РЕАЛЬНАЯ функция
        
        assert result == "mocked"  # Тест упадёт!


# Плохая практика, так не делать    
def test_problem_import_before_patch2():
    """❌ НЕПРАВИЛЬНО: импорт функции до применения патча"""
    # Функция уже импортирована вверху файла: from homework import hello
    
    with patch('lessons.m_2026_04_04.homework.hello') as mock_hello:
        mock_hello.return_value = "mocked"
        
        # hello всё ещё указывает на реальную функцию!
        result = mock_hello()  # ❌ Вызовется РЕАЛЬНАЯ функция
        
        assert result == "mocked"  # Тест упадёт!


from lessons.m_2026_04_04 import homework


def test_success_inner_long_operation():
    # Функция уже импортирована вверху файла: from homework import hello
    
    with patch('lessons.m_2026_04_04.homework.time.sleep') as mock_sleep:
        # mock_hello.return_value = "mocked"
        
        result = homework.hello()  # Вызовется mock
        
        assert result == "mocked"


def test_success_hello_with_long_inner_fun():

    with patch('lessons.m_2026_04_04.homework.inner_fun') as mock_inner_fun:
        mock_inner_fun.return_value = "mocked"
        
        result = homework.hello_with_long_inner_fun()  # Вызовется mock
        
        assert result == "mocked"