from groq import Groq
import json
from google.cloud import bigquery
from datetime import datetime
from newspaper import Article, Config
import pandas as pd
from news_parser import news_query
from text_parser import text_parser
from api_reader import news_analyzer
import time

total_articles = {}

while True:
    day_1 = datetime.now().strftime("%Y-%m-%d")

    gdelt_data = news_query(day_1) # parsing gdelt data from current day

    text_parsed = text_parser(gdelt_data) # parsing the article texts from the GDELT URLs

    total_articles[day_1] = news_analyzer(text_parsed) # under the key of "day_1," you will find all the articles broken down with details

    with open("final_analysis.json", "w") as f:
        json.dump(total_articles, f, indent=2)

    time.sleep(24*3600) # wait till next day to run
