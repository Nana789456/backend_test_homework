"""
#дз
- Повторить проейденный материал (именованные и НЕ именованные аргументы)
- Повторить что такой JSON и чем он отличается от dict
- Познакомиться с библиотекой Pydantic (в lessons/m_2026_02_11/lesson.ipynb есть основа с чего можно начать)
- Изучить понятие "Кеширование"
- Кеширование + декораторы
- Подготовить вопросы
"""

import json

json_dict = {'game':'футбол', 'age': 21, 'score': None}
json_str = json.dumps(json_dict, ensure_ascii=True, indent=3)
print(type(json_str))
print(json_str[0])
print(json_str)
parsed_dict = json.loads(json_str)
print(type(parsed_dict))
print(parsed_dict)

json_tuple = (1,2)
json_str = json.dumps(json_tuple, ensure_ascii=True, indent=3)
print(type(json_str))
print(json_str)

parsed_tuple = json.loads(json_str)
print(type(parsed_tuple))
print(parsed_tuple)
python_tuple = tuple(parsed_tuple)
print(type(python_tuple))
print(python_tuple)
