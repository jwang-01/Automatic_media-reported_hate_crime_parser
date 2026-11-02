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

    gdelt_data = news_query(day_1)

    text_parsed = text_parser(gdelt_data)

    total_articles[day_1] = news_analyzer(text_parsed)

    with open("final_analysis.json", "w") as f:
        json.dump(total_articles, f, indent=2)

    time.sleep(24*3600)