import re


from bs4 import BeautifulSoup
import requests

url = "https://www.umbrawindowtinting.com/"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
headers = {
    'User-Agent': user_agent
}

page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.text, 'html')

some_div = soup.find_all(string=re.compile(r"(?i)\blocation\b"))
print(some_div)
