import sqlite3
from typing import Any, Optional, List

author_list = []
quantyti = int(input("Введите количество авторов для добавления : "))
for _ in range(quantyti):
    author = {}
    name = input("Имя автора: ")
    author['name'] = name
    surname = input("Фамилия автора: ")
    author['surname'] = surname
    author_list.append(author)
print(author_list)

def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('test.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='authors'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `authors` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT, 
                    surname TEXT
                )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `authors`
                (name, surname) VALUES (?, ?)
                """,
                [
                    (item['name'], item['surname'])
                    for item in initial_records
                ]
            )


if __name__ == "__main__":
    init_db(author_list)
    with sqlite3.connect("test.db") as conn:
       cursor = conn.cursor()
       cursor.execute("SELECT * FROM authors")
       users = cursor.fetchall()
       print(users)
