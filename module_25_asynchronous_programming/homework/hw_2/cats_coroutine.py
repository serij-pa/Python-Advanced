import asyncio
from pathlib import Path
import time

import aiohttp
import aiofiles

URL = 'https://cataas.com/cat'
#CATS_WE_WANT = 10
OUT_PATH = Path(__file__).parent / 'cats_coroutine'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()

async def get_cat(client: aiohttp.ClientSession, idx: int) -> bytes:
    async with client.get(URL) as response:
        #print(f"{response.status}", end=" ")
        result = await response.read()
        await write_to_disk(result, idx)


async def write_to_disk(content: bytes, id: int):
    file_path = "{}/{}.png".format(OUT_PATH, id)
    async with aiofiles.open(file_path, mode='wb') as f:
        await f.write(content)


async def get_all_cats(number_cats):

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        tasks = [get_cat(client, i) for i in range(number_cats)]
        return await asyncio.gather(*tasks)


def main_corot(number_cats):
    start = time.time()
    print(f"Начало загрузки {number_cats} котиков c asyncio")
    res = asyncio.run(get_all_cats(number_cats))
    lead_time = round((time.time() - start), 5)
    #print(len(res))
    print(f"Время выполнения {lead_time} сек.\n")
    return lead_time

if __name__ == '__main__':
    main_corot(3)
