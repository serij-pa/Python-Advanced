import sqlite3


DESCRIPTION_BOOK = [
    {'id': 0, 'description': "Это самоучитель ", 'view_counter': 0, 'book_number': 1},
    {'id': 1, 'description': "Жажда мести ", 'view_counter': 0, 'book_number': 2},
    {'id': 2, 'description': "описывающий русское общество ", 'view_counter': 0, 'book_number': 3}
]
def create_table_description_book(initial_description):
    ...

if __name__ == "__main__":
    #create_table_description_book(DESCRIPTION_BOOK)
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='description_book'; 
            """)
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript("""
            CREATE TABLE IF NOT EXISTS description_book 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL, view_counter INTEGER, book_number INTEGER REFERENCES table_books(id))
            """)
            #(id INTEGER PRIMARY KEY AUTOINCREMENT, desc, view, book_number)
            #(id INTEGER PRIMARY KEY AUTOINCREMENT, desc TEXT NOT NULL, view INTEGER, book_number INTEGER REFERENCES table_books(id))
            #cursor.execute("INSERT INTO description_book (desc, view) VALUES (?, ?)", (DESCRIPTION_BOOK[0]["description"], DESCRIPTION_BOOK[0]["view_counter"]))
            cursor.executemany("INSERT INTO description_book (description, view_counter, book_number) VALUES (?, ?, ?)", [(item["description"], item["view_counter"], item["book_number"]) for item in DESCRIPTION_BOOK])


    with sqlite3.connect("table_books.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM table_books")
        users = cursor.fetchall()
        print(users)
        for user in users:
            print(user)