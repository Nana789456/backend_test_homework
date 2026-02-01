"""
#дз
- Повторить пройденный материал:
    - аргументы VS параметры (применительно к фукциям)
    - какие бывают аргументы и их практическое применение
    - какие бывают параметры и их практическое применение
    - что такое *args и **kwargs
    - алгоритмическую сложность на примере работы с set, tuple, list
- Изменяемы и не изменяемые объекты в python
- Изучить области видимости
- Решить задачу
- Подготовить вопросы
"""

"""
Задача:
Нужно найти всех "двоечников" — тех, у кого средний балл ХОТЯ БЫ по одному предмету ниже 3.

Цель

Необходимо:
- Дописать get_average_value
- Дописать is_low_achiever
- Разобраться как работает filter
"""

students_data = {
    'Иванов': {'Математика': [2, 3, 2], 'Физика': [5, 5, 5]},
    'Петров': {'Математика': [5, 5, 5], 'Физика': [5, 4, 5]},
    'Попов': {'Математика': [4, 4, 3], 'Физика': [3, 2, 2]},
    'Кузнецов': {'Математика': [5, 1, 5], 'Физика': [3, 4, 4]}
}


def get_average_value(marks):
# Вычисляем среднее арифметическое списка оценок.

    if len(marks) == 0:
        return 0.0
    return sum(marks) / len(marks)

def is_failing(marks):

# Возвращает True, если средний балл < 3, то пользователь «двоечник».

    return get_average_value(marks) < 3

def get_failing_users(students_data):
    failing_users = {}
    failing_users_list = []
    print("Пользователи-«двоечники» (средний балл < 3):")
    for user, subjects in students_data.items(): # user - 'Иванов', subjects - {'Математика': [2, 3, 2], 'Физика': [5, 5, 5]}
        for subject, marks in subjects.items(): # subject - 'математика', marks - [2, 3, 2]
            if is_failing(marks):
                failing_users[user] = marks
                avg = get_average_value(marks)
                failing_users_list.append(user)
                # print(f"  {user}: {marks}, средний балл: {avg:.2f}")
    return failing_users_list


print(get_failing_users(students_data))
