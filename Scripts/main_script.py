import asyncio
import time

from Util.get_links_from_file import get_links
from Util import scrape_page_for_address as address_fetcher
from Util import get_pages_async as gca
from Util import create_output_file as cof

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

__menu_ref = None


def start(input_path, _type, _timeout, _menu_ref, _scraping_aux=True, _scraping_failed=False):
    global __menu_ref
    __menu_ref = _menu_ref
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

    responses = get_responses(links, timeout)


def get_responses(_links, _timeout):
    update_status("Fetching pages from urls, please wait.")
    _responses = []

    for i in range(500, 500000, 500):
        temp = asyncio.run(gca.get_pages(_links[max(0, i - 500): min(i, len(_links))], _timeout))
        _responses.extend(temp)

        if i >= len(_links):
            break

    update_status("Finding addresses...")
    return _responses


def finish():
    global scraping, scraping_aux, scraping_failed, responses, index

    if scraping_failed:
        update_status("Trying failed links...")
        time.sleep(3)

        index = 0
        scraping_failed = False

        global failed_links
        responses = get_responses(failed_links, timeout)

        update_status("Finding addresses...")
        return

    if scraping_aux:
        update_status("Trying auxiliary links...")
        time.sleep(3)

        index = 0
        scraping_aux = False

        global aux_links
        responses = get_responses(aux_links, timeout)

        update_status("Finding addresses...")
        return

    scraping = False

    update_status("Creating output file...")
    cof.create_output_file(output_type, found_addresses)

    update_status("Program finished. Closing in 3 seconds.")

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
    elif not result.found_adr and result.aux_links and scraping_aux:
        aux_links.extend(result.aux_links)
    elif result.found_adr:
        found_addresses[result.url.host] = result.address


def update_status(status):
    global __menu_ref

    __menu_ref.status_label.configure(text=status)
    __menu_ref.update_menu()
