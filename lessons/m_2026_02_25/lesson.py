from fastapi import FastAPI

# Создаем экземпляр приложения FastAPI
app = FastAPI()

# Определяем простой GET-эндпоинт
@app.get("/") # http://127.0.0.1:8000/
async def root():
    return {"message": "Hello, FastAPI!"}

# Эндпоинт с параметром в пути
@app.get("/books/{id}/{size}") # item_id - параметр пути, http://127.0.0.1:8000/items/1 - пример пути (адреса) запроса
async def read_item(id: int, size:int,  name: str = None, author: str = None,):  # q — необязательный query-параметр
    return {"id книги": id, "size": size, "название книги": name, "author": author}
