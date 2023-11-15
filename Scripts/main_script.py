import asyncio
import time

from Util import create_output_file as cof
from Util import get_pages_async as gca
from Util import scrape_page_for_address as address_fetcher
from Util.get_links_from_file import get_links

# Links from input file and responses from the links
links = []
responses = []

# Found addresses, auxiliary links and failed links
found_addresses = {}
aux_links = []
failed_links = []

output_type = 'parquet'
timeout = 100

# Current page response to scrape index
index = 0

# Check for continuing the script
scraping = False
scraping_aux = False
scraping_failed = False

# Reference to main menu for status updates
__menu_ref = None


def start(input_path, _type, _timeout, _menu_ref, _scraping_aux=True, _scraping_failed=False):
    """
    Start the main scraping script with current parameters.
    :param input_path: file path to the input file
    :param _type: output file type
    :param _timeout: request timeout
    :param _menu_ref: refernce to the main menu
    :param _scraping_aux: True: scrape auxiliary links
    :param _scraping_failed: True: retry failed requests
    :return: None
    """

    global __menu_ref
    __menu_ref = _menu_ref

    # Set current page index to 0 and start the scraping
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

    # Get request responses from links
    responses = get_responses(links, timeout)


def get_responses(_links, _timeout):
    """
    Start fetching request responses, 500 links at once, asynchronously. \n
    Also updates current menu status.
    :param _links: links to get responses from
    :param _timeout: request timeout
    :return: requests responses
    """

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
    """
    Call when the current scraping stage is finished. \n
    If other stages are pending, instead of finishing it will start the next stage
    :return: None | 1 if the entire process is finished
    """
    global scraping, scraping_aux, scraping_failed, responses, index

    # If the script should retry failed requests
    if scraping_failed:
        update_status("Trying failed links...")
        time.sleep(3)

        index = 0
        scraping_failed = False

        global failed_links
        responses = get_responses(failed_links, timeout)

        update_status("Finding addresses...")
        return

    # If the script should scrape for auxiliary links
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

    # End the script and create output files
    update_status("Creating output file...")
    cof.create_output_file(output_type, found_addresses)

    update_status("Program finished. Closing in 3 seconds.")

    return 1


def update():
    """
    Called each iteration of the menu. \n
    Scrapes the next page until the end of the response array.
    :return: None
    """

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

    # Check if an address was found, and if not do the affiliated task
    if scraping_failed and result.failed:
        failed_links.append(result.url)
    elif scraping_aux and not result.found_adr and result.aux_links:
        aux_links.extend(result.aux_links)
    elif result.found_adr:
        found_addresses[result.url.host] = result.address


def update_status(status):
    """
    Update main menu status message.
    :param status: status as string
    :return: None
    """
    global __menu_ref

    __menu_ref.status_label.configure(text=status)
    __menu_ref.update_menu()
