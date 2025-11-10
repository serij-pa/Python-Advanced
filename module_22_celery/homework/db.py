import sqlite3
from flask import jsonify

def get_table(db_name):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("select email from emails")
        #cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        result = cursor.fetchall()
        return [res for res in result]

if __name__ == "__main__":
    nam_db = "my_email.db"
    tab_name = get_table(nam_db)
    if tab_name:
        for tab in tab_name:
            print(tab[0])