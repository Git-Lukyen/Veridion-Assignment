import json
import re
import time

import pandas as pd
import os

start = time.time()

a = 10000000
while a:
    a -= 1

print(f"{start - time.time()}")
