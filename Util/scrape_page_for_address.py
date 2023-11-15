import re

import geopy
from bs4 import BeautifulSoup
from geopy import Nominatim

# Regex pattern that finds Zipcodes
zipcode_regex_pattern = re.compile(r"(^|\s)[a-zA-Z]{2} \d{4,6}(?:\s|$)")

# Regex pattern that finds Streets
street_regex_pattern = re.compile(
    r"(?i)(^|\s)\d{2,7}\b\s+.{5,30}\b\s+(?:road|rd|way|street|st|str|avenue|ave|boulevard|blvd|lane|ln|drive|dr|terrace|ter|place|pl|court|ct)(?:\.|\s|$)")

# Regex pattern that finds Postal Offices
pobox_regex_pattern = re.compile(r"(?i)(?:po|p.o.)\s+(?:box)")

# Regex pattern that finds a number
number_regex_pattern = re.compile(r"\d+")

# Initializing geolocator
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


# This class is used for sending a response back to the main script
class ResponseObj:
    def __init__(self, _failed, _url, _found_adr=None, _aux_links=None, _address=CompanyAddress()):
        self.failed = _failed
        self.found_adr = _found_adr
        self.aux_links = _aux_links
        self.address = _address
        self.url = _url


# Initialization
def start():
    pass


def scrape_page(page):
    """
    Scrape the page for the company's address.
    :param page: request response
    :return: ResponseObj
    """

    # Try to see if the current page had a valid response
    try:
        status_code = page.status_code
        if status_code != 200:
            print(f"Page doesn't have status code 200! {page.request.url}")
            return ResponseObj(_failed=True, _url=page.request.url)
    except:
        print(f"Connect error? {page.request.url}")
        return ResponseObj(_failed=True, _url=page.request.url)

    url = page.url

    # Try to parse the page's content
    try:
        soup = BeautifulSoup(page.text, 'lxml')
    except:
        print(f"error parsing page... {url}")
        return ResponseObj(_failed=True, _url=page.request.url)

    # Search for a valid formatted street
    final_street = None
    try:
        final_street = [val for val in soup.find_all(string=street_regex_pattern) if len(val) <= 100]
        if final_street:
            final_street = re.search(street_regex_pattern, final_street[0].text).group(0)
            final_street = re.sub(pobox_regex_pattern, '', final_street)
    except:
        print(f"Error getting street from page {url}")

    # Search for a valid formatted zipcode
    final_zipcode = None
    try:
        final_zipcode = [val for val in soup.find_all(string=zipcode_regex_pattern) if len(val) <= 100]

        if final_zipcode:
            final_zipcode = re.search(zipcode_regex_pattern, final_zipcode[0].text).string.strip()
            final_zipcode = re.sub(pobox_regex_pattern, '', final_zipcode)
    except:
        print(f"Error getting zipcode from page {url}")

    # Try to get the full address from the found zipcode / street
    adr_by_street, adr_by_zipcode = None, None
    if final_street:
        adr_by_street = geocode_address(final_street)
    if final_zipcode:
        adr_by_zipcode = geocode_address(final_zipcode)

    # Create the final address and check for if it's probable that it's correct
    final_address = create_final_address(adr_by_street, adr_by_zipcode, final_street, final_zipcode)
    if final_address:
        not_null_count = len([field for field in final_address.__dict__.values() if field])
        if not_null_count <= 3:
            final_address = None

    # If no address was found try to search the address on other links from the page with the same domain
    if final_address is None:
        print(f"Didn't get address for this page... will try other links. {url}")
        aux_links = None

        try:
            aux_links = [mod_href(url, link['href']) for link in soup.find_all("a", href=True)]
            aux_links = [link for link in aux_links if link is not None]
        except:
            print(f"!! couldn't get hrefs for {url}")
            return ResponseObj(_failed=False, _url=url, _found_adr=None, _aux_links=[])

        return ResponseObj(_failed=False, _url=url, _found_adr=None, _aux_links=aux_links[:min(19, len(aux_links) - 1)])

    return ResponseObj(False, _url=url, _found_adr=True, _address=final_address)


def mod_href(url, href):
    """
    Return a modified url based on if the href has the same domain or is a redirect.
    :param url: page url
    :param href: auxiliary url
    :return: modified url
    """
    if href[0] == '/':
        return url.join(href)
    elif re.search(f"{url}.{{2,}}", href):
        return href


def geocode_address(query):
    """
    Try to get a valid address from a query.
    :param query: query as string
    :return: address | None
    """
    global geolocator

    try:
        address = geolocator.geocode(query, addressdetails=True, timeout=2)
        return address
    except:
        print(f"Query failed: {query}")
        return None


def create_final_address(adr_by_street, adr_by_zipcode, street, zipcode):
    """
    Combine the 2 addresses into one final address.
    :param adr_by_street: address found by street
    :param adr_by_zipcode: address found by zipcode
    :param street: street query used
    :param zipcode: zipcode query used
    :return: final address
    """
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
        final_address.postcode = re.findall(number_regex_pattern, zipcode)[-1]
    else:
        final_address.postcode = choose_field(adr_by_street, adr_by_zipcode, 'postcode', False)

    if street:
        final_address.road = re.sub(number_regex_pattern, '', street)
        final_address.road_numbers = re.search(number_regex_pattern, street).group(0)
    else:
        final_address.road = choose_field(adr_by_street, adr_by_zipcode, 'road', True)

    return final_address


def choose_field(dict1, dict2, field, prio_first):
    """
    Choose one of 2 fields from an address based on priority.
    :param dict1: address 1
    :param dict2: address 2
    :param field: field to choose
    :param prio_first: prioritize first if True
    :return: final field
    """
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
