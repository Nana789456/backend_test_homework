import time

db_cache = {}


def sum_num(num1, num2):
    time.sleep(5)
    return num1 + num2


def cache_fun(fun, *args):
    fun_name = fun.__name__
    hash_key = tuple([fun_name, args]) # hash_key - ("имя функции", (1, 2))

    if hash_key not in db_cache:
        db_cache[hash_key] = fun(*args) # при первом вызове функции проводим расчёты
        return db_cache[hash_key]
    else:
        time.sleep(1)
        return db_cache[hash_key] # при остальных вызовах - берём данные из кеша


print("start")

print(cache_fun(sum_num, 1, 2))
print(cache_fun(sum_num, 1, 2))

print(cache_fun(sum_num, 5, 2))
print(cache_fun(sum_num, 5, 2))

print(cache_fun(sum_num, 8, 10))
print(cache_fun(sum_num, 8, 10))

print(cache_fun(sum_num, 0, 10))


# У кеша есть время своей жизни, для того чтоббы оббеспечить актуальность данных в ответе 

import redis
import time
import json

# Подключаемся к Redis (по умолчанию localhost:6379)
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_weather(city):
    """
    Функция, которая имитирует запрос погоды с кешированием в Redis
    """
    # Пробуем получить данные из кеша
    cache_key = f"weather:{city}"
    cached_result = r.get(cache_key)
    
    if cached_result:
        print(f"Данные для {city} взяты из кеша!")
        return json.loads(cached_result)  # Преобразуем строку обратно в словарь, который понятен Python
    
    # Если в кеше нет - делаем "запрос"
    print(f"Запрашиваю погоду для {city}...")
    time.sleep(2)  # Имитация долгого запроса
    
    # Получили из какой-то функции
    result = {
        'city': city,
        'temperature': 20,
        'condition': 'солнечно',
        'humidity': 65
    }
    
    # Сохраняем в кеш на 30 секунд
    r.setex(cache_key, 30, json.dumps(result, ensure_ascii=False)) # через json.dumps сериализуем (переводим) в строку, которая поняьна БД для кеша, т.е. redis
    print(f"Данные для {city} сохранены в кеш")
    
    return result

# Тестируем
print(get_weather("Moscow"))  # Будет выполнен запрос
print(get_weather("Moscow"))  # Возьмется из кеша
print(get_weather("Moscow"))  # Возьмется из кеша

print("Ждем 31 секунду...")
time.sleep(31)

print(get_weather("Moscow"))  # Кеш истек - снова запрос
print(get_weather("Moscow"))  # Возьмется из кеша
print(get_weather("Moscow"))  # Возьмется из кеша



import redis
import time
import json
from functools import wraps

# Настройка подключения
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def redis_cache(ttl=60):
    """
    Декоратор для кеширования результатов функции в Redis
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Создаем ключ из имени функции и аргументов
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Пробуем получить из кеша
            cached = redis_client.get(key)
            if cached:
                print(f"Кеш HIT для {func.__name__}")
                return json.loads(cached)
            
            # Выполняем функцию
            print(f"Кеш MISS для {func.__name__}")
            result = func(*args, **kwargs)
            
            # Сохраняем в кеш
            redis_client.setex(key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

# Использование декоратора
@redis_cache(ttl=30)
def expensive_calculation(n):
    """Тяжелые вычисления"""
    print(f"Вычисляю... {n}")
    time.sleep(3)  # Имитация работы
    return n * n

# Тестируем
print(expensive_calculation(5))  # Вычислит
print(expensive_calculation(5))  # Из кеша
print(expensive_calculation(10)) # Вычислит