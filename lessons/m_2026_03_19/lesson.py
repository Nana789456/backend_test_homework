
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

# ==================== 2. Несколько JSON объектов ====================

class Order(BaseModel):
    user_id: int
    items: List[Item]

@app.post("/orders/json")
async def create_order(order: Order):
    """
    Принимает вложенный JSON
    """
    return {
        "user_id": order.user_id,
        "items_count": len(order.items),
        "total": sum(item.price for item in order.items)
    }

"""
curl -X POST http://localhost:8000/orders/json \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 123,
    "items": [
      {"name": "Ноутбук", "price": 999.99, "tags": ["электроника"]},
      {"name": "Мышь", "price": 29.99, "tags": ["периферия"]}
    ]
  }'
"""

# ==================== 3. Form Data (application/x-www-form-urlencoded) ====================

@app.post("/items/form")
async def create_item_form(
    name: str = Form(...),
    price: float = Form(...),
    description: str = Form(None)
):
    """
    Принимает данные из формы (x-www-form-urlencoded)
    """
    return {
        "name": name,
        "price": price,
        "description": description,
        "message": f"Создан товар {name} из формы"
    }

"""
curl -X POST http://localhost:8000/items/form \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=Книга&price=499.50&description=Фантастика"
"""

# ==================== 4. Multipart Form Data (с файлом) ====================

@app.post("/items/upload")
async def upload_item(
    name: str = Form(...),
    price: float = Form(...),
    file: UploadFile = File(...)
):
    """
    Принимает данные + файл (multipart/form-data)
    """
    # Читаем содержимое файла (в реальности сохранили бы)
    content = await file.read()
    file_size = len(content)
    
    return {
        "name": name,
        "price": price,
        "filename": file.filename,
        "file_size": file_size,
        "content_type": file.content_type
    }

"""
curl -X POST http://localhost:8000/items/upload \
  -F "name=Фото" \
  -F "price=1000" \
  -F "file=@/path/to/your/image.jpg"
"""

# ==================== 5. Raw Body (как строка/байты) ====================

from fastapi import Request

@app.post("/items/raw")
async def create_item_raw(request: Request):
    """
    Принимает тело запроса как сырые байты
    Полезно для XML, CSV и т.д.
    """
    body = await request.body()
    body_str = body.decode()
    
    return {
        "body_bytes": len(body),
        "body_sample": body_str[:100] if len(body_str) > 100 else body_str
    }

"""
curl -X POST http://localhost:8000/items/raw \
  -H "Content-Type: text/plain" \
  -d "какой-то сырой текст"
"""

# ==================== 6. Несколько параметров в JSON ====================

@app.post("/items/mixed")
async def create_item_mixed(
    item: Item,
    user_id: int,
    priority: str = "normal"
):
    """
    Смешиваем тело JSON и query параметры
    """
    return {
        "user_id": user_id,
        "priority": priority,
        "item": item.dict()
    }

"""
curl -X POST "http://localhost:8000/items/mixed?user_id=42&priority=high" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Смартфон",
    "price": 599.99,
    "tags": ["электроника"]
  }'
"""

# ==================== 7. Произвольный JSON (как словарь) ====================

from typing import Dict, Any

@app.post("/items/dynamic")
async def create_item_dynamic(data: Dict[str, Any]):
    """
    Принимает любой JSON без строгой схемы
    """
    return {
        "received_keys": list(data.keys()),
        "data": data
    }

"""
curl -X POST http://localhost:8000/items/dynamic \
  -H "Content-Type: application/json" \
  -d '{
    "любой": "ключ",
    "число": 123,
    "список": [1, 2, 3],
    "вложенность": {"a": 1, "b": 2}
  }'
"""

# ==================== 8. Список объектов ====================

@app.post("/items/bulk")
async def create_items_bulk(items: List[Item]):
    """
    Принимает массив объектов
    """
    return {
        "count": len(items),
        "items": [item.dict() for item in items],
        "total_price": sum(item.price for item in items)
    }

"""
curl -X POST http://localhost:8000/items/bulk \
  -H "Content-Type: application/json" \
  -d '[
    {"name": "Товар 1", "price": 100},
    {"name": "Товар 2", "price": 200},
    {"name": "Товар 3", "price": 300}
  ]'
"""

# ==================== 9. Смешанный Form Data с несколькими файлами ====================

@app.post("/items/multi-upload")
async def upload_multiple_files(
    description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """
    Принимает описание и несколько файлов
    """
    file_info = []
    for file in files:
        content = await file.read()
        file_info.append({
            "filename": file.filename,
            "size": len(content),
            "type": file.content_type
        })
    
    return {
        "description": description,
        "files_count": len(file_info),
        "files": file_info
    }

"""
curl -X POST http://localhost:8000/items/multi-upload \
  -F "description=Мои документы" \
  -F "files=@/path/to/file1.pdf" \
  -F "files=@/path/to/file2.jpg" \
  -F "files=@/path/to/file3.txt"
"""

# ==================== 10. Обработка ошибок валидации ====================

from fastapi import HTTPException, status

@app.post("/items/validate")
async def create_item_validate(item: Item):
    """
    Пример с дополнительной валидацией
    """
    if item.price < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Цена не может быть отрицательной"
        )
    
    if len(item.name) < 3:
        raise HTTPException(
            status_code=400,
            detail="Название должно быть минимум 3 символа"
        )
    
    return {"valid": True, "item": item.dict()}

"""
curl -X POST http://localhost:8000/items/validate \
  -H "Content-Type: application/json" \
  -d '{"name": "PS5", "price": -500}'
# Вернет ошибку 400 с деталями
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
Решаемая задача: Получение всех переданных query-параметров в FastAPI, даже если их количество заранее неизвестно.
"""

# Пример 1: Через Request
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/sum-params")
async def sum_params(request: Request):
    # Получаем все query параметры как словарь
    params = dict(request.query_params)
    
    # Суммируем только числовые значения
    total = 0
    for key, value in params.items():
        try:
            total += float(value)
        except ValueError:
            # Пропускаем нечисловые значения
            continue
    
    return {
        "all_params": params,
        "sum_of_numbers": total
    }

# Пример 2: Через Depends()
from fastapi import FastAPI, Depends, Query
from typing import Dict

app = FastAPI()

async def get_all_params(params: Dict[str, str] = Query(...)):
    return params

@app.get("/sum-params-v2")
async def sum_params_v2(all_params: Dict = Depends(get_all_params)):
    total = 0
    for value in all_params.values():
        try:
            total += float(value)
        except ValueError:
            continue
    
    return {
        "all_params": all_params,
        "sum_of_numbers": total
    }

from fastapi import FastAPI, Depends, Query

app = FastAPI()

# Специальный тип для сбора всех параметров
@app.get("/sum-params")
async def sum_params(all_params: dict = Depends(lambda: Query(...))):
    # Или более правильно:
    # all_params: dict = Depends(Query())
    # FastAPI поймет, что нужно собрать все query параметры
    total = 0
    for value in all_params.values():
        try:
            total += float(value)
        except ValueError:
            continue
    return {"sum": total, "params": all_params}




"""
Материал к занятию: Кеширование в FastAPI с библиотекой fastapi-cache
=====================================================================

Библиотека: https://github.com/long2ice/fastapi-cache
FastAPI: 0.133.0
Бэкенд: Redis (InMemory для первого примера)

Структура материала:
1. Быстрый старт: настройка и первый пример
2. Переход на Redis
3. Формирование ключа кеша (механика)
4. POST-запросы и проблема тела
5. Кастомный key_builder с хешем тела
6. Проблема порядка полей в теле
7. Инвалидация кеша
8. Подводные камни
9. Практические задания
"""

# =====================================================================
# 1. Быстрый старт: настройка и первый пример
# =====================================================================

"""
Тезис: Кеширование позволяет сохранять результат выполнения запроса
и отдавать его при повторных обращениях без повторения тяжелых вычислений.

Объяснение: Библиотека fastapi-cache поддерживает различные бэкенды:
InMemory, Redis, Memcached. Начнем с самого простого — InMemory.
"""

# Пример 1.1: Базовое кеширование с InMemory
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
import asyncio

app = FastAPI()

# Инициализация InMemory бэкенда
@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

@cache(expire=60)  # Кеш живет 60 секунд
@app.get("/heavy")
async def heavy_computation():
    # Имитация тяжелых вычислений
    await asyncio.sleep(3)
    return {"result": 42, "computed_at": "тяжелые вычисления"}

"""
Разбор примера:
1. Декоратор @cache оборачивает функцию и перехватывает вызовы
2. При первом запросе функция выполняется, результат сохраняется в кеш
3. При повторных запросах в течение 60 секунд возвращается сохраненный результат
4. Функция не выполняется повторно
"""

# =====================================================================
# 2. Переход на Redis
# =====================================================================

