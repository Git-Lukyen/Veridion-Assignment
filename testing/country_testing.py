import json

import pycountry
from text_unidecode import unidecode

states = json.load(open('../states_titlecase.json'))

matches = [x for x in states if x["abbreviation"] == "IL"]
print(matches)
