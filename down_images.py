from decorators import ResponseTimer
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from time import perf_counter, strftime
import asyncio, aiofiles, os, requests


async def main():
    with requests.get('https://pokemondb.net/pokedex/all') as response:
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', attrs={'id': 'pokedex'})
            images = (image['data-src'] for image in table.findAll('span', attrs={'class': 'img-fixed icon-pkmn'}))

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'}
    download_tasks = []
    sema_count = 100
    sema = asyncio.Semaphore(sema_count)
    async with ClientSession(headers=headers) as session:
        for image_endpoint in images:
            download_tasks.append(download(sema, session, image_endpoint))
        await asyncio.gather(*download_tasks)

async def download(sema, session, url):
    '''
    Makes async http requests and parses it with BeautifulSoup
    Download's the image that the first endpoint matched.
    If request fails, retries it in the excepion catch
    '''
    async with sema:
        start = perf_counter()
        filename = url.split('/')[-1]
        path = os.path.join(os.getcwd(), 'sprites', filename)
        async with session.get(url) as response:
            printer(response.status, response.url.path, start)
            if response.status == 200:
                async with aiofiles.open(path, 'wb') as aiof:
                    await aiof.write(await response.read())
                    await aiof.close()

def printer(status, url_path, start):
    '''Wraps the async response with usefull debugging stats'''
    print(
        f"{strftime('[%d/%m/%Y %H:%M:%S]')} {status}@{url_path!r} finished in {(perf_counter() - start):.2f}")


if __name__ == '__main__':
    requests.get = ResponseTimer(requests.get)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())