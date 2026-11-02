import json
import pandas as pd

def people_split(x):
    new_list = []
    new_people = x.split(';')
    for y in new_people:
        new_list.append(y.split(',',1)[0])
    return list(dict.fromkeys(new_list))

data = ['queryresults(01-23__04-23).json.json','queryresults(05-23__08-23).json','queryresults(09-23__12-23).json']

new_data = []
for x in data:
    for chunk in pd.read_json(x, chunksize=10000, lines=True, convert_dates=False):

        chunk['People_Involved'] = chunk['People_Involved'].apply(people_split)

        new_data.extend(chunk.to_dict(orient='records'))



