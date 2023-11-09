import re

import geopy
from bs4 import BeautifulSoup
import requests
from geopy import Nominatim

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

zipcode_regex_pattern = re.compile(r", [a-zA-Z]{2} \d{4,6}(?:\s|$)")
street_regex_pattern = re.compile(
    r"(?i)(\d{2,7}\b)\s+(.{2,30}\b)\s+((?:road|rd|way|street|st|str|avenue|ave|boulevard|blvd|lane|ln|drive|dr|terrace|ter|place|pl|court|ct)(?:\.)?)")
number_regex_pattern = re.compile(r"\d+")
rnumber_regex_pattern = re.compile(r"\d+")
pobox_regex_pattern = re.compile(r"(?i)(?:po|p.o.)+ +(?:box)")

geopy.geocoders.options.default_user_agent = "Company-Location-Finder"
geolocator = Nominatim()


class CompanyAddress:
    def __init__(self):
        self.country = ''
        self.state = ''
        self.region = ''
        self.city = ''
        self.postcode = ''
        self.road = ''
        self.road_numbers = ''


def create_final_address(adr_by_street, adr_by_zipcode, street, zipcode):
    if not adr_by_street and not adr_by_zipcode:
        return None

    if adr_by_street:
        adr_by_street = adr_by_street.raw['address']
    if adr_by_zipcode:
        adr_by_zipcode = adr_by_zipcode.raw['address']

    final_address = CompanyAddress()

    final_address.country = choose_field(adr_by_street, adr_by_zipcode, 'country', False)
    if final_address.country == 'United States':
        final_address.state = choose_field(adr_by_street, adr_by_zipcode, 'state', False)

    final_address.region = choose_field(adr_by_street, adr_by_zipcode, 'county', False)
    final_address.city = choose_field(adr_by_street, adr_by_zipcode, 'city', False)

    if zipcode:
        final_address.postcode = re.search(number_regex_pattern, zipcode[len(zipcode) - 7:]).group(0)
    else:
        final_address.postcode = choose_field(adr_by_street, adr_by_zipcode, 'postcode', False)

    if street:
        final_address.road = re.sub(number_regex_pattern, '', street)
        final_address.road_numbers = re.search(number_regex_pattern, street).group(0)
    else:
        final_address.road = choose_field(adr_by_street, adr_by_zipcode, 'road', True)

    return final_address


def choose_field(dict1, dict2, field, prio_first):
    field1, field2 = None, None
    if dict1 and field in dict1:
        field1 = dict1[field]
    if dict2 and field in dict2:
        field2 = dict2[field]

    if field1 and field2:
        if prio_first:
            return field1
        else:
            return field2

    if not field1:
        return field2

    return field1


def start():
    pass


def scrape_page(page):
    try:
        status_code = page.status_code
        if status_code != 200:
            print(f"Page doesn't have status code 200! {page.request.url}")
            return None
    except:
        print(f"Couldn't get response fields? {page.request.url}")
        return None

    url = page.url

    soup = BeautifulSoup(page.text, 'lxml')

    final_street = [val for val in soup.find_all(string=street_regex_pattern) if len(val) <= 100]
    if final_street:
        final_street = re.search(street_regex_pattern, final_street[0].text).group(0)
        final_street = re.sub(pobox_regex_pattern, '', final_street)

    final_zipcode = [val for val in soup.find_all(string=zipcode_regex_pattern) if len(val) <= 100]
    if final_zipcode:
        final_zipcode = re.search(zipcode_regex_pattern, final_zipcode[0].text).string.strip()
        final_zipcode = re.sub(pobox_regex_pattern, '', final_zipcode)

    global geolocator

    adr_by_street, adr_by_zipcode = None, None
    if final_street:
        adr_by_street = geolocator.geocode(final_street, addressdetails=True)
    if final_zipcode:
        adr_by_zipcode = geolocator.geocode(final_zipcode, addressdetails=True)

    final_address = create_final_address(adr_by_street, adr_by_zipcode, final_street, final_zipcode)

    if final_address is None:
        print(f"Didn't get address for this page... {url}")
        return None

    return final_address
