import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_translation():
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Test both transcription and translation on the same file
    test_file = 'src/videos/1.mp3'  # Make sure this file exists
    
    if not os.path.exists(test_file):
        print(f"Error: Test file {test_file} not found")
        return
    
    try:
        # Test transcription
        print("\nTesting transcription...")
        with open(test_file, 'rb') as f:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="verbose_json",
                timestamp_granularities=["segment"]
            )
        print("Transcription successful")
        print(f"Transcribed text: {transcription.text[:200]}...")
        
        # Test translation
        print("\nTesting translation...")
        with open(test_file, 'rb') as f:
            translation = client.audio.translations.create(
                model="whisper-1",
                file=f,
                response_format="srt"  # Use SRT format for translations
            )
        print("Translation successful")
        print("\nTranslated text (first 200 chars):")
        print(translation[:200] + "...")
        
        # Compare responses
        print("\nResponse formats:")
        print(f"Transcription type: {type(transcription)}")
        print(f"Translation type: {type(translation)}")
        print("\nTranscription has segments:", hasattr(transcription, 'segments'))
        print("Translation is direct SRT format")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    test_translation()
