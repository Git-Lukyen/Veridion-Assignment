import json

import pandas as pd
import re

nbs_regex_pattern = re.compile(u"\xa0")


def create_output_file(output_type, results):
    """
    Creates an output file in the current directory based on the specified file type.

    :param output_type: "json" | "parquet"
    :param results: scraped addresses
    :return: None
    """
    if output_type == 'parquet':
        create_parquet_output(results)
    else:
        create_json_output(results)


def create_json_output(results):
    json_results = []
    for key in results:
        result = results[key]

        obj = {
            "link": key,
            "country": result.country,
            "state": result.state,
            "region": result.region,
            "city": result.city,
            "postcode": result.postcode,
            "road": result.road,
            "road_numbers": result.road_numbers
        }

        json_results.append(obj)

    output_file = open("addresses.json", "w")
    json.dump(json_results, output_file)
    pass


def create_parquet_output(results):
    data = []

    # Create a dataframe with the specified columns filled with the data from results
    for url in results:
        temp = [url]
        temp.extend([format_field(val) for val in
                     results[url].__dict__.values()])

        data.append(temp)

    columns = ['Link', 'Country', 'State', 'Region', 'City', 'Postcode', 'Road', 'Road Numbers']
    data_frame = pd.DataFrame(data, columns=columns)
    data_frame.to_parquet("addresses.parquet")


def format_field(field):
    # Remove bugged non-breaking spaces
    if field is None:
        return ''
    else:
        return re.sub(nbs_regex_pattern, ' ', field)
