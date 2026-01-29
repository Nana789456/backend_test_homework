"""
Задача 1: Найти пользователя с наименьшим средним баллом
"""


def get_user_with_min_average_value(users_marks):
    def get_average_value(key):
        marks = users_marks[key]
        sum_marks = sum(marks)
        number_marks = len(marks)
        average = sum_marks / number_marks
        return average
    
    return min(users_marks, key=get_average_value)

