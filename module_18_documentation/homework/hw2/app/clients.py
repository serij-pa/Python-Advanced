import json
import multiprocessing
import time
from multiprocessing.pool import ThreadPool

import requests

import logging

logging.basicConfig(level=logging.DEBUG)


class BookClient:
    URL: str = 'http://0.0.0.0:5000/api/books'
    TIMEOUT: int = 5

    def __init__(self):
        self.session = requests.Session()

    def get_all_books(self) -> dict:
        response = self.session.get(self.URL, timeout=self.TIMEOUT)
        return response.json()

    def add_new_book(self, data):
        response = self.session.post(self.URL, json=data, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def delete_book_by_id(self, book_id):
        response = self.session.delete(self.URL + f"/{book_id}", timeout=self.TIMEOUT)
        return response.json()

    def get_book_by_id(self, book_id):
        response = self.session.get(self.URL + f"/{book_id}", timeout=self.TIMEOUT)
        return response.json()

    def put_book_by_id(self, book_id, data):
        response = self.session.put(self.URL + f"/{book_id}", json=data, timeout=self.TIMEOUT)
        return response.json()


class AuthorClient:
    URL: str = 'http://0.0.0.0:5000/api/authors'
    TIMEOUT: int = 5

    def __init__(self):
        self.session = requests.Session()

    def get_all_authors(self) -> dict:
        response = self.session.get(self.URL, timeout=self.TIMEOUT)
        return response.json()

    def add_new_authors(self, data):
        response = self.session.post(self.URL, json=data, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def get_all_book_by_author_id(self, author_id):
        response = self.session.get(self.URL + f"/{author_id}", timeout=self.TIMEOUT)
        return response.json()

    def delete_author_by_id(self, author_id):
        response = self.session.delete(self.URL + f"/{author_id}", timeout=self.TIMEOUT)
        return response.status_code

list_of_opening_hours =[]

def list_url(number, book_id):
    urls = []
    for i in range(number):
        urls.append(client.URL + f'/{book_id}')
    return urls

def working_hours(number, mode=None):
    start = time.time()
    if mode is None:
        for _ in range(number):
            client.get_all_books()
    elif mode == 1:
        for _ in range(number):
            client.session.get(client.URL)
    stop = time.time() - start
    list_of_opening_hours.append(stop)

def working_hours_by_threadpool(number, mode=None):
    start = time.time()
    with ThreadPool(processes=multiprocessing.cpu_count()) as threads:
        if mode is None:
            threads.map(client.get_book_by_id, [1] * number)
        elif mode == 1:
            threads.map(client.session.get, list_url(number, book_id=1))

    threads.join()
    stop = time.time() - start
    list_of_opening_hours.append(stop)


if __name__ == '__main__':
    client = BookClient()
    #client.session.post(client.URL, data=json.dumps({'title': 'Анна Каренина', 'author': 3}), headers={'content-type': 'application/json'})
    working_hours(10)
    working_hours(100)
    working_hours(1000)
    working_hours(10, 1)
    working_hours(100, 1)
    working_hours(1000, 1)
    working_hours_by_threadpool(10)
    working_hours_by_threadpool(100)
    working_hours_by_threadpool(1000)
    working_hours_by_threadpool(10, 1)
    working_hours_by_threadpool(100, 1)
    working_hours_by_threadpool(1000, 1)
    print(f"Время работы 10 простых запросов {list_of_opening_hours[0]}")
    print(f"Время работы 100 простых запросов {list_of_opening_hours[1]}")
    print(f"Время работы 1000 простых запросов {list_of_opening_hours[2]} \n")
    print(f"Время работы 10 запросов с сессией {list_of_opening_hours[3]}")
    print(f"Время работы 100 запросов с сессией {list_of_opening_hours[4]}")
    print(f"Время работы 1000 запросов с сессией {list_of_opening_hours[5]}\n")
    print(f"Время работы 10 запросов с потоком {list_of_opening_hours[6]}")
    print(f"Время работы 100 запросов с потоком {list_of_opening_hours[7]}")
    print(f"Время работы 1000 запросов с потоком {list_of_opening_hours[8]} \n")
    print(f"Время работы 10 запросов с потоком с сессией {list_of_opening_hours[9]}")
    print(f"Время работы 100 запросов с потоком с сессией {list_of_opening_hours[10]}")
    print(f"Время работы 1000 запросов с потоком с сессией {list_of_opening_hours[11]} \n")