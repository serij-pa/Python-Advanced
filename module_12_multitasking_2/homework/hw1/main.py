import logging
import multiprocessing
import sqlite3
import time
import requests
from multiprocessing.pool import ThreadPool


logging.basicConfig(level=logging.INFO)
logger :logging.Logger = logging.getLogger(__name__)

URL: str ="https://www.swapi.tech/api/people/"

count = 1


def url_hero():
    list_url = []
    for i in range(1, 22):
        list_url.append(URL + str(i))
    return list_url


def get_hero(url: str):
    my_reg = requests.get(url, timeout=(5, 15))
    if my_reg.status_code != 200:
        return "Что то пошло не так."
    data = my_reg.json()
    hero = (data["result"]["properties"]['name'], data["result"]["properties"]["birth_year"], data["result"]["properties"]["gender"])
    return hero


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


def load_heroes_pool():
    start = time.time()
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        res = pool.map(get_hero, url_hero())
        #pool.close()
    pool.join()
    end = time.time()
    logger.info(f"Время работы программы c POOL {end - start}")
    return res


def load_heroes_threadPool():
    start = time.time()
    with ThreadPool(processes=multiprocessing.cpu_count()) as threads:
        res = threads.map(get_hero, url_hero())
    threads.join()
    end = time.time()
    logger.info(f"Время работы программы c ThreadPool {end - start}")
    return res


def record_db(list_heroes):
    with sqlite3.connect("star_wars_db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS heroes (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age TEXT NOT NULL,
            gender TEXT NOT NULL)
        """)
        for hero in list_heroes:
            if hero is not None:
                cursor.execute(f"INSERT INTO heroes (id, name, age, gender) VALUES (?, ?, ?, ?)", hero)


if __name__ == "__main__":
    hp = load_heroes_pool()
    #record_db(hp)
    ht = load_heroes_threadPool()
    #record_db(ht)

