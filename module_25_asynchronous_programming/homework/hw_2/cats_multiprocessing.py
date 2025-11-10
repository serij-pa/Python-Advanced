from pathlib import Path
import time
import multiprocessing
import requests


URL = 'https://cataas.com/cat'
#CATS_WE_WANT = 10
OUT_PATH = Path(__file__).parent / 'cats_multiprocessing'
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
    queue = multiprocessing.Queue()
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    for num_cts in range(number_cats):
        queue.put(get_cat(num_cts))
    queue.close()
    queue.join_thread()
    pool.close()
    pool.join()


def main_multiproc(number_cats):
    start = time.time()
    print(f"Начало загрузки {number_cats} котиков c multiprocessing")
    res = get_all_cats(number_cats)
    lead_time = round((time.time() - start), 5)
    print(f"Время выполнения {lead_time} сек.\n")
    return lead_time

if __name__ == '__main__':
    main_multiproc(3)
