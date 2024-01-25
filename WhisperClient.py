from openai import OpenAI

class WhisperClient:
    def __init__(self):
        # Initialize the OpenAI client
        self.client = OpenAI()

    def transcribe_audio(self, audio_file_path, model="whisper-1"):
        # Transcribe the audio file using the specified model
        with open(audio_file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model=model, 
                file=audio_file
            )
        return transcript.text