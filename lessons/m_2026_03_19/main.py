from fastapi import FastAPI, Form, File, UploadFile, status
from pydantic import BaseModel
from typing import Optional, List


app = FastAPI(title="Моё первое API")

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    tags: List[str] = []

db = {}

@app.post("/items/json", status_code = status.HTTP_201_CREATED)
async def create_item_json(item: Item):
    """
    Принимает JSON в теле запроса
    """

    db[len(db)] = item.model_dump()

    return {
        "received": item.model_dump(),
        "message": f"Создан товар {item.name} ценой {item.price}"
    }


@app.get("/items/")
async def get_all_items():
    """
    Получаем все элементы из базы

    Пример запроса:
    curl -X GET http://localhost:8000/items/ \
    -H "Content-Type: application/json"
    """

    return db


@app.get("/items/{id}/")
async def get_item_by_id(id: int):
    """
    Получаем элемент из базы по id

    Пример запроса:
    curl -X GET http://localhost:8000/items/ \
    -H "Content-Type: application/json"
    """

    try:
        item = db[id]
    except KeyError:
        return "По такому индексу элемента нет"

    return item

