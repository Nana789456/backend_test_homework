# Пример SQL инъекции
sql_str = 'INSERT INTO reports VALUES (123 123 123'
new_value = " 456) ; DROP TABLE reports;"
sql = sql_str + new_value
print(sql)


"""
МОКИРОВАНИЕ В PYTHON: КЛЮЧЕВЫЕ ПРИНЦИПЫ

Основная проблема: patch заменяет объект по указанному пути, но не обновляет существующие ссылки.
"""

import pytest
from unittest.mock import patch, Mock
import homework  # Импортируем модуль целиком
from homework import hello, aggregate_data  # Импортируем конкретные функции


# ============= ЧАСТЬ 1: ПОЧЕМУ НЕ РАБОТАЕТ ИМПОРТ ДО ПАТЧА =============

def test_problem_import_before_patch():
    """❌ НЕПРАВИЛЬНО: импорт функции до применения патча"""
    # Функция уже импортирована вверху файла: from homework import hello
    
    with patch('homework.hello') as mock_hello:
        mock_hello.return_value = "mocked"
        
        # hello всё ещё указывает на реальную функцию!
        result = hello()  # ❌ Вызовется РЕАЛЬНАЯ функция
        
        assert result == "mocked"  # Тест упадёт!


def test_problem_direct_import_without_module():
    """❌ НЕПРАВИЛЬНО: прямая ссылка без обращения через модуль"""
    from homework import aggregate_data
    
    with patch('homework.aggregate_data') as mock_agg:
        mock_agg.return_value = {"total": 100, "avg": 10}
        
        # aggregate_data - это локальная переменная, указывающая на оригинал
        result = aggregate_data(10)  # ❌ Реальная функция
        
        assert result["total"] == 100  # Тест упадёт


# ============= ЧАСТЬ 2: ПРАВИЛЬНЫЕ СПОСОБЫ МОКИРОВАНИЯ =============

def test_correct_import_module_approach():
    """✅ ПРАВИЛЬНО: импорт модуля целиком и обращение через модуль"""
    with patch('homework.aggregate_data') as mock_agg:
        mock_agg.return_value = {"total": 100, "avg": 10}
        
        # Обращаемся через модуль - всегда свежая ссылка
        result = homework.aggregate_data(10)
        
        assert result["total"] == 100
        mock_agg.assert_called_once_with(10)


def test_correct_decorator_with_module():
    """✅ ПРАВИЛЬНО: использование декоратора с доступом через модуль"""
    with patch('homework.aggregate_data') as mock_agg:
        mock_agg.return_value = {"total": 100, "avg": 10}
        
        result = homework.aggregate_data(10)
        
        assert result["total"] == 100
        mock_agg.assert_called_once_with(10)


def test_correct_import_inside_context():
    """✅ ПРАВИЛЬНО: импорт функции ВНУТРИ контекста патча"""
    with patch('homework.aggregate_data') as mock_agg:
        mock_agg.return_value = {"total": 100, "avg": 10}
        
        # Импортируем после применения патча
        from homework import aggregate_data
        result = aggregate_data(10)
        
        assert result["total"] == 100
        mock_agg.assert_called_once_with(10)


# ============= ЧАСТЬ 3: МОКИРОВАНИЕ ЗАВИСИМОСТЕЙ (НЕ ТЕСТИРУЕМОЙ ФУНКЦИИ) =============

def test_mock_dependencies():
    """✅ ПРАВИЛЬНО: мокируем зависимости (time.sleep), а не саму функцию"""
    from homework import aggregate_data
    
    with patch('homework.time.sleep') as mock_sleep:
        # Не мокаем aggregate_data, мокаем её зависимость
        result = aggregate_data(10)
        
        assert result["total"] == 1000  # 10 * 100
        assert result["avg"] == 50
        mock_sleep.assert_called_once_with(2)


def test_mock_dependencies_decorator():
    """✅ ПРАВИЛЬНО: декоратор для мока зависимостей"""
    from homework import aggregate_data
    
    with patch('homework.time.sleep') as mock_sleep:
        result = aggregate_data(5)
        
        assert result["total"] == 500
        mock_sleep.assert_called_once_with(2)


# ============= ЧАСТЬ 4: МОКИРОВАНИЕ В ДРУГОМ МОДУЛЕ (ГДЕ ФУНКЦИЯ ИСПОЛЬЗУЕТСЯ) =============

def test_mock_where_function_is_used():
    """✅ ПРАВИЛЬНО: мокируем функцию в том месте, где она ИСПОЛЬЗУЕТСЯ"""
    # Представим, что есть функция process_report, которая вызывает aggregate_data
    from homework import process_report
    
    with patch('homework.aggregate_data') as mock_agg:
        mock_agg.return_value = {"total": 100, "avg": 10}
        
        # process_report использует aggregate_data - она будет замокана
        result = process_report(10)
        
        assert result["processed"] == 100
        mock_agg.assert_called_once_with(10)


# ============= ЧАСТЬ 5: НАГЛЯДНАЯ ДЕМОНСТРАЦИЯ ПРОБЛЕМЫ СО ССЫЛКАМИ =============

def test_demonstrate_reference_problem():
    """Демонстрация проблемы со ссылками"""
    from homework import hello
    original_id = id(hello)
    
    with patch('homework.hello') as mock_hello:
        mock_hello.return_value = "mocked"
        
        # Старая ссылка всё ещё указывает на реальную функцию
        assert id(hello) == original_id  # ID не изменился
        assert hello() == "real"  # Вызывается реальная
        
        # Новая ссылка получит мок
        from homework import hello
        assert hello() == "mocked"  # Вызывается мок
    
    # После with ссылка может остаться на мок (если делали повторный импорт)
    # Поэтому всегда используйте обращение через модуль!


# ============= ИТОГОВЫЕ РЕКОМЕНДАЦИИ =============

"""
КЛЮЧЕВЫЕ ВЫВОДЫ:

1. ✅ Импортируйте МОДУЛЬ целиком: `import homework`
   - Тогда вы всегда будете обращаться к актуальному атрибуту: `homework.function()`

2. ✅ Если импортируете функцию, делайте это ПОСЛЕ применения патча
   - Или внутри контекста `with patch(...):`

3. ✅ Мокируйте ЗАВИСИМОСТИ функции, а не саму функцию
   - Например: `patch('module.time.sleep')` вместо `patch('module.aggregate_data')`

4. ✅ Если функция используется в другом месте, мокайте её там
   - Например: тестируете `process_report` → мокайте `aggregate_data`

5. ❌ НЕ импортируйте функцию ДО применения патча
   - Старая ссылка сохранится и будет игнорировать мок

ПРАВИЛЬНЫЕ ПАТТЕРНЫ:
- `import module` + `module.function()` внутри контекста
- `from module import function` ВНУТРИ контекста
- `patch('module.dependency')` для мока зависимостей
"""