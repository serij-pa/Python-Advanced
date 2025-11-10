import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("star_wars_heroes_db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM heroes")
        users = cursor.fetchall()
        print(users)
        for user in users:
            print(user)