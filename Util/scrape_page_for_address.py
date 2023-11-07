import re

from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

zipcode_regex_pattern = re.compile(r", [a-zA-Z]{2} \d{4,6}(?:\s|$)")
street_regex_pattern = re.compile(
    r"(?i)(\d{2,7})+ +(\w{3,25})+ +((?:road|rd|way|street|st|str|avenue|ave|boulevard|blvd|lane|ln|drive|dr|terrace|ter|place|pl|court|ct)(?:\.)?(?:\s|\,|$))")


def start():
    pass


def scrape_page(page, url):
    if page is None:
        print(f"Got no response from page. URL: {url}")
        return None

    soup = BeautifulSoup(page.text, 'lxml')
    all_locations = [adr.strip() for adr in soup.find_all(string=zipcode_regex_pattern) if len(adr) <= 50]
    if not all_locations:
        all_locations = [adr.strip() for adr in soup.find_all(string=zipcode_regex_pattern) if len(adr) <= 50]

    if not all_locations:
        print(f"Found no address. URL: {url}")
        return None

    return all_locations[0]
