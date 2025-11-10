import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict


BOOKS = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 1},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 2},
    {'id': 3, 'title': 'War and Peace', 'author': 3},
]

AUTHORS = [
    {'author_id': 1, 'first_name': 'Chitlur', 'last_name': 'Swaroop', 'middle_name': '_'},
    {'author_id': 2, 'first_name': 'Herman', 'last_name': 'Melville', 'middle_name': '_'},
    {'author_id': 3, 'first_name': 'Leo', 'last_name': 'Tolstoy', 'middle_name': 'Nikolaevich'}
]

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'


@dataclass
class Book:
    title: str
    author: str
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[int] = None
    author_id: Optional[int] = None

    def __getitem__(self, item):
        return getattr(self, item)


def init_db(initial_authors, initial_books):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()

        # создаем таблицу авторов
        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{AUTHORS_TABLE_NAME}';
            """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f"""
                CREATE TABLE `{AUTHORS_TABLE_NAME}`(
                    author_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    middle_name VARCHAR(50)
                    );
                """
            )
            cursor.executemany(
                f"""
                INSERT INTO `{AUTHORS_TABLE_NAME}`
                (first_name, last_name, middle_name) VALUES (?, ?, ?)
                """,
                [
                    (item['first_name'], item['last_name'], item['middle_name'])
                    for item in initial_authors
                ]
            )

        # создаем таблицу книг
        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{BOOKS_TABLE_NAME}';
            """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f"""
                CREATE TABLE `{BOOKS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT,
                    author INTEGER NOT NULL REFERENCES autors(autor_id) ON DELETE CASCADE
                );
                """
            )
            cursor.executemany(
                f"""
                INSERT INTO `{BOOKS_TABLE_NAME}`
                (title, author) VALUES (?, ?)
                """,
                [
                    (item['title'], item['author'])
                    for item in initial_books
                ]
            )


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author=row[2])


def _get_author_obj_from_row(row: tuple):
    return Author(author_id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3])


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def get_all_authors():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{AUTHORS_TABLE_NAME}`')
        all_authors = cursor.fetchall()
        return [_get_author_obj_from_row(row) for row in all_authors]


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (title, author) VALUES (?, ?)
            """,
            (book.title, book.author)
        )
        book.id = cursor.lastrowid
        return book

def add_author(author: Author):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{AUTHORS_TABLE_NAME}` 
            (first_name, last_name, middle_name) VALUES (?, ?)
            """,
            (author.first_name, author.last_name, author.middle_name)
        )
        author.author_id = cursor.lastrowid
        return author


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?
            """,
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {BOOKS_TABLE_NAME}
            SET title = ?, author = ?
            WHERE id = ?
            """,
            (book.title, book.author, book.id)
        )
        conn.commit()


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?
            """,
            (book_id,)
        )
        conn.commit()


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE title = ?
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


if __name__ == "__main__":
    init_db(AUTHORS, BOOKS)
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {BOOKS_TABLE_NAME}")
        users = cursor.fetchall()
        print(users)
        for user in users:
            print(user)