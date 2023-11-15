import asyncio

import httpx

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
headers = {
    'User-Agent': user_agent
}


async def get_pages(links, timeout):
    """
    Get all the pages from links asynchoronously
    :param links: page links
    :param timeout: request timeout
    :return:
    """
    limits = httpx.Limits(max_keepalive_connections=100, max_connections=3000)
    async with httpx.AsyncClient(headers=headers, verify=False, follow_redirects=True, limits=limits,
                                 timeout=timeout) as client:
        reqs = [client.get(link, timeout=20) for link in links]
        results = await asyncio.gather(*reqs, return_exceptions=True)

    return results
