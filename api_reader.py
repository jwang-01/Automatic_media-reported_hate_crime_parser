
from groq import Groq
import json
import pandas as pd
import time

def news_analyzer(text_parsed):
    client = Groq()

    big_list = []

    df = pd.read_json(text_parsed, lines=True) #get article text

    for s in range(len(df)):
        text = df.at[s, "Text"]
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "from article, Determine if its a hate crime (criminal offense motivated by racial bias), why yes/no, race of victim and perpetrator, then summary, location, and date of hate crime. If no info available for 1 of previous sections, report none for that section only. If not hate crime, report none for all."},
                {
                "role": "user",
                "content": f"{text}"
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "Article_Analysis",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "Hate Crime?" : {"type":"boolean"},
                        "Reasoning" : {"type":"string"},
                        "Race (Victim)": {"type": "string"},
                        "Race (Perpetrator)": {"type": "string"},
                        "Summary of Crime": {
                            "type": "string"
                        },
                        "Location of Crime": {
                            "type": "string"
                        },
                        "Date of Crime": {"type": "string"}
                    },
                    "required": ["Hate Crime?", "Reasoning", "Race (Victim)", "Race (Perpetrator)", "Summary of Crime", "Date of Crime", "Location of Crime"],
                    "additionalProperties": False
                }
            }
        }
    )
        result = json.loads(completion.choices[0].message.content or "{}")
        print(json.dumps(result, indent=2))
        big_list.append(result)
        time.sleep(30)
    return big_list



