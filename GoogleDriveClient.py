from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import io
from googleapiclient.http import MediaIoBaseDownload
import json
class GoogleDriveClient:
    def __init__(self, credentials_file, token_file):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = self.authenticate_google_drive()

    def authenticate_google_drive(self):
        creds = None
        # The file token_file stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, ['https://www.googleapis.com/auth/drive.readonly'])
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())

        service = build('drive', 'v3', credentials=creds)
        return service

    def download_new_audio_files(self, folder_id, destination_folder):
        # Call the Drive v3 API
        results = self.service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                file_id = item['id']
                file_name = item['name']
                if file_name.lower().endswith(('.mp3', '.m4a')):
                    request = self.service.files().get_media(fileId=file_id)
                    file_path = os.path.join(destination_folder, file_name)
                    with open(file_path, 'wb') as fh:
                        downloader = MediaIoBaseDownload(fh, request)
                        done = False
                        while done is False:
                            status, done = downloader.next_chunk()
                            print(f"Download {file_name} {int(status.progress() * 100)}%.")
                    print(f'{file_name} downloaded to {file_path}')

    def save_last_downloaded_file_timestamp(self, file_timestamp):
        with open('last_downloaded_file.json', 'w') as f:
            json.dump({'last_file_timestamp': file_timestamp}, f)

    def get_last_downloaded_file_timestamp(self):
        try:
            with open('last_downloaded_file.json', 'r') as f:
                data = json.load(f)
                return data.get('last_file_timestamp')
        except (FileNotFoundError, json.JSONDecodeError):
            # Create the file with an empty JSON object if it doesn't exist or if it's empty
            with open('last_downloaded_file.json', 'w') as f:
                json.dump({'last_file_timestamp': '2024-01-24T19:56:38.143Z'}, f)
            return '2024-01-24T19:56:38.143Z'

    def list_files_in_folder(self, folder_id):
        query = f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder'"
        results = self.service.files().list(
            q=query,
            pageSize=100, fields="nextPageToken, files(id, name, createdTime, mimeType)").execute()
        
        items = results.get('files', [])
        if not items:
            # No more files to download, return None
            return None
        
        print(items)
        return items
    
    def download_file_by_id(self, file_id, file_name, file_time, destination_folder):

        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        self.save_last_downloaded_file_timestamp(file_time)
        file_path = os.path.join(destination_folder, file_name)
        with open(file_path, 'wb') as f:
            f.write(fh.getbuffer())
        return os.path.abspath(file_path)
