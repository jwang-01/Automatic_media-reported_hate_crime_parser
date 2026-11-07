
from google.cloud import bigquery
from datetime import date

def news_query(date_time1):
    client = bigquery.Client(project="yayaya-507218")

    date1 = date_time1

    query = f"""
    SELECT 
        DATE,
        g.DocumentIdentifier AS Article_URL,
        g.SourceCommonName AS Source,
        g.V2Locations AS Location,
        g.V2Persons AS People_Involved,
        g.V2Themes AS Themes_And_Context
    FROM 
        `gdelt-bq.gdeltv2.gkg_partitioned` AS g
    WHERE 
        g._PARTITIONDATE BETWEEN DATE('{date1}') AND DATE('{date1}')
        AND REGEXP_CONTAINS(g.V2Themes, r'(?i)KILL|SOC_GENERALCRIME|ARREST|ARMEDCONFLICT|UNGP_CRIME_VIOLENCE|TERROR|WOUND|RAPE|CRIME_COMMON_ROBBERY|HARASSMENT|BULLYING|TORTURE|CRM_ARSON|HATE_SPEECH|HATE')
        AND REGEXP_CONTAINS(g.V2Themes, r'(?i)DISCRIMINATION_RACE_RACIST|DISCRIMINATION_RACE|RACIST|RACE|RACISM')
        AND REGEXP_CONTAINS(g.V2Locations, r'(?i)US|United States')
        AND (TranslationInfo IS NULL OR TranslationInfo LIKE 'eng%') """


    df = client.query(query).to_dataframe()

    df.to_json("gdelt_data.json", orient="records", lines=True)

    return "gdelt_data.json"

