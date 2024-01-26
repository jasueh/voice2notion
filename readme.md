
# voice2notion

## Introduction

This integration takes audio files from a specific Google Drive Folder and creates a transcription using OpenAI Whisper model, then sends the transcription to OpenAI Chat model to create a summary along with more information about the transcript like sentinment of the text, action items, follow-up questions, etc.\
Then uses the Notion API to insert the bookmark into Notion DB using Notion API: <https://developers.notion.com/docs/working-with-databases>

## Pre-requisites

### Google Drive

#### Get credentials.json

How to create credentials.json
<https://developers.google.com/drive/api/quickstart/python>

- Go to the Google Cloud Console.
- Create a new project or select an existing one.
- Navigate to the "APIs & Services" > "Dashboard" section.
- Click on “Enable APIs and Services” and enable the Google Drive API for your project.
- Go to "Credentials" in the sidebar.
- Click “Create credentials” and choose “OAuth client ID”.
- If prompted, configure the consent screen.
- Select the application type (usually "Desktop app" for local scripts).
- Give the OAuth client a name if required, and click “Create”.
- Download the JSON file that contains your credentials.

> **_NOTE:_**  The first run you will need to authorize the application to connect to your google drive folders

#### Get Folder ID

How to get the folder ID

Open Google Drive:

Go to Google Drive in your web browser and log in if necessary.
Navigate to the Desired Folder:

Find the folder from which you want to download files.
Get the Folder ID:

Open the folder by clicking on it.
Look at the URL in your browser's address bar. It will look something like this: <https://drive.google.com/drive/u/0/folders/12345abcdef67890>
The folder ID is the long string of letters and numbers after folders/. In this example, the folder ID is 12345abcdef67890.
This folder ID is what you'll use to specify which folder you want to interact with through the Google Drive API. Replace 'your_google_drive_folder_id' in your script with this actual folder ID.

### OpenAI API

<https://platform.openai.com/docs/overview>

#### OpenAI Speech-to-Text - Whisper

<https://platform.openai.com/docs/guides/speech-to-text>

#### OpenAI Text Generation - gpt-3.5-turbo / gpt-4

<https://platform.openai.com/docs/guides/text-generation>

### Notion

- Create a Notion Integration and add the connection to the Database <https://developers.notion.com/docs/create-a-notion-integration>
- The database as it is, should have 2 columns:
  - Name, type: title
  - Link / URL, type: URL

## Setup

install python dependencies:

```text
 pip install google-auth google-api-python-client google-auth-oauthlib google-auth-httplib2

 pip install --upgrade openai
```

Create .env file with the Open API Key to use the OpenAI library in python.\
Once you add your API key below, make sure to not share it with anyone! The API key should remain private.\
`OPENAI_API_KEY={{your_api_key}}`

## Docker image

To create the docker image you need to run:

`docker build --rm -t voice2notion-app .`
