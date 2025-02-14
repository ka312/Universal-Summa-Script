import os
from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
import yt_dlp
from pydub import AudioSegment
import math
import time
from datetime import timedelta
import ffmpeg
from dotenv import load_dotenv
from utils import validate_audio_file, clean_temp_files, create_srt_content
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

# Load environment variables
load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Ensure required directories exist
os.makedirs('src/videos', exist_ok=True)
os.makedirs('src/chunks', exist_ok=True)

# Clean any leftover temporary files on startup
clean_temp_files()
clean_temp_files('src/chunks')

def split_audio(input_file, chunk_duration_ms=300000):  # 5 minutes
    """Split audio into chunks"""
    audio = AudioSegment.from_file(input_file)
    chunks = []
    
    total_chunks = math.ceil(len(audio) / chunk_duration_ms)
    for i in range(total_chunks):
        start = i * chunk_duration_ms
        end = min((i + 1) * chunk_duration_ms, len(audio))
        chunk = audio[start:end]
        chunk_path = f"src/chunks/chunk_{i}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)
    
    return chunks

def process_chunk(chunk_info):
    """Process a single audio chunk"""
    chunk_path, time_offset, translation_mode = chunk_info
    
    try:
        with open(chunk_path, 'rb') as audio_file:
            if translation_mode:
                result = client.audio.translations.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="srt"
                )
                transcript = result
            else:
                result = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )
                
                # Adjust timestamps for this chunk
                for segment in result.segments:
                    segment.start += time_offset / 1000
                    segment.end += time_offset / 1000
                
                transcript = create_srt_content(result.segments)
            
            return transcript, time_offset
            
    except Exception as e:
        print(f"Error processing chunk {chunk_path}: {str(e)}")
        return "", time_offset
    finally:
        try:
            os.remove(chunk_path)
            print(f"Cleaned up chunk: {chunk_path}")
        except Exception as e:
            print(f"Error cleaning up chunk {chunk_path}: {str(e)}")

def process_large_audio(input_file, translation_mode=False):
    """Process large audio file and create SRT using parallel processing"""
    chunks = split_audio(input_file)
    chunk_infos = []
    time_offset = 0
    
    # Prepare chunk information for parallel processing
    for chunk_path in chunks:
        chunk_infos.append((chunk_path, time_offset, translation_mode))
        time_offset += len(AudioSegment.from_file(chunk_path))
    
    # Process chunks in parallel
    results = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_chunk, chunk_info) for chunk_info in chunk_infos]
        # Wait for all futures to complete
        concurrent.futures.wait(futures)
        # Get results while preserving order
        results = [future.result() for future in futures]
    
    # Combine results in correct order
    full_transcript = ""
    for transcript, _ in sorted(results, key=lambda x: x[1]):
        full_transcript += transcript
    
    return full_transcript

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/edu-videos')
def edu_videos():
    return render_template('edu_videos.html')

@app.route('/podcast')
def podcast():
    return render_template('podcast.html')

@app.route('/meeting')
def meeting():
    return render_template('meeting.html')

@app.route('/entertainment')
def entertainment():
    return render_template('entertainment.html')

@app.route('/supported-websites')
def supported_websites():
    return render_template('supported_websites.html')

@app.route('/process-video', methods=['POST'])
def process_video():
    url = request.form.get('url')
    translation = request.form.get('translation', 'none')
    
    try:
        # Log the translation parameter
        print(f"Translation mode: {translation}")
        
        # Download video
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'src/videos/1.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Process audio file
        audio_file = 'src/videos/1.mp3'
        
        # Process audio based on selection
        try:
            print(f"Processing audio file: {audio_file}")
            if translation == 'english':
                print("Using translations endpoint for English translation")
                srt_content = process_large_audio(audio_file, translation_mode=True)
                print("Translation successful")
                
                # Extract text content from SRT for summary
                translated_text = ""
                for line in srt_content.split('\n'):
                    if not line.strip().isdigit() and '-->' not in line and line.strip():
                        translated_text += line.strip() + ' '
                
                # Generate summary from translated text
                if request.form.get('type') == 'edu-video':
                    prompt = "Generate a structured educational summary with key concepts, examples, and takeaways from this transcript:"
                elif request.form.get('type') == 'podcast':
                    prompt = "Identify key speakers, provide a discussion breakdown, and list actionable insights from this transcript:"
                elif request.form.get('type') == 'meeting':
                    prompt = "Summarize the discussions, list action items, and document decisions made in this transcript:"
                else:
                    prompt = "Provide a general summary of this content:"

                summary_response = client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": translated_text}
                    ]
                )
                
                summary = summary_response.choices[0].message.content
            else:
                print("Using transcriptions endpoint for original language")
                srt_content = process_large_audio(audio_file, translation_mode=False)
                print("Transcription successful")
                
                # Generate summary from transcribed text
                if request.form.get('type') == 'edu-video':
                    prompt = "Generate a structured educational summary with key concepts, examples, and takeaways from this transcript:"
                elif request.form.get('type') == 'podcast':
                    prompt = "Identify key speakers, provide a discussion breakdown, and list actionable insights from this transcript:"
                elif request.form.get('type') == 'meeting':
                    prompt = "Summarize the discussions, list action items, and document decisions made in this transcript:"
                else:
                    prompt = "Provide a general summary of this content:"

                # Extract text content from SRT for summary
                transcribed_text = ""
                for line in srt_content.split('\n'):
                    if not line.strip().isdigit() and '-->' not in line and line.strip():
                        transcribed_text += line.strip() + ' '

                summary_response = client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": transcribed_text}
                    ]
                )
                
                summary = summary_response.choices[0].message.content
            
            return jsonify({
                'success': True,
                'subtitles': srt_content,
                'summary': summary
            })
                
        except Exception as e:
            print(f"Processing error: {str(e)}")
            raise Exception(f"Processing failed: {str(e)}")
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })
    finally:
        # Clean up temporary files
        try:
            if os.path.exists(audio_file):
                os.remove(audio_file)
                print(f"Cleaned up temporary file: {audio_file}")
        except Exception as e:
            print(f"Error cleaning up temporary file: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True)
