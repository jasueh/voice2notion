from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import io
from googleapiclient.http import MediaIoBaseDownload

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
