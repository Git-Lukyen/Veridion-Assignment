import pandas as pd


def get_links(path):
    file = pd.read_parquet(path)

    links = ["https://www." + link[0] for link in file.values]
    return links
