from newspaper import article, Config
import pandas as pd

def text_parser(gdelt_data):
    df = pd.read_json(gdelt_data, lines=True) #reading lines of subsectioned gdelt data 

    total = {}

    for s in range(len(df)):

        url = df.at[s, "Article_URL"]
        config = Config() #making the website think the library is a normal user
        config.browser_user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36")
        
        try:
            article_news = article.Article(url, config=config) #tests to see if the website successfully accessed the website
            article_news.download()
            article_news.parse()
            print("Printed successfully.")

        except Exception as e:
            print(f"Error occurred while accessing {url}") #if the website doesn't allow the parser through, continue
            continue

        total[article_news.title] = article_news.text #gets body of text


    new_data = pd.DataFrame(total.items(), columns=["Title", "Text"])
    print(new_data.head())

    new_data.to_json("articles_extracted.json", orient="records", lines=True) #turn into json file to use later

    return "articles_extracted.json"


text_parser("gdelt_data.json", 150, 153) #used to test if the function worked


