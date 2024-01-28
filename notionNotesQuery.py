import os
import requests
from pprint import pprint

import configparser

config = configparser.ConfigParser()
config.read('config.properties')

# Set up Notion API keys and database ID
NOTION_API_KEY = config['notion']['api_key'] 
NOTION_DATABASE_ID = config['notion']['db_id'] 
NOTION_URL = config['notion']['url'] 

# Get data from the Notion database
# Use this to see how some fields structures should be sent. 
def get_database_data():
    headers = {
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NOTION_API_KEY}",
    }

    response = requests.post(
        f"{NOTION_URL}/databases/{NOTION_DATABASE_ID}/query", headers=headers
    )

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.content)
        return

    results = response.json()["results"]
    print ("result: ", results)

    for result in results:
        pprint(result["properties"]["Name"]["title"][0]["text"]["content"])
        pprint(result["properties"]["Link / URL"]["url"])
        pprint(result["properties"]["Type"])
        pprint(result["properties"]["Status"])


# Retrieve data from the Notion database
get_database_data()