import json
import re

import pandas as pd
import os

# data = [['dom', 10], ['abhi', 15], ['celeste', 14]]
#
# df = pd.DataFrame(data, columns=['Name', 'Age'])
#
# df.to_parquet("dataframe.parquet")

str = 'www.google.com'
str2 = 'www.google.com/home'
res = re.search(f"{str}.{{2,}}", str2)
print(res)
