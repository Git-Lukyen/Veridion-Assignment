import asyncio

from Util.get_links_from_file import get_links
from Util import scrape_page_for_address as address_fetcher
from Util import get_pages_async as gca

links = []
results = []
output_type = 'parquet'
index = 0


def start(input_path, type):
    global links, output_type, index, results

    # Reset current index back to 0
    index = 0

    # Initialize location scraper based on settings
    address_fetcher.start()

    # Initialize output and input objects
    links = get_links(input_path)
    output_type = type

    # Get page content async
    results = asyncio.run(gca.get_pages(links))
    print(results)


def finish():
    pass


def update(state):
    if not state:
        return

    global index

    url_to_scrape = links[index]
    page_to_scrape = results[index]
    index += 1

    address = address_fetcher.scrape_page(page_to_scrape, url_to_scrape)
    if address is not None:
        print(address)
