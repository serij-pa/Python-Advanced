from pathlib import Path
import time
import threading
import requests


URL = 'https://cataas.com/cat'
#CATS_WE_WANT = 10
OUT_PATH = Path(__file__).parent / 'cats_thread'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()

def get_cat(idx: int) -> bytes:
    response = requests.get(URL)
    #print(f"{response.status_code}", end=" ")
    result = response.content
    write_to_disk(result, idx)


def write_to_disk(content: bytes, id: int):
    file_path = "{}/{}.png".format(OUT_PATH, id)
    with open(file_path, mode='wb') as f:
        f.write(content)


def get_all_cats(number_cats):
    threads = [threading.Thread(target=get_cat, args=(i,)) for i in range(number_cats)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def main_thread(number_cats):
    start = time.time()
    print(f"Начало загрузки {number_cats} котиков c threading")
    res = get_all_cats(number_cats)
    lead_time = round((time.time() - start), 5)
    print(f"Время выполнения {lead_time} сек.\n")
    return lead_time

if __name__ == '__main__':
    main_thread(3)
