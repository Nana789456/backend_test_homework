def my_range_gen(n):
    counter = 0
    while counter < n:
        yield counter  # Здесь функция "замирает" и возвращает значение
        counter += 1

    # # Когда цикл завершится, функция "выйдет", и генератор выбросит StopIteration
    # while True:
    #     yield 'finish'

# Использование через цикл
# print("Работа генератора my_range_gen:")
# for i in my_range_gen(3):
#     print(i)

# Под капотом это выглядит так:
print("\nЧто под капотом:")
gen = my_range_gen(3) # Создается объект-генератор, код НЕ выполняется.
print(next(gen)) # Выполняется до первого yield, возвращает 0
print(next(gen)) # Продолжает с места остановки, возвращает 1
print(next(gen)) # Продолжает, возвращает 2
try:
    print(next(gen)) 
except StopIteration as e:
    print(e)

# print(next(gen)) 
# print(next(gen))
# print(next(gen))
# print(next(gen))
# print(next(gen))