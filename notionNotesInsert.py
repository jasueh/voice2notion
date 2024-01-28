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


def additional_info_handler(arr, header, item_type):

    output=[]
    
    info_header = {
        'type': 'heading_2',
        'heading_2': {
            'rich_text': [
                {
                    'text': {
                        'content': header,
                    },
                },
            ],
        },
    }
    output.append(info_header)
    print (f"The array of items: {arr}")
    for item in arr:
        print(f"The item in the array being processed: {item}")
        info_item = {
            'type': item_type,
            item_type: {
                'rich_text': [
                    {
                        'text': {
                            'content': item,
                        },
                    },
                ],
            },
        }
        output.append(info_item)
    return output



# Create a new page in the Notion database
def create_database_item( url, transcript,content):
    headers = {
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NOTION_API_KEY}",
    }
    
    main_points=additional_info_handler(content['main_points'], "Main Points", "bulleted_list_item"),
    print("Main Points section")
    print(main_points)
    print("====================================================================")

    
    action_items=additional_info_handler(content['action_items'], "Action Items", "to_do"),
    print("Action Items section")
    print(action_items)
    print("====================================================================")
    
    
    follow_up=additional_info_handler(content['follow_up'], "Follow Up questions", "bulleted_list_item"),
    print("Follow Up section")
    print(follow_up)
    print("====================================================================")
    
    combined_items = main_points + action_items + follow_up
    combined_items_flat = [item for sublist in combined_items for item in sublist]
    
    print("Combined Items")
    print(combined_items)
    print("====================================================================")
    
    
        
    print("Summary")
    print(content['summary'])
    print("====================================================================")
    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        'icon': {
            'type': 'emoji',
            'emoji': '🎙️',
        },
        "properties": {
            "Name": {"title": [{"text": {"content": content['title']}}]},
            "Link / URL": {"url": url},
            "Status":{'id': '%25%255A', 'select': {'color': 'pink', 'id': '4283667e-080f-48d7-8e97-16220f30c2d5','name': '1: New'}, 'type': 'select'},
            "Type": {'id': 'HrX%40', 'select': {'color': 'green', 'id': '29f6918a-1a49-42ea-b7e1-655dafc33ecb', 'name': 'Voice Note'},  'type': 'select'}
        },
        'children': [
            {
                'type': 'heading_2',
                'heading_2':{
                    'rich_text': [
                        {
                            'text': {
                                'content': 'Summary:',
                            },
                        },
                    ], 
                },                 
            },
            {
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [
                        {
                            'type': 'text',
                            'text': {
                                'content': content['summary'],
                            },
                        },
                    ],
                },
            },
            {
                'type': 'heading_2',
                'heading_2':{
                    'rich_text': [
                        {
                            'text': {
                                'content': 'Transcript:',
                            },
                        },
                    ], 
                },                 
            },
            {
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [
                        {
                            'type': 'text',
                            'text': {
                                'content': transcript,
                            },
                        },
                    ],
                },
            },
            *combined_items_flat,

            {
                'type': 'heading_2',
                'heading_2':{
                    'rich_text': [
                        {
                            'text': {
                                'content': 'Sentiment:',
                            },
                        },
                    ], 
                },                 
            },
            {
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [
                        {
                            'type': 'text',
                            'text': {
                                'content': content['sentiment'],
                            },
                        },
                    ],
                },
            },

        ]
    }
    
    
    pprint(data)
    print("====================================================================")
    
    response = requests.post(f"{NOTION_URL}/pages", headers=headers, json=data)
    pprint(response.json())

# Insert elements into the Notion database
#create_database_item("First Item", "http://google.com")
#create_database_item("Second Item", "http://google.com")