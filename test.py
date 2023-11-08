import asyncio

import aiohttp
import httpx
import requests

links = ['https://www.umbrawindowtinting.com', 'http://www.embcmonroe.org', 'http://www.caffeygroup.com',
         'http://www.sk4designs.com', 'http://www.draftingdesign.com', 'http://www.truesdail.com',
         'http://www.seedsourceag.com', 'http://www.romebeerfest.com', 'http://www.beerock.com',
         'http://www.cabwhp.org', 'http://www.saintmlc.com', 'http://www.dillonmusic.com', ]
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
headers = {
    'User-Agent': user_agent
}


async def get_links():
    limits = httpx.Limits(max_keepalive_connections=100, max_connections=3000)
    async with httpx.AsyncClient(headers=headers, verify=False, follow_redirects=True, limits=limits) as client:
        reqs = [client.get(link) for link in links]
        results = await asyncio.gather(*reqs, return_exceptions=True)

    return results


print(asyncio.run(get_links()))
