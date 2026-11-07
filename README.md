# Automatic_media-reported_hate_crime_parser
A daily updating hate crime (as reported by the media) dataset using newsarticle3k (gets news article text) and groq API's openai chatbot to analyze teh details within the articles.

# Set-Up

For Python code:

1. Use Python 3
2. Set up virtual environment
3. Download the requirements.txt and load up the packages

For SQL Query:
1. You must log into a google.cloud account to run the code
2. Download Google Cloud CLI into your local machine and follow the set-up instructions
3. Download the Google Cloud Code extension in VS Code
4. Run: ```gcloud auth login```
5. Run: ```gcloud auth application-default login```
6. Choose/create your project and now the project should be able to run

GROQ API Setup:
1. Log into GROQ
2. Create a project key for this project
3. Load your project key into your environment using: ``` $env:GROQ_API_KEY="API_KEY" ```

# About each file:

- GDELT_data.py: This was the initial code for parsing data from GDELT inspired by the code shown in the GDELT website examples.

- Themes: 
   - LOOKUP-GKGTHEMES.TXT: This is the original list of themes from GDELT Global Knowledge Graph (GKG)
   - themesss_new.json: These are themes that specifically contain ethnicities/race
   - theme.txt: These are themes that specifically contain words related to crimess/violence

- requirements.txt: File of required libraries/modules

- news_parser.py: This is the code for making SQL Queries
   - gdelt_data.json: This is an example of parsed GDELT data on articles related to discrimination and hate crimes from October 16th (Around the day of the Alexandros Paporakis attempted anti-Indian mass shooting)
 
- text_parser.py: This is the code that takes the URLS from gdelt_data.json and parses the article text
   - articles_extracted.json: This is an example of unique articles extracted from lines 147 to 155, inclusive, of gdelt_data.json. I chose those lines specifically because 147-155     contains mentions of the Alexandros Paporakis case.) Only unique titles are kept because the titles of the articles are made into dictionary keys and python only keeps unique keys. 

- api_reader.py: This is the code that takes the article texts, then runs them through GROQ API's openai chatbot to figure out whether or not the article was talking about a hate crime and why, the race of the perpetrator and victim, the summary of the crime, the date of the crime, and the location of the crime.

- main.py: This is the main file that takes all the news_parser.py, text_parser.py, and api_reader.py modules and combines them into one system. After iterating through the process for one day, the time module is used to force the file to wait for 24 hours before reparsing data for a new day. 
   - final_analysis.json: This is an example of the final output after the articles from articles_extracted.json is analyzed by the LLM (lines 147-155 only).
 
# Limitations

In the final_analysis file, you can see that there are repeated counts of the same event. If not addressed, this will eventually lead to an overestimate of hate crimes. We are currently working on an efficient solution to work on this issue that doesn't require another LLM or another algorithm with exponential time complexity. We have considered tagging each event with an evetn ID, but this would require the LLM to retain memory of the previous requests which our LLM cannot currently do. 

# Library Credits

Credits to: newspaper3k, GROQ API, Google Bigquery SQL
