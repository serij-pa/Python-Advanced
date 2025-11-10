import sqlite3
from flask import jsonify


if __name__ == "__main__":
    #create_table_description_book(DESCRIPTION_BOOK)

    with sqlite3.connect("test.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors")
        users = cursor.fetchall()
        print(users)
