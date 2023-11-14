import pandas as pd
import scraping_test

filename = "../Input_Files/links.snappy.parquet"
df = pd.read_parquet(filename)

for link in df.values:
    url = link[0]
    print(scraping_test.scrape_page("https://" + link[0]))
