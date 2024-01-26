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



# Create a new page in the Notion database
def create_database_item(title, url, content):
    headers = {
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NOTION_API_KEY}",
    }

    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": title}}]},
            "Link / URL": {"url": url},
            "Status":{'id': '%25%255A', 'select': {'color': 'pink', 'id': '4283667e-080f-48d7-8e97-16220f30c2d5','name': '1: New'}, 'type': 'select'},
            "Type": {'id': 'HrX%40', 'select': {'color': 'orange', 'id': 'l`<Y', 'name': 'WebClip'},  'type': 'select'}
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": content
                            }
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(f"{NOTION_URL}/pages", headers=headers, json=data)
    pprint(response.json())

# Insert elements into the Notion database
#create_database_item("First Item", "http://google.com")
#create_database_item("Second Item", "http://google.com")