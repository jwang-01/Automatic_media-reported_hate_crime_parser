import pandas as pd
import json, ijson
import re
from pathlib import Path
from collections import Counter as Count

chunk_size = 10000

def people_split(x):
    new_list = [y.split(',',1)[0] for y in x.split(';') if y.strip()]
    return list(dict.fromkeys(new_list))

themes = ["AFRICAN AMERICAN","ASIAN","HISPANIC","BLACK","WHITE","JEWISH","AMERICAN","KILL",

"ARMEDCONFLICT",

"SOC_GENERALCRIME",

"UNGP_CRIME_VIOLENCE",

"TERROR",

"WOUND",

"RAPE",

"CRIME_COMMON_ROBBERY",

"HARASSMENT",

"BULLYING",

"TORTURE",

"CRM_ARSON",

"HATE_SPEECH"
]

def ethnicity_split(x):
    out = []
    for a in x.split(';'):
            tokens = a.split(',', 1)[0].split('_')
            for rec in themes:
                if rec in tokens:
                    out.append(rec)
                    break
    return list(dict.fromkeys(out))

location = ["United States"]

def location_split(x):
    b = x.split(';')
    new_list = [a.split('#')[1] for a in b if any(rec in a for rec in location)]
    return list(dict.fromkeys(new_list))

FILE = Path("cleaned_data.json")

raw = FILE.read_bytes()

raw = re.sub(rb"\bNaN\b",       b"null", raw)
raw = re.sub(rb"\b-Infinity\b", b"null", raw)
raw = re.sub(rb"\bInfinity\b",  b"null", raw)

# 2) Wrap as an array if the outer brackets are missing
stripped = raw.strip()
if not stripped.startswith(b"["):
    stripped = stripped.rstrip().rstrip(b",")   # drop trailing comma
    raw = b"[" + stripped + b"]"
else:
    raw = stripped

FILE.write_bytes(raw)
print("repaired ->", FILE, FILE.stat().st_size, "bytes")

new_data = []

open_data = []

with open(FILE, "rb") as f:
    for obj in ijson.items(f, "item"):
        new_data.append(obj)
        if len(new_data) >= chunk_size:
            chunk = pd.DataFrame(new_data)
            chunk["People_Involved"] = chunk["People_Involved"].fillna("").astype(str).apply(people_split)
            chunk['Themes_And_Context'] = chunk['Themes_And_Context'].fillna("").astype(str).apply(ethnicity_split) 
            chunk['Location'] = chunk["Location"].fillna("").astype(str).apply(location_split)
            # process / write chunk here
            open_data.extend(chunk.to_dict(orient="records"))
            print(f"chunk: {len(chunk)} rows")
            new_data.clear()

if new_data:
    chunk = pd.DataFrame(new_data)
    chunk["People_Involved"] = chunk["People_Involved"].fillna("").astype(str).apply(people_split)
    chunk['Themes_And_Context'] = chunk['Themes_And_Context'].fillna("").astype(str).apply(ethnicity_split)
    chunk['Location'] = chunk["Location"].fillna("").astype(str).apply(location_split)
    open_data.extend(chunk.to_dict(orient="records"))
    print(f"final chunk: {len(chunk)} rows")

data = pd.DataFrame(open_data)

def eliminate(x, y):
    eliminated = []
    for w in y:
        for t in x:
            if t not in y[w]:
                continue
            else:
                eliminated.append(t)
    x = [t for t in x if t not in eliminated]
    indexes = []
    for z in eliminated:
         for key in y:
            if z in y[key]:
                indexes.append(key)
    return x, list(Count(indexes).keys())

target_cities = {"Illinois", "California", "New York"}

big_list = {}
for row, rec in data.iterrows():
    print("Pairing Rows...")
    for x in rec['Location']:
        if any(city in x for city in target_cities):
            break
        else:
            print('Nothing in row.')
            continue
            
    listsss = [a for a in rec['People_Involved']]
    remaining, indexes = eliminate(listsss, big_list)
    if remaining:
        big_list[str(row)] = remaining
        big_list[str(row)].append(rec['Article_URL'])
        big_list[str(row)].append(rec['Themes_And_Context']) 
        big_list[str(row)].append(rec['Location'])
    if indexes:
        for key in indexes:
            big_list[str(key)].append(rec["Article_URL"])
            for z in rec['Themes_And_Context']:
                if z in big_list[str(key)]:
                    big_list[str(key)].append(z)
            for z in rec['Location']:
                if z in big_list[str(key)]:
                    big_list[str(key)].append(z)
    print(f"{remaining} + {rec['Article_URL']}")

    print("Row" + str(row) + "processed.")

print(pd.DataFrame(open_data).iloc[1])

with open("final_data.json","w") as f:
    json.dump(open_data, f, indent=4)

with open("big_data.json","w") as f:
    json.dump(big_list, f, indent=4)
