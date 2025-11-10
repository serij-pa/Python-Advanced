import logging
import sqlite3
import time
import threading
from typing import List

import requests

logging.basicConfig(level=logging.INFO)
logger :logging.Logger = logging.getLogger(__name__)

URL: str ="https://www.swapi.tech/api/people/"

count = 1


def get_hero(url: str):
    global count
    my_reg = requests.get(url, timeout=(5, 15))
    if my_reg.status_code != 200:
        return
    data = my_reg.json()

    if data is not None:
        hero = (count, data["result"]["properties"]['name'], data["result"]["properties"]["birth_year"], data["result"]["properties"]["gender"])
        cursor.execute(f"INSERT INTO heroes (id, name, age, gender) VALUES (?, ?, ?, ?)", hero)
    count += 1


def load_heroes() -> None:
    starts: float = time.time()
    for i in range(1, 22):
        url = URL + str(i)
        get_hero(url)

    logger.info("Время выполнения {:.4}".format(time.time() - starts))


def load_hero_multithread():
    starts: float = time.time()
    threads = []
    for i in range(1, 22):
        url = URL + str(i)
        thread = threading.Thread(target=get_hero, args=(url,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    logger.info("Время выполнения {:.4}".format(time.time() - starts))


if __name__ == "__main__":
    with sqlite3.connect("star_wars_db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS heroes (id INTEGER, 
            name TEXT NOT NULL, 
            age TEXT NOT NULL, 
            gender TEXT NOT NULL)
        """)
        #load_heroes()
        load_hero_multithread()