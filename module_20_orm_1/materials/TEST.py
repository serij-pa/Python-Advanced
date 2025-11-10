import sqlite3
from flask import jsonify


if __name__ == "__main__":
    #create_table_description_book(DESCRIPTION_BOOK)

    with sqlite3.connect("materials_db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        result = cursor.fetchall()
        print(result)
        for res in result:
            print(res[0])