"""
Тезис: В production-среде используется Redis как общее хранилище кеша
для нескольких экземпляров приложения.

Объяснение: InMemory работает только в рамках одного процесса.
При рестарте приложения кеш теряется. Redis лишен этих недостатков.
"""

# Пример 2.1: Настройка Redis бэкенда
from fastapi_cache.backends.redis import RedisBackend
import aioredis

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@cache(expire=60)
@app.get("/heavy")
async def heavy_computation():
    await asyncio.sleep(3)
    return {"result": 42}

"""
Разбор примера:
1. FastAPICache.init() инициализирует глобальный экземпляр кеша
2. prefix добавляется ко всем ключам — полезно, если Redis используется и для других задач
3. RedisBackend автоматически сериализует/десериализует ответы
"""

# =====================================================================
# 3. Формирование ключа кеша (механика)
# =====================================================================

"""
Тезис: Ключ кеша формируется по принципу: {prefix}:{путь}?{query_params}

Объяснение: По умолчанию библиотека строит ключ на основе URL-пути
и query-параметров. Тело запроса НЕ учитывается.

Пример ключей в Redis:
# GET /users?page=1
KEY: "fastapi-cache:/users?page=1"
VALUE: '{"items": [...], "total": 100}'

# GET /users?page=2
KEY: "fastapi-cache:/users?page=2"
VALUE: '{"items": [...], "total": 100}'
"""

# Пример 3.1: GET с query параметрами
@cache(expire=60)
@app.get("/users")
async def get_users(page: int = 1, limit: int = 10):
    # Имитация запроса к БД с пагинацией
    return {
        "items": [f"user_{i}" for i in range((page-1)*limit, page*limit)],
        "page": page,
        "limit": limit,
        "total": 100
    }

"""
Разбор примера:
1. Разные значения page и limit создают разные ключи
2. Запросы с одинаковыми параметрами получают кешированный ответ
"""

# =====================================================================
# 4. POST-запросы и проблема тела
# =====================================================================

"""
Тезис: По умолчанию тело POST-запроса не участвует в формировании ключа кеша.

Объяснение: Библиотека считает, что POST — это всегда создание/изменение данных,
и кеширование обычно не применяется. Но если POST выполняет тяжелые вычисления
(например, расчет скоринга, генерация отчета), кеширование нужно, причем
результат зависит от тела запроса.
"""

# Пример 4.1: Проблема — тело не учитывается
@cache(expire=60)
@app.post("/calculate")
async def calculate(data: dict):
    # Тяжелые вычисления, зависящие от data
    # Проблема: запросы с разными телами получат один кеш!
    import time
    time.sleep(2)
    return {"result": sum(data.values()) if data else 0}

"""
Что произойдет:
- Первый запрос с {"a": 1, "b": 2} выполнится, результат сохранится
- Второй запрос с {"a": 100, "b": 200} получит тот же кеш,
  потому что ключ не учитывает тело
"""

# =====================================================================
# 5. Кастомный key_builder с хешем тела
# =====================================================================

"""
Тезис: Добавляем хеш тела запроса в ключ кеша через кастомный key_builder.

Объяснение: Нужно извлечь тело, преобразовать в стабильное строковое
представление и вычислить хеш. Библиотека позволяет подменить функцию
построения ключа.
"""

import hashlib
import json
from pydantic import BaseModel
from fastapi import Request

# Модель для примеров
class CalcRequest(BaseModel):
    a: int
    b: int
    operation: str = "sum"

# Пример 5.1: Вариант с Pydantic моделью (рекомендуется)
def body_key_builder(func, namespace, request, **kwargs):
    # Извлекаем Pydantic модель из kwargs
    data = kwargs.get('data')
    
    # Преобразуем в JSON с сортировкой ключей для стабильности
    body_json = data.json()  # у Pydantic моделей есть .json()
    body_hash = hashlib.md5(body_json.encode()).hexdigest()[:8]
    
    return f"{namespace}:{request.url.path}:{body_hash}"

@app.post("/calculate")
@cache(expire=300, key_builder=body_key_builder)
async def calculate(data: CalcRequest):
    # Тяжелые вычисления
    import time
    time.sleep(2)
    
    if data.operation == "sum":
        result = data.a + data.b
    elif data.operation == "multiply":
        result = data.a * data.b
    else:
        result = 0
    
    return {
        "result": result,
        "computed": True,
        "cached": False
    }

