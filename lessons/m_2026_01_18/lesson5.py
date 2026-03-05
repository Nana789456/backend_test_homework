def get_average_value(student_subjects):
    pass

def is_low_achiever(student_record):
    student_name, subjects_dict = student_record
    average = get_average_value(subjects_dict)
    ...

students_data = {
    'Иванов': {'Математика': [2, 3, 2], 'Физика': [5, 5, 5]},
    'Петров': {'Математика': [5, 5, 5], 'Физика': [5, 4, 5]},
    'Попов': {'Математика': [4, 4, 3], 'Физика': [3, 2, 2]},
    'Кузнецов': {'Математика': [5, 1, 5], 'Физика': [3, 4, 4]}
}

low_achievers = dict(filter(is_low_achiever, students_data.items()))
print(low_achievers)
