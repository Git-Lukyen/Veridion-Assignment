import asyncio

import aiohttp

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
headers = {
    'User-Agent': user_agent
}


async def get_pages(links):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(session.get(link, headers=headers, timeout=5, ssl=False)) for link in links]
        results = []
        results = await asyncio.gather(*tasks, return_exceptions=True)

        return results
