import asyncio

from Util.get_links_from_file import get_links
from Util import scrape_page_for_address as address_fetcher
from Util import get_pages_async as gca

links = []
responses = []

found_addresses = {}
aux_links = []
failed_links = []

output_type = 'parquet'
timeout = 100

index = 0
scraping = False
scraping_aux = False
scraping_failed = False


def start(input_path, _type, _timeout, _scraping_aux=True, _scraping_failed=False):
    # Reset current index back to 0
    global index, scraping, scraping_aux, scraping_failed
    index = 0
    scraping = True
    scraping_aux = _scraping_aux
    scraping_failed = _scraping_failed

    # Initialize location scraper based on settings
    address_fetcher.start()

    # Initialize output and input objects
    global links, output_type, timeout
    links = get_links(input_path)
    output_type = _type
    timeout = _timeout

    # Get page content async
    global responses
    responses = asyncio.run(gca.get_pages(links[:20], timeout))


def finish():
    global scraping, scraping_aux, scraping_failed, responses, index

    if scraping_failed:
        index = 0
        scraping_failed = False

        global failed_links
        responses = asyncio.run(gca.get_pages(failed_links, timeout))
        return

    if scraping_aux:
        index = 0
        scraping_aux = False

        global aux_links
        responses = asyncio.run(gca.get_pages(aux_links, timeout))
        return

    scraping = False

    return 1


def update():
    if not scraping:
        return

    global index

    if index == len(responses):
        return finish()

    page_to_scrape = responses[index]
    index += 1

    try:
        if page_to_scrape.url.host in found_addresses:
            return
    except:
        return

    result = address_fetcher.scrape_page(page_to_scrape)

    if result.failed:
        failed_links.append(result.url)
    elif not result.found_adr and result.aux_links:
        aux_links.extend(result.aux_links)
    elif result.found_adr:
        found_addresses[result.url.host] = result.address
