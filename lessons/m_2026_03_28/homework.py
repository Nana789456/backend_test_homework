"""
#дз
- Повторить проейденный материал
- Повторить работу запросов через Postman
- Попробовать поделать запросы swagger 1
Адрес:
http://localhost/docs
- Изучить что такое Авторизация и попробовать реализовать
- Изучить что такое моки
- Изучить мокирование запросов
- Подготовить вопросы
"""

# from fastapi import FastAPI, Form, File, UploadFile, status, Request
# from pydantic import BaseModel
# from typing import Optional, List


# app = FastAPI(title="Моё первое API")

# class Category(BaseModel): # данный класс описывает тело нашего запроса, какие поля и каких типов мы ожидаем в запросе
#     name: str
#     slug: str
#     description: str = None
#     tags: List[str] = []


# @app.post("/api/v1/categories/", status_code = status.HTTP_201_CREATED)
# async def create_item_json(request: Request, age: int, item: Category):
#     print(request.headers)
#     return {
#             "received": item.model_dump(),
#             "message": f"Создана категория {item.name} со слагом {item.slug} с возрастом {age}"
#         }


import requests

def get_weather(city):
    # Реальный HTTP-запрос
    response = requests.get(f"api.weather.com/{city}")
    return response.json()
