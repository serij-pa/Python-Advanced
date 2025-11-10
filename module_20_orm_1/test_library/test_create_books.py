import sqlite3
from typing import Any, Optional, List

books_list = []
quantyti = int(input("Ввдите количество книг для добавления : "))
for _ in range(quantyti):
    book = {}
    name = input("Название книги: ")
    book['name'] = name
    count = int(input("Количество книг: "))
    book['count'] = count
    release_date = input("дата выхода (%Y-%m-%d) 1900-01-01: ")
    book['release_date'] = release_date
    author_id = int(input("ID автора книги: "))
    book['author_id'] = author_id
    #print(book)
    books_list.append(book)
print(books_list)

def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('test.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='books'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT, 
                    count Integer,
                    release_date TEXT,
                    author_id Integer
                )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `books`
                (name, count, release_date, author_id) VALUES (?, ?, ?, ?)
                """,
                [
                    (item['name'], item['count'], item['release_date'], item['author_id'])
                    for item in initial_records
                ]
            )


if __name__ == "__main__":
    #create_table_description_book(DESCRIPTION_BOOK)
    init_db(books_list)
    with sqlite3.connect("test.db") as conn:
       cursor = conn.cursor()
       cursor.execute("SELECT * FROM books")
       users = cursor.fetchall()
       print(users)
