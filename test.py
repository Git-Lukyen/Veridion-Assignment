import json

import pandas as pd

file = pd.read_parquet("Output_Files/addresses.parquet")

json_results = []
for entry in file.values:    

    obj = {
        "link": entry[0],
        "country": entry[1],
        "state": entry[2],
        "region": entry[3],
        "city": entry[4],
        "postcode": entry[5],
        "road": entry[6],
        "road_numbers": entry[7]
    }

    json_results.append(obj)

output_file = open("Output_Files/addresses.json", "w")
json.dump(json_results, output_file)
