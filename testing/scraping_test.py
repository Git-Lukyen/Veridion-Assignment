import re

from bs4 import BeautifulSoup
import requests

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
headers = {
    'User-Agent': user_agent
}


def scrape_page(page, url):
    some_div = []
    try:
        soup = BeautifulSoup(page.text, 'html')
        some_div = [adr.strip() for adr in soup.find_all(string=re.compile(r", [a-zA-Z]{2} \d{4,6}(?:\s|$)"))]
        if len(some_div) == 0:
            some_div = [adr.strip() for adr in soup.find_all(string=re.compile(
                "(?i)(\d{2,7})+ +(\w{3,25})+ +((?:road|rd|way|street|st|str|avenue|ave|boulevard|blvd|lane|ln|drive|dr|terrace|ter|place|pl|court|ct)(?:\.)?(?:\s|\,|$))"))
                        if len(adr) <= 50]
    except:
        print(f"something went wrong with extracting adr for page: {url}")

    if len(some_div) == 0:
        print(f"got no elements for page: {url}")
    return some_div


if __name__ == "__main__":
    print(scrape_page("https://www.wyandottewinery.com/"))
