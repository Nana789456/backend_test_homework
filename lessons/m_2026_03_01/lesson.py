from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    age: int = None

users_db = {}
user_counter = 1

# Через get запрос мы получает данные с сервера, т.е. сервер обраьатывает наш запрос и даёт ожидаемый нами ответ, например что-то подсчитать или что-то найти
# Через post запрос мы отправляем данные на сервер для изменения состояния даных на сервере, например добавление новой записи в базу данных
@app.post("/users/")
async def create_user(user: User):
    global user_counter
    user_id = user_counter
    users_db[user_id] = user
    user_counter += 1
    return {"id": user_id, **user.dict()}