"""
#дз
- Повторить проейденный материал
- Установить Postman
- Обратиться к ручкам (сделать запросы на наш сервер к функциям, что прописали) через Postman
- Изучить GET/POST/PUT/DELETE запросы
- Изучить материал из lessons/m_2026_03_12/main.py
- Переносите код в этот файл и запускайте через 
uvicorn lessons.m_2026_03_14.homework:app --reload
- Подготовить вопросы
"""

# Изучить тело запроса
from fastapi import FastAPI, Form, File, UploadFile
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# ==================== 1. JSON Body (Pydantic модель) ====================

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    tags: List[str] = []

@app.post("/items/json")
async def create_item_json(item: Item):
    """
    Принимает JSON в теле запроса
    """
    return {
        "received": item.dict(),
        "message": f"Создан товар {item.name} ценой {item.price}"
    }

"""
curl -X POST http://localhost:8000/items/json \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ноутбук",
    "price": 999.99,
    "description": "Игровой ноутбук",
    "tags": ["электроника", "компьютеры"]
  }'
"""
