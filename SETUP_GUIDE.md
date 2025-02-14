# Universal Summa Script - Simple Setup Guide

This guide will help you set up and run the Universal Summa Script application on your computer without using a virtual environment.

## Prerequisites

1. Python 3.8 or higher installed on your computer
   - To check if Python is installed, open a terminal/command prompt and run:
     ```
     python --version
     ```

2. FFmpeg installed on your system

### Installing FFmpeg

#### Windows:
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract the downloaded file
3. Add FFmpeg to your system's PATH:
   - Copy the path to the `bin` folder (e.g., `C:\ffmpeg\bin`)
   - Open System Properties → Advanced → Environment Variables
   - Add the path to the System PATH variable
   - Restart your terminal/command prompt
   - Verify installation by running:
     ```
     ffmpeg -version
     ```

#### macOS:
```bash
brew install ffmpeg
```

#### Linux:
```bash
sudo apt update
sudo apt install ffmpeg
```

## Installation Steps

1. Download and extract the project files to your desired location

2. Open a terminal/command prompt and navigate to the project directory:
```bash
cd path/to/project/folder
```

3. Run the check_requirements.py script to install required packages:
```bash
python check_requirements.py
```

4. Create a `.env` file in the project folder:
   - Copy `.env.example` to `.env`
   - Open `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

   To get an OpenAI API key:
   1. Go to https://platform.openai.com/
   2. Sign up or log in
   3. Navigate to API keys section
   4. Create a new secret key

## Starting the Server

1. Open a terminal/command prompt

2. Navigate to the project directory:
```bash
cd path/to/project/folder
```

3. Start the Flask server:
```bash
# Windows
set FLASK_APP=app.py
python -m flask run

# macOS/Linux
export FLASK_APP=app.py
python -m flask run
```

4. Open your web browser and go to:
```
http://127.0.0.1:5000
```

## Using the Application

1. Choose one of the available sections:
   - EDU-Videos
   - Podcast
   - Meeting
   - Entertainment

2. Enter a video URL (YouTube and other platforms supported)

3. For non-English content:
   - Select "English" in the translation dropdown to get English subtitles

4. Click "Start Processing"

## Troubleshooting

### Common Issues

1. **Python not found**
   ```bash
   # Check Python installation
   python --version
   ```

2. **FFmpeg not found**
   ```bash
   # Check FFmpeg installation
   ffmpeg -version
   ```

3. **Package installation errors**
   ```bash
   # Run check_requirements.py again
   python check_requirements.py
   ```

4. **Permission errors**
   - Run terminal/command prompt as administrator
   - Check write permissions in the project folder

5. **Server won't start**
   - Make sure no other application is using port 5000
   - Try a different port:
     ```bash
     # Windows
     set FLASK_APP=app.py
     python -m flask run --port=5001

     # macOS/Linux
     export FLASK_APP=app.py
     python -m flask run --port=5001
     ```

### Error Messages

1. **"OpenAI API key not found"**
   - Check if `.env` file exists
   - Verify API key is correct
   - Make sure there are no spaces around the API key in `.env`

2. **"FFmpeg not found"**
   - Reinstall FFmpeg
   - Check PATH environment variable
   - Restart terminal/command prompt

3. **"Port already in use"**
   - Close other applications using port 5000
   - Use a different port as shown above

## Important Notes

- The application needs internet access for:
  - Downloading videos
  - Communicating with OpenAI API
- Maximum supported file size is 1GB
- Temporary files are stored in `src/videos` and `src/chunks`
- API usage may incur costs (check OpenAI pricing)
- Keep your API key secure and never share it

## Command Quick Reference

```bash
# Check Python version
python --version

# Check FFmpeg installation
ffmpeg -version

# Install requirements
python check_requirements.py

# Start server (Windows)
set FLASK_APP=app.py
python -m flask run

# Start server (macOS/Linux)
export FLASK_APP=app.py
python -m flask run

# Start on different port (if 5000 is busy)
python -m flask run --port=5001
