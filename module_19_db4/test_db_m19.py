import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("homework.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT count() FROM students")
        users = cursor.fetchall()
        print(len(users))
        for user in users:
            print(user)