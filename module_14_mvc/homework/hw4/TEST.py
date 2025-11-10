import sqlite3
from typing import Any, Optional, List

DATA: List[dict] = [
    {'id': 1, 'name': 'War and Peace', 'count': 1, 'release_date': '1873-01-16', 'author_id': 1},
    {'id': 2, 'name': 'Мастер и маргарита', 'count': 2, 'release_date': '1940-02-13', 'author_id': 2},
    {'id': 3, 'name': 'Собачье сердце', 'count': 2, 'release_date': '1925-01-03', 'author_id': 2},
    ]

def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('city_library.db') as conn:
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
    init_db(DATA)
    #create_table_description_book(DESCRIPTION_BOOK)

    with sqlite3.connect("city_library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        users = cursor.fetchall()
        print(users)
        for user in users:
            data = {'id': user[0], 'name': user[1], 'count': user[2], 'release_date': user[3], 'author_id': user[4]}
            print(data['descript'])