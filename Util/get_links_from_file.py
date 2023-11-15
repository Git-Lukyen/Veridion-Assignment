import pandas as pd


def get_links(path):
    """
    Fetch links from specified .parquet file.
    :param path: file path
    :return:
    """

    file = pd.read_parquet(path)

    links = ["http://" + link[0] for link in file.values]
    return links
