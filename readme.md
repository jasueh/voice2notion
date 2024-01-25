install python dependencies: 
 pip install google-auth google-api-python-client google-auth-oauthlib google-auth-httplib2

 pip install --upgrade openai

How to create credentials.json
https://developers.google.com/drive/api/quickstart/python


Go to the Google Cloud Console.
Create a new project or select an existing one.
Navigate to the "APIs & Services" > "Dashboard" section.
Click on “Enable APIs and Services” and enable the Google Drive API for your project.
Go to "Credentials" in the sidebar.
Click “Create credentials” and choose “OAuth client ID”.
If prompted, configure the consent screen.
Select the application type (usually "Desktop app" for local scripts).
Give the OAuth client a name if required, and click “Create”.
Download the JSON file that contains your credentials.


How to get the folder ID 

Open Google Drive:

Go to Google Drive in your web browser and log in if necessary.
Navigate to the Desired Folder:

Find the folder from which you want to download files.
Get the Folder ID:

Open the folder by clicking on it.
Look at the URL in your browser's address bar. It will look something like this: https://drive.google.com/drive/u/0/folders/12345abcdef67890
The folder ID is the long string of letters and numbers after folders/. In this example, the folder ID is 12345abcdef67890.
This folder ID is what you'll use to specify which folder you want to interact with through the Google Drive API. Replace 'your_google_drive_folder_id' in your script with this actual folder ID.