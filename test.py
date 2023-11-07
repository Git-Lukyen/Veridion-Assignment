import asyncio

import aiohttp
import requests

links = ['https://www.google.com', 'https://www.facebook.com']


async def get_links():
    async with aiohttp.ClientSession() as session:
        results = []
        for url in links:
            resp = await session.get(url)
            results.append(await resp.text())

        print(results)


asyncio.run(get_links())
