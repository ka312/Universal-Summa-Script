import os
from typing import Tuple

def validate_audio_file(file_path: str) -> Tuple[bool, str]:
    """
    Validates if the file exists and is in a supported format.
    Returns a tuple of (is_valid: bool, error_message: str)
    """
    if not os.path.exists(file_path):
        return False, "File not found"
    
    # List of supported audio formats by OpenAI API
    supported_formats = {
        '.mp3', '.mp4', '.mpeg', '.mpga', 
        '.m4a', '.wav', '.webm'
    }
    
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext not in supported_formats:
        return False, f"Unsupported file format. Supported formats are: {', '.join(supported_formats)}"
    
    # Check if file is empty
    if os.path.getsize(file_path) == 0:
        return False, "File is empty"
    
    # Check if file size is too large (over 1GB)
    max_size = 1024 * 1024 * 1024  # 1GB in bytes
    if os.path.getsize(file_path) > max_size:
        return False, "File size exceeds 1GB limit"
    
    return True, "File is valid"

def clean_temp_files(directory: str = 'src/videos') -> None:
    """
    Cleans up temporary files in the specified directory
    """
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Cleaned up: {file_path}")
            except Exception as e:
                print(f"Error cleaning up {file_path}: {str(e)}")
    except Exception as e:
        print(f"Error accessing directory {directory}: {str(e)}")

def format_timestamp(seconds: float) -> str:
    """
    Converts seconds to SRT timestamp format (HH:MM:SS,mmm)
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def create_srt_content(segments: list) -> str:
    """
    Creates SRT formatted content from segments
    """
    srt_content = ""
    for i, segment in enumerate(segments, 1):
        start_time = format_timestamp(segment.start)
        end_time = format_timestamp(segment.end)
        srt_content += f"{i}\n{start_time} --> {end_time}\n{segment.text}\n\n"
    return srt_content
