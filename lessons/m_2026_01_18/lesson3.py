"""
Задача 3: Найти книгу с самым поздним годом издания
"""

# latest_book = max(books, key=books.get)
# latest_year = books[latest_book]

# print(f"Книга с самым поздним годом издания: {latest_book} ({latest_year})")




def get_latest_book_and_year(books):
    latest_book = None
    latest_year = -1
    for book, year in books.items():
        if year > latest_year:
            latest_year = year
            latest_book = book
    return latest_book, latest_year

result= get_latest_book_and_year(books)
print(result)