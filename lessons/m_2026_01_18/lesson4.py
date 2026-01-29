"""
Задача 4: Отфильтровать пользователей-«двоечников» и написать тесты
"""

# Используйте:
# - функцию get_average_value (как в нашем примере),
# - функцию filter()

# Шаги:
# - Напишите или используйте уже готовую функцию get_average_value(key).
# - Напишите предикатную функцию (возвращающую True/False)


# def get_average_value(key):
#     marks = user_marks[key]
#     sum_marks = sum(marks)
#     number_marks = len(marks)
#     average = sum_marks / number_marks
#     return average


# def is_failing(key):
#     avg = get_average_value(key)
#     return avg < 3.0

# failing_students = list(filter(is_failing, user_marks.keys()))
# print(f"Пользователи-«двоечники»: {failing_students}")

def get_average_value(marks):

# Вычисляем среднее арифметическое списка оценок.

    if len(marks) == 0:
        return 0.0
    return sum(marks) / len(marks)

def is_failing(marks):

# Возвращает True, если средний балл < 3, то пользователь «двоечник».

    return get_average_value(marks) < 3

def get_failing_users(user_marks):
    failing_users = {}
    print("Пользователи-«двоечники» (средний балл < 3):")
    for user, marks in user_marks.items():
        if is_failing(marks):
            failing_users[user] = marks
            avg = get_average_value(marks)
            print(f"  {user}: {marks}, средний балл: {avg:.2f}")
    return failing_users
