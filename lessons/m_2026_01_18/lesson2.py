"""
Задача 2: Найти студента с самой длинной фамилией
"""
students = ['Иванов', 'Петренко', 'Сидорова123', 'Абрамян', 'Ван']


# longest_surname = max(students, key=len) # сравниваем длину строк
# print({longest_surname}, {len(longest_surname)})

def get_longest_surname(surnames):
    longest_surname = ''
    max_surname_len = -1
    for surname in surnames:
        if len(surname) > max_surname_len:
            longest_surname = surname
            max_surname_len = len(surname)
    return longest_surname

result = get_longest_surname(students)
print(result)