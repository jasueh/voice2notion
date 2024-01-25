
from ChatGPTClient import ChatGPTClient
from GoogleDriveClient import GoogleDriveClient
from WhisperClient import WhisperClient

class Main:
    def __init__(self, gd_credentials_file, gd_token_file, gd_folder_id, destination_folder):
        self.gd_credentials_file = gd_credentials_file
        self.gd_token_file = gd_token_file
        self.gd_folder_id = gd_folder_id
        self.destination_folder = destination_folder

        # Initialize the GoogleDriveClient
        self.gd_client = GoogleDriveClient(self.gd_credentials_file, self.gd_token_file)

    def download_voice_notes(self, destination_folder):
        # Download and process files
        while True:
            downloaded_file_path = self.gd_client.download_files_one_by_one(gd_folder_id, destination_folder)
            print(f"Processing file: {downloaded_file_path} - ")
                        
            # Break the loop if no more files to download
            if downloaded_file_path is None:
                print("No more files to process.")
                break


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
            json_summary = chatgpt_client.generate_text(system_prompt)

            # Placeholder for any post-processing or result handling
            # e.g., saving the summary to a file, printing, etc.
            print(f"Jason summary:  {json_summary} ")

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
    main_app.download_voice_notes(destination_folder)
