
from ChatGPTClient import ChatGPTClient
from GoogleDriveClient import GoogleDriveClient
from WhisperClient import WhisperClient
from datetime import datetime
import notionNotesInsert
import json

class Main:
    def __init__(self, gd_credentials_file, gd_token_file, gd_folder_id, destination_folder):
        self.gd_credentials_file = gd_credentials_file
        self.gd_token_file = gd_token_file
        self.gd_folder_id = gd_folder_id
        self.destination_folder = destination_folder

        # Initialize the GoogleDriveClient
        self.gd_client = GoogleDriveClient(self.gd_credentials_file, self.gd_token_file)

    def download_voice_notes(self):
        # Download and process files
        files_list = self.gd_client.list_files_in_folder(self.gd_folder_id)
        
        last_downloaded_timestamp = self.gd_client.get_last_downloaded_file_timestamp()



        for file_metadata in files_list:
            
            print(f"Processing file ID: {file_metadata['id']} - Name:  {file_metadata['name']}")
            print(f"Created Time: {file_metadata['createdTime']}")
            print(f"Last Downloaded Time: {last_downloaded_timestamp}")
            
            # Parse the timestamps
            created_time = datetime.fromisoformat(file_metadata['createdTime'].replace("Z", "+00:00"))
            last_downloaded_time = datetime.fromisoformat(last_downloaded_timestamp.replace("Z", "+00:00"))

            # Compare the timestamps
            if created_time > last_downloaded_time:
                print("Created Time is bigger than Last Downloaded Time")
                self.download_and_process_file(file_metadata)
            elif created_time < last_downloaded_time:
                print("Last Downloaded Time is bigger than Created Time, nothing to do here")
            else:
                print("Both times are equal, nothing to do here")


    def download_and_process_file(self, file_metadata):
        downloaded_file_path = self.gd_client.download_file_by_id(file_metadata['id'], file_metadata['name'], file_metadata['createdTime'],self.destination_folder)
        print(f"Downloaded file: {downloaded_file_path}")
        

        # Transcribe the downloaded file using WhisperClient
        whisper_client = WhisperClient()
        transcript = whisper_client.transcribe_audio(downloaded_file_path)
        print(f"Transcript:  {transcript} ")

        # Use ChatGPTClient for further processing (e.g., summarizing)
        chatgpt_client = ChatGPTClient()
        
        #summary_options = ["Summary", "Main Points", "Action Items", "Follow-up Questions", "Stories", "References", "Arguments", "Related Topics", "Sentiment"]
        summary_options = ["Summary", "Main Points", "Action Items", "Follow-up Questions", "Sentiment"]
        verbosity = "Low"
        summary_language = "en"
        system_prompt = chatgpt_client.generate_system_prompt(transcript, summary_options, verbosity, summary_language)
        json_summary_str = chatgpt_client.generate_text(system_prompt)

        # Placeholder for any post-processing or result handling
        # e.g., saving the summary to a file, printing, etc.
        print(f"Jason summary:  {json_summary_str} ")
        json_summary = json.loads(json_summary_str)
        
        
        url = f"https://drive.google.com/file/d/{file_metadata['id']}/view?usp=drivesdk"
        notionNotesInsert.create_database_item(json_summary['title'], url, json_summary_str )
        

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
