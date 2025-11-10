import aiohttp
import aiofiles
import asyncio

from urllib.parse import urlsplit
from bs4 import BeautifulSoup

DEEP = 3
URL = {'https://distep.ru/'}

async def get_url(client: aiohttp.ClientSession, url, deep):
    async with client.get(url) as response:
        print(response.status)
        result = await response.read()
        soup = BeautifulSoup(result, 'html.parser')
        base = urlsplit(url).netloc.replace("www.", "")
        links = soup.find_all("a")
        if links:
            for i_link in links:
                link = i_link.get('href')
                if link:
                    if link.startswith('http') and base not in link:
                        URL.add(link)
                        await write_to_file(link)
    deep -= 1
    if deep > 0:
        tasks = [get_url(client, url, deep) for url in URL]
        return await asyncio.gather(*tasks)
    else:
        return await asyncio.sleep(5)


async def write_to_file(link_to_file):
    async with aiofiles.open('links.txt', 'a') as file:
        await file.write(f'{link_to_file}\n')


async def crawler():
    connector = aiohttp.TCPConnector(limit=10, ssl=False, force_close=True)
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(50), connector=connector,) as client:
        tasks = [get_url(client, url, DEEP) for url in URL]
        return await asyncio.gather(*tasks)


def main():
    asyncio.run(crawler())


if __name__ == '__main__':
    main()