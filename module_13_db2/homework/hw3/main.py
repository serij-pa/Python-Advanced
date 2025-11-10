import datetime
import sqlite3


def log_bird(
        cursors: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
) -> None:
    bird = (bird_name, count, date_time)
    cursors.execute(f"INSERT INTO birds (name, count, right_now) VALUES (?, ?, ?)", bird)


def check_if_such_bird_already_seen(
        cursor: sqlite3.Cursor,
        bird_name: str
) -> bool:
    resp = cursor.execute(f"SELECT EXISTS (SELECT * FROM birds WHERE name='{bird_name}')")
    result = resp.fetchone()[0]
    return result


if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name: str = input("Пожалуйста введите имя птицы: \n> ")
    count_str: str = input("Сколько птиц вы увидели?: \n> ")
    count: int = int(count_str)
    right_now: str = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect("../homework.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS birds (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        count INTEGER NOT NULL,
                        right_now VARCHAR NOT NULL)
        
        """)

        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")

        else:
            log_bird(cursor, name, right_now)
            print("Птица добавлена")