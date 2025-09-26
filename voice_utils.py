import openai
import os

# Load your OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes an audio file into text using OpenAI Whisper API.
    
    Args:
        file_path (str): Path to the audio file
    
    Returns:
        str: Transcribed text
    """
    try:
        with open(file_path, "rb") as audio_file:
            transcript = openai.Audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return "Sorry, I couldn't transcribe the audio."
