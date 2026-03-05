"""
#дз
- Повторить проейденный материал (именованные и НЕ именованные аргументы)
- Повторить FastAPI
- Решить ДЗ
- Подготовить вопросы
"""

"""
Домашнее задание: FastAPI — параметры пути и query-параметры

Задание 1: Приветствие
Создай ручку /hello/{name}, которая принимает имя пользователя и возвращает:
- {"message": "Привет, {name}!"} — если name передано
- Если добавить query-параметр age (необязательный), то дополни полями: {"message": "Привет, {name}!", "age": age}

Задание 2: Четное или нечетное
Создай ручку /check_number/{number}, которая принимает число и возвращает:
- {"number": number, "is_even": true} — если число четное
- {"number": number, "is_even": false} — если число нечетное

Задание 3: Калькулятор суммы
Создай ручку /sum/, которая через query-параметры принимает два числа a и b и возвращает их сумму.
- Пример: /sum/?a=5&b=3 → {"a":5, "b":3, "sum":8}

Задание 4: Проверка возраста
Создай ручку /user/{name}, которая принимает имя (path-параметр) и опциональный query-параметр age.
- Если age не передан: {"name": name, "message": "Возраст не указан"}
- Если age < 18: {"name": name, "message": "Доступ запрещен"}
- Если age >= 18: {"name": name, "message": "Доступ разрешен"}

Задание 5: Поиск по товарам
Создай ручку /products/, которая принимает query-параметры:
- category (строка, необязательный)
- in_stock (булево, по умолчанию false)

Нужно возвращать список товаров (придумай несколько товаров в коде).
- Если передан category — фильтруй по категории
- Если in_stock=true — показывай только товары в наличии (поле in_stock: true в товаре)
"""

from fastapi import FastAPI

app = FastAPI()

# Пишите код здесь


@app.get("/hello/{name}")
async def hello(name: str, age: int = None):
    return {"message": f"Привет, {name}!", "age": age}


# http://127.0.0.1:8000/hello/Bob





@app.get("/check_number/{number}")
async def check_number(number: int):
    if number % 2 == 0:
        return {"number": number, "is_even": True}
    else:    
        return {"number": number, "is_even": False}

# http://127.0.0.1:8000/check_number/24

# http://127.0.0.1:8000/check_number/19


@app.get("/sum/")
async def sum_numbers(a: int, b: int):
    return {"a": a, "b": b, "sum": sum([a, b])}


# @app.get("/sum/")
# async def sum(a: int, b: int):
#     sum_number = a + b
#     return {"a": a, "b": b, "sum": sum_number}