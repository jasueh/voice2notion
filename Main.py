
from GoogleDriveClient import GoogleDriveClient


class Main:
    def __init__(self, gd_credentials_file, gd_token_file, gd_folder_id, destination_folder):
        self.gd_credentials_file = gd_credentials_file
        self.gd_token_file = gd_token_file
        self.gd_folder_id = gd_folder_id
        self.destination_folder = destination_folder

        # Initialize the GoogleDriveClient
        self.gd_client = GoogleDriveClient(self.gd_credentials_file, self.gd_token_file)

    def download_voice_notes(self):
        # Download new audio files from the specified Google Drive folder
        self.gd_client.download_new_audio_files(self.gd_folder_id, self.destination_folder)

# Example usage
if __name__ == "__main__":
    # Path to your 'credentials.json' file
    gd_credentials_file = 'credentials/credentials.json'
    # Path to the 'token.json' file (this will be created automatically)
    gd_token_file = 'credentials/token.json'
    # Google Drive folder ID from which to download audio files
    gd_folder_id = '1hwC1supWB3LszQZDTHw9xZ74lehLXC_v'
    # Local destination folder for downloading files
    destination_folder = 'downloads'

    main_app = Main(gd_credentials_file, gd_token_file, gd_folder_id, destination_folder)
    main_app.download_voice_notes()