# Пример 5.2: Вариант с сырым Request (проблема однократного чтения тела)
async def request_body_key_builder(func, namespace, request, **kwargs):
    # Базовый ключ из пути и query
    key = f"{namespace}:{request.url.path}"
    if request.query_params:
        key += f"?{request.query_params}"
    
    # Добавляем хеш тела для POST/PUT/PATCH
    if request.method in ["POST", "PUT", "PATCH"]:
        # Важно: тело можно прочитать только один раз!
        body = await request.body()
        if body:
            body_hash = hashlib.md5(body).hexdigest()[:8]
            key += f":body:{body_hash}"
    
    return key

@app.post("/calculate-raw")
@cache(expire=300, key_builder=request_body_key_builder)
async def calculate_raw(request: Request):
    body = await request.json()
    import time
    time.sleep(2)
    
    result = sum(body.values()) if isinstance(body, dict) else 0
    
    return {
        "result": result,
        "computed": True,
        "cached": False
    }

"""
Разбор примеров:
1. Вариант с моделью чище и безопаснее: не тратит тело запроса,
   использует структурированные данные
2. Вариант с Request демонстрирует проблему однократного чтения тела
   (если тело уже читали до кеша, получить его не удастся)
3. Хеш обрезается до 8 символов для читаемости, коллизиями можно пренебречь
"""

# =====================================================================
# 6. Проблема порядка полей в теле
# =====================================================================

"""
Тезис: JSON с одинаковым содержимым, но разным порядком ключей дает
разные хеши → разные ключи.

Объяснение: Нужно нормализовать JSON перед хешированием — отсортировать ключи.
"""

# Пример 6.1: Стабильный key_builder с сортировкой ключей
def stable_body_key_builder(func, namespace, request, **kwargs):
    data = kwargs.get('data')
    
    # Получаем dict и сортируем ключи
    data_dict = data.dict()
    body_json = json.dumps(data_dict, sort_keys=True)
    body_hash = hashlib.sha256(body_json.encode()).hexdigest()[:8]
    
    return f"{namespace}:{request.url.path}:{body_hash}"

@app.post("/calculate-stable")
@cache(expire=300, key_builder=stable_body_key_builder)
async def calculate_stable(data: CalcRequest):
    import time
    time.sleep(2)
    
    result = data.a + data.b
    return {"result": result}

"""
Разбор примера:
1. sort_keys=True гарантирует одинаковый порядок ключей
2. SHA256 вместо MD5 — небольшая перестраховка, но можно использовать любой хеш
3. Запросы {"a":1, "b":2} и {"b":2, "a":1} теперь попадают в один кеш
"""

# =====================================================================
# 7. Инвалидация кеша
# =====================================================================

"""
Тезис: При изменении данных старый кеш нужно удалять.

Объяснение: Кешировать GET-запросы списка товаров — хорошо. Но при добавлении
нового товара кеш должен быть сброшен.
"""

from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

# Имитация базы данных
items_db = []

@app.post("/items")
async def create_item(item: Item):
    # Сохраняем в БД
    items_db.append(item.dict())
    
    # Инвалидируем кеш списка товаров
    redis = FastAPICache.get_backend().redis
    await redis.delete("fastapi-cache:/items")
    
    return {"id": len(items_db) - 1, **item.dict()}

@app.get("/items")
@cache(expire=3600)
async def get_items():
    # Вернет кешированный список или выполнит запрос
    return items_db

# Пример 7.2: Инвалидация по паттерну (все страницы пагинации)
@app.post("/items-bulk")
async def create_items_bulk(items: list[Item]):
    for item in items:
        items_db.append(item.dict())
    
    # Удаляем все ключи, начинающиеся с префикса /items
    redis = FastAPICache.get_backend().redis
    keys = await redis.keys("fastapi-cache:/items*")
    if keys:
        await redis.delete(*keys)
    
    return {"created": len(items)}

# Пример 7.3: Эндпоинт для ручной очистки кеша
@app.post("/admin/clear-cache/{path_prefix:path}")
async def clear_cache(path_prefix: str = ""):
    redis = FastAPICache.get_backend().redis
    pattern = f"fastapi-cache:{path_prefix}*" if path_prefix else "fastapi-cache:*"
    keys = await redis.keys(pattern)
    if keys:
        await redis.delete(*keys)
    return {"cleared_keys": len(keys) if keys else 0}

"""
Разбор примера:
1. После создания товара удаляем ключ списка товаров
2. При следующем GET /items запрос пойдет в БД и создаст новый кеш
3. Использование keys с паттерном позволяет сбросить кеш для всех страниц сразу
"""

# =====================================================================
# 8. Подводные камни
# =====================================================================

"""
Тезис: Нужно помнить об ограничениях при работе с кешированием.

1. Однократное чтение тела
2. Объем кеша
3. Сброс кеша при рестарте Redis
"""

# Пример 8.1: Проблема однократного чтения тела
from fastapi import HTTPException

@app.post("/wrong")
async def wrong(request: Request):
    # ⚠️ Так делать нельзя — тело будет потеряно для кеша
    body1 = await request.json()  # читаем тело
    # ... какой-то код
    # Если дальше вызывается эндпоинт с кешем, key_builder не сможет прочитать тело повторно
    return {"body": body1}

# Правильный подход — использовать зависимости
from fastapi import Depends

async def get_body(request: Request):
    return await request.json()

@app.post("/correct")
@cache(expire=60, key_builder=request_body_key_builder)
async def correct(body: dict = Depends(get_body)):
    # Тело доступно через dependency, key_builder тоже сможет его прочитать
    return {"result": sum(body.values())}

"""
Другие подводные камни:

- Объем кеша: при кешировании POST-запросов с большими телами ключи получаются
  длинными, а значения могут быть объемными. Контролировать через TTL.

- Сброс кеша при рестарте Redis: если Redis настроен без persistence,
  при перезапуске весь кеш теряется.
"""

# =====================================================================
# 9. Практические задания
# =====================================================================

"""
Задание 1. GET с параметрами
----------------------------
Реализовать эндпоинт /products с параметрами category и sort.
Закешировать на 5 минут.

Ожидаемый результат: запросы с одинаковыми параметрами получают кеш,
с разными — отдельные ключи.
"""

@app.get("/products")
@cache(expire=300)  # 5 минут
async def get_products(category: str = None, sort: str = "name"):
    # Имитация запроса к БД
    await asyncio.sleep(2)
    products = [
        {"id": 1, "name": "Product A", "category": "books", "price": 100},
        {"id": 2, "name": "Product B", "category": "electronics", "price": 200},
        {"id": 3, "name": "Product C", "category": "books", "price": 150},
    ]
    
    if category:
        products = [p for p in products if p["category"] == category]
    
    if sort == "price":
        products.sort(key=lambda x: x["price"])
    else:
        products.sort(key=lambda x: x["name"])
    
    return products

"""
Задание 2. POST с хешем тела
---------------------------
Реализовать эндпоинт /discount-calculate, который принимает JSON со списком товаров
и возвращает сумму скидки. Добавить кеширование на 10 минут с учетом тела запроса.

Ожидаемый результат: при повторной отправке того же списка товаров ответ берется из кеша.
"""

class CartItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class CartRequest(BaseModel):
    items: list[CartItem]
    promo_code: str = None

def cart_key_builder(func, namespace, request, **kwargs):
    cart = kwargs.get('cart')
    # Сортируем items для стабильности
    items_dict = [item.dict() for item in cart.items]
    items_dict.sort(key=lambda x: x['product_id'])
    
    data = {
        "items": items_dict,
        "promo_code": cart.promo_code
    }
    
    body_json = json.dumps(data, sort_keys=True)
    body_hash = hashlib.md5(body_json.encode()).hexdigest()[:8]
    
    return f"{namespace}:{request.url.path}:{body_hash}"

@app.post("/discount-calculate")
@cache(expire=600, key_builder=cart_key_builder)  # 10 минут
async def discount_calculate(cart: CartRequest):
    # Тяжелые вычисления скидки
    await asyncio.sleep(3)
    
    total = sum(item.quantity * item.price for item in cart.items)
    
    # Разные промокоды дают разную скидку
    discount = 0
    if cart.promo_code == "SAVE10":
        discount = total * 0.1
    elif cart.promo_code == "SAVE20":
        discount = total * 0.2
    
    return {
        "total": total,
        "discount": discount,
        "final": total - discount
    }

"""
Задание 3. Инвалидация
---------------------
Добавить эндпоинт /admin/clear-cache, который сбрасывает кеш для всех эндпоинтов,
начинающихся с /products.

Ожидаемый результат: вызов этого эндпоинта удаляет соответствующие ключи в Redis.
"""

@app.post("/admin/clear-products-cache")
async def clear_products_cache():
    redis = FastAPICache.get_backend().redis
    keys = await redis.keys("fastapi-cache:/products*")
    if keys:
        await redis.delete(*keys)
    return {
        "cleared": True,
        "keys_count": len(keys) if keys else 0,
        "message": f"Удалено {len(keys) if keys else 0} ключей кеша для /products"
    }

# =====================================================================
# Запуск приложения
# =====================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
