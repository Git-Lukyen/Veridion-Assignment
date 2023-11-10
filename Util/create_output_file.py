import pandas as pd
import re

nbs_regex_pattern = re.compile(u"\xa0")


def create_output_file(output_type, results):
    if output_type == 'parquet':
        create_parquet_output(results)
    else:
        create_json_output(results)


def create_json_output(results):
    pass


def create_parquet_output(results):
    data = []

    for url in results:
        temp = [url]
        temp.extend([format_field(val) for val in
                     results[url].__dict__.values()])

        data.append(temp)

    columns = ['Link', 'Country', 'State', 'Region', 'City', 'Postcode', 'Road', 'Road Numbers']
    data_frame = pd.DataFrame(data, columns=columns)
    data_frame.to_parquet("found_addresses.snappy.parquet")


def format_field(field):
    if field is None:
        return ''
    else:
        return re.sub(nbs_regex_pattern, ' ', field)
