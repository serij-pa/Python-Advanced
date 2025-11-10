import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("SalesInfo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders")
        users = cursor.fetchall()
        print(users)
        for user in users:
            print(user)