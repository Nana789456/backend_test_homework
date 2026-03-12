from fastapi import FastAPI


app = FastAPI(title="Моё первое API")

@app.get("/")
def read_root():
    return {"message": "ping"}


# Ручки нужно располагать от оббщего к частному, т.е. /users должно идти до /users/{id}
@app.get("/users")
def get_users(name:str = ''):
    """Получить список всех пользователей"""
    users = [
        {"id": 1, "name": "Иван", "age": 25},
        {"id": 2, "name": "Мария", "age": 30}
    ]

    filtered_users = []

    for user in users:
        if name == user["name"]:
            filtered_users.append(user["age"])

    return filtered_users


# Плохой вариант разделение ролей ручек
# @app.get("/users/{id_or_name}/")
# def get_users_by_id(id_or_name: int | str):
#     """Получить список всех пользователей"""
#     users = [
#         {
#             "id": 3, 
#             "name": "Mary", 
#             "age": 30
#         },
#         {
#             "id": 1, 
#             "name": "Ivan",     
#             "age": 25
#         },
#         {
#             "id": 2, 
#             "name": "Mary", 
#             "age": 30
#         }
#     ]

#     if isinstance(id_or_name, int):
#         try:
#             user = users[id_or_name]
#         except IndexError:
#             return 'Пользователь не найден'
        
#     return user


@app.get("/users/{name}/")
def get_users_name(name: str | int):
    """Получить список всех пользователей"""
    
    name_is_int = True
    
    users = [
        {
            "name": "Mary", 
            "age": 30
        },
        {
            "name": "Ivan",     
            "age": 25
        },
        {
            "name": "Jon", 
            "age": 30
        }
    ]

    try:
        name = int(name)
    except Exception:
        name_is_int = False

    if name_is_int:
        try:
            user = users[name]
            return user
        except IndexError:
            return 'Пользователь не найден'
    else:
        for user in users:
            if user["name"] == name:
                return user
        

# @app.get("/users/{id}/")
# def get_users_by_id(id: int):
#     """Получить список всех пользователей"""
#     users = [
#         {
#             "name": "Mary", 
#             "age": 30
#         },
#         {
#             "name": "Ivan",     
#             "age": 25
#         },
#         {
#             "name": "Mary", 
#             "age": 30
#         }
#     ]

#     try:
#         user = users[id]
#     except IndexError:
#         return 'Пользователь не найден'
        
#     return user


