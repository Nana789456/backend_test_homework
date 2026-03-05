# Изучить тело запроса
from fastapi import FastAPI, Form, File, UploadFile
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

product_boxes = [
    ("яблоки", "c1", True),
    ("помидоры", "c2", True),
    ("огурцы", "c2", False),
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

"""
Задание 5: Поиск по товарам
Создай ручку /products/, которая принимает query-параметры:
- category (строка, необязательный)
- in_stock (булево, по умолчанию false)

Нужно возвращать список товаров (придумай несколько товаров в коде).
- Если передан category — фильтруй по категории
- Если in_stock=true — показывай только товары в наличии (поле in_stock: true в товаре)
"""