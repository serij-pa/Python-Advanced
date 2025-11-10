import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("homework.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM table_friendship_schedule")
        users = cursor.fetchall()

        for user in users:
            print(user)
        print(len(users))