import asyncio
import json
import requests
from pathlib import Path

import aiohttp
import time


URL = 'https://cataas.com/cat'
CATS_WE_WANT = 5
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()

async def get_cat(client: aiohttp.ClientSession, idx: int) -> bytes:
    async with client.get(URL) as response:
        print(f"{response.status}", end=" ")
        #print(type(response))
        result = await response.read()
        await asyncio.to_thread(write_to_disk, result, idx)


def write_to_disk(content: bytes, id: int):
    file_path = "{}/{}.png".format(OUT_PATH, id)
    with open(file_path, mode='wb') as f:
        f.write(content)


async def get_all_cats():

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        tasks = [get_cat(client, i) for i in range(CATS_WE_WANT)]
        return await asyncio.gather(*tasks)


def main():
    start = time.time()
    print(f"Начало загрузки {CATS_WE_WANT} котиков")
    res = asyncio.run(get_all_cats())
    print(len(res))
    print(f"Время выполнения {round((time.time() - start), 5)} сек.")


if __name__ == '__main__':
    main()
