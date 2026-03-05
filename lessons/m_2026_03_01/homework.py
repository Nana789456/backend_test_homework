"""
#дз
- Повторить проейденный материал
- Залить все изменения на GitHub, чтобы на локалке не копились НЕ закоммиченые изменения
- Решить ДЗ
- Установить Postman
- Обратиться к ручкам (сделать запросы на наш сервер к функциям, что прописали) через Postman
- Изучить GET/POST/PUT/DELETE запросы
- Подготовить вопросы
"""

"""
Домашнее задание: FastAPI — параметры пути и query-параметры

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
@app.get("/user/{name}")
async def user(name: str, age: int = None):
    if age == None:
        return {"name": name, "message": "Возраст не указан"}
    elif age < 18:    
        return {"name": name, "message": "Доступ запрещен"}
    else:
        return {"name": name, "message": "Доступ разрешен"}


product_boxes = [
    ("яблоки", "фрукты", True),
    ("помидоры", "овощи", True),
    ("огурцы", "овощи", False),
]

@app.get("/products/")
async def products_handler(category: str = None, in_stock: bool = False):

    filtered_products = []

    if category:
        for product_box in product_boxes:
            if category in product_box:
                product_name = product_box[0]
                filtered_products.append(product_name)
    
    if in_stock:
        for product_box in product_boxes:
            if True in product_box:
                product_name = product_box[0]
                filtered_products.append(product_name)
    return {"products": filtered_products}
