import sqlite3
from typing import Optional, List

def init_db_1():
    with sqlite3.connect('hotel.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_hotel'; 
            """)
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript("""
            CREATE TABLE IF NOT EXISTS table_hotel 
            (roomId INTEGER PRIMARY KEY AUTOINCREMENT, 
            firstName VARCHAR(30),
            lastName VARCHAR(30),
            floor INTEGER DEFAULT 1,
            guestNum INTEGER DEFAULT 1,
            beds INTEGER DEFAULT 1,
            price INTEGER DEFAULT 2500,
            checkIn INTEGER,
            checkOut INTEGER,
            archive INTEGER DEFAULT 0
            )
            """)


DESCRIPTION_ROOM = [
    {'roomId': 0, 'floor': 1, 'beds': 1, 'guestNum': 1, 'price': 2500},
    {'roomId': 1, 'floor': 1, 'beds': 1, 'guestNum': 2, 'price': 2000},
    {'roomId': 2, 'floor': 1, 'beds': 1, 'guestNum': 3, 'price': 2500},
]


def init_db_rooms(initial_records: List[dict]) -> None:
    with sqlite3.connect('hotel.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='rooms'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `rooms` (
                    roomId INTEGER PRIMARY KEY AUTOINCREMENT, 
                    floor INTEGER, 
                    beds INTEGER,
                    guestNum INTEGER,
                    price INTEGER
                )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `rooms`
                (floor, beds, guestNum, price) VALUES (?, ?, ?, ?)
                """,
                [
                    (item['floor'], item['beds'], item['guestNum'], item['price'])
                    for item in initial_records
                ]
            )


def init_db_booking() -> None:
    with sqlite3.connect('hotel.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='booking'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `booking` (
                    roomId INTEGER PRIMARY KEY AUTOINCREMENT, 
                    floor INTEGER, 
                    beds INTEGER,
                    guestNum INTEGER,
                    price INTEGER
                )
                """
            )


if __name__ == "__main__":
    init_db_rooms(DESCRIPTION_ROOM)
    init_db_booking()
    with sqlite3.connect("hotel.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM booking")
        users = cursor.fetchall()
        print(users)
        for user in users:
            print(user)