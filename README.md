# Universal Summa Script

A powerful web application that transcribes, summarizes, and translates video and audio content using advanced AI technology.

![Landing Page](https://raw.githubusercontent.com/ka312/Universal-Summa-Script/refs/heads/main/images/logo.png)
![Landing Page](https://raw.githubusercontent.com/ka312/Universal-Summa-Script/refs/heads/main/images/website%201%20(1)_upscayl_3x_digital-art-4x.png)
![Landing Page](https://raw.githubusercontent.com/ka312/Universal-Summa-Script/refs/heads/main/images/how%20to.png)
![Landing Page](https://raw.githubusercontent.com/ka312/Universal-Summa-Script/refs/heads/main/images/sites.png)

## Pages & Features

### Landing Page
- Modern, responsive landing page with animated gradient sections
- Interactive 3D cards showcasing different features
- Quick access to all main functionalities
- Step-by-step guide on how to use the application
- Overview of key features and supported platforms

![Landing Page](https://raw.githubusercontent.com/ka312/Universal-Summa-Script/refs/heads/main/images/fetures.png)

### EDU-Videos Page
- Specialized for educational content transcription
- Supports YouTube videos, lectures, and tutorials
- Generates structured educational summaries
- Highlights key concepts and learning points
- Perfect for study materials and note-taking

![EDU Videos](placeholder_edu.jpg)

### Podcast Page
- Transcribes podcast episodes with high accuracy
- Identifies speakers and conversation segments
- Creates searchable text content from audio
- Extracts key insights and discussion points
- Supports various podcast platforms

![Podcast](placeholder_podcast.jpg)

### Meeting Page
- Converts meeting recordings into organized text
- Captures action items and key decisions
- Supports Zoom and other meeting platforms
- Perfect for meeting minutes and documentation
- Maintains conversation context and flow

![Meeting](placeholder_meeting.jpg)

### Entertainment Page
- Transcribes movies, shows, and entertainment content
- Generates high-quality subtitles
- Supports multiple languages and accents
- Perfect for content accessibility
- Maintains timing accuracy

![Entertainment](placeholder_entertainment.jpg)

### Supported Websites Page
- Lists all compatible platforms and websites
- Includes popular services like YouTube, Vimeo
- Details supported file formats and limitations
- Updated regularly with new platform support
- User-friendly interface for quick reference

![Supported Websites](placeholder_supported.jpg)

## Technical Implementation

### Frontend
- HTML5, CSS3 with modern features
- Responsive design using Bootstrap 5
- Custom animations and transitions
- Interactive UI elements
- Mobile-first approach

### Backend
- Python Flask framework
- OpenAI Whisper API integration
- Concurrent processing for faster results
- Efficient file handling and cleanup
- Robust error handling

### Key Features
- Parallel chunk processing for faster transcription
- Real-time progress updates
- Automatic file cleanup
- Support for multiple audio formats
- Intelligent text processing

### Libraries & Tools
- Flask: Web framework
- OpenAI: Whisper API for transcription
- yt-dlp: Video downloading
- pydub: Audio processing
- Bootstrap: Frontend framework
- Concurrent.futures: Parallel processing

## Project Structure
```
PROJECT/
├── app.py              # Main Flask application
├── utils.py           # Utility functions
├── static/
│   ├── css/          # Stylesheets
│   └── js/           # JavaScript files
├── templates/         # HTML templates
├── src/
│   ├── chunks/       # Temporary audio chunks
│   └── videos/       # Downloaded videos
└── requirements.txt   # Python dependencies
```

## Setup & Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   OPENAI_API_KEY=your_api_key
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Features in Detail

### Transcription
- Uses OpenAI's Whisper model
- Supports multiple languages
- High accuracy with context preservation
- Handles various accents and dialects

### Summarization
- Context-aware summary generation
- Key points extraction
- Structured output based on content type
- Maintains important details

### Translation
- Supports multiple target languages
- Preserves context during translation
- Maintains timing with original content
- Handles cultural nuances

## Performance Optimizations

- Parallel processing of audio chunks
- Efficient memory management
- Automatic cleanup of temporary files
- Optimized file handling
- Caching for better performance

## Future Enhancements

- Additional platform support
- Real-time transcription
- Advanced customization options
- Enhanced summary features
- More language support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

