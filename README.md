# YouTube Channel Bulk Video Downloader 🎥

A powerful Python application that lets you download entire YouTube channels effortlessly. Built with reliability in mind, it automatically resumes interrupted downloads and converts audio to your preferred format.

## ✨ Features

- **Bulk Channel Downloads**: Download all videos from any YouTube channel in one go
- **Resume Capability**: Automatically resumes interrupted downloads from where it left off
- **Multiple Audio Formats**: Choose from WAV, MP3, M4A, FLAC, or OPUS formats
- **Concurrent Downloads**: Download multiple videos simultaneously for faster processing
- **Robust Error Handling**: Automatic retry with exponential backoff on failures
- **Progress Tracking**: Persistent progress tracking across sessions
- **High Quality**: Best quality video and audio downloads with configurable settings
- **Flexible Audio Conversion**: Convert audio to your preferred format (WAV, MP3, FLAC, etc.)
- **Detailed Logging**: Comprehensive logging for troubleshooting
- **Interactive Mode**: User-friendly CLI interface with guided setup
- **Smart Skip**: Automatically skips already downloaded videos to save time and bandwidth

## 📋 Requirements

- Python 3.8 or higher
- FFmpeg (for audio conversion)
- Active internet connection

## 🚀 Installation

### Step 1: Install Python
Make sure Python 3.8+ is installed on your system. Download from [python.org](https://www.python.org/downloads/)

### Step 2: Install FFmpeg

**Windows:**
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract the ZIP file
3. Add the `bin` folder to your system PATH

Or use Chocolatey:
```bash
choco install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg      # CentOS/RHEL
```

**macOS:**
```bash
brew install ffmpeg
```

### Step 3: Install Python Dependencies

Run the installation script:
```bash
# Windows
install.bat

# Or manually:
pip install -r requirements.txt
```

## 💻 Usage

### Interactive Mode (Recommended for beginners)

```bash
python main.py --interactive
```

The interactive mode will guide you through:
1. Entering the YouTube channel URL
2. Selecting download options (videos, audio, or both)
3. Choosing your preferred audio format (WAV, MP3, FLAC, etc.)
4. Choosing output directory
5. Confirming and starting the download

### Command Line Mode

**Basic usage - Download both videos and audio:**
```bash
python main.py "https://www.youtube.com/@channelname"
```

**Download only videos:**
```bash
python main.py "https://www.youtube.com/@channelname" --no-audio
```

**Download only audio (default WAV format):**
```bash
python main.py "https://www.youtube.com/@channelname" --no-video
```

**Download audio in MP3 format:**
```bash
python main.py "https://www.youtube.com/@channelname" --no-video --audio-format mp3
```

**Download audio in FLAC format (lossless):**
```bash
python main.py "https://www.youtube.com/@channelname" --no-video --audio-format flac
```

**Specify custom output directory:**
```bash
python main.py "https://www.youtube.com/@channelname" -o "D:\MyDownloads"
```

**Resume interrupted download:**
```bash
python main.py "https://www.youtube.com/@channelname" --resume
```
*Note: Resume is automatically enabled by default*

**Adjust concurrent downloads:**
```bash
python main.py "https://www.youtube.com/@channelname" --concurrent 5
```

### Accepted Channel URL Formats

- `https://www.youtube.com/@channelname`
- `https://www.youtube.com/channel/UCxxxxxxxxxx`
- `https://www.youtube.com/c/channelname`
- `https://www.youtube.com/user/username`

## 📁 Output Structure

```
downloads/
├── channelid_videos/
│   ├── Video Title 1.mp4
│   ├── Video Title 2.mp4
│   └── ...
└── channelid_audio/
    ├── Video Title 1.wav
    ├── Video Title 2.wav
    └── ...

data/
└── download_progress.json  # Progress tracking file

logs/
└── downloader.log  # Detailed logs
```

## ⚙️ Configuration

Edit `config.py` to customize settings:

```python
# Download settings
MAX_RETRIES = 5                  # Number of retry attempts
RETRY_DELAY = 3                  # Delay between retries (seconds)
CONCURRENT_DOWNLOADS = 3         # Number of simultaneous downloads
DOWNLOAD_TIMEOUT = 600           # Download timeout (seconds)

# Audio settings for WAV conversion
AUDIO_BITRATE = "320k"           # Audio quality
AUDIO_SAMPLE_RATE = 48000        # Sample rate in Hz
AUDIO_CHANNELS = 2               # 1=Mono, 2=Stereo
```

## 🔄 Resume Capability

The downloader automatically saves progress after each successful download. If the download is interrupted:

1. Simply run the same command again
2. The program will automatically skip already downloaded videos
3. Download will continue from where it left off

Progress is stored in `data/download_progress.json`

## 🛠️ Troubleshooting

### FFmpeg Not Found
**Error:** `ffmpeg not found`
**Solution:** Install FFmpeg and add it to your system PATH

### Permission Denied
**Error:** `Permission denied` when writing files
**Solution:** Run with administrator privileges or choose a different output directory

### Download Fails
**Error:** Videos fail to download
**Solution:** 
- Check your internet connection
- Verify the channel URL is correct
- Check `logs/downloader.log` for detailed error messages
- Some videos may be private or age-restricted

### Memory Issues
**Error:** High memory usage
**Solution:** Reduce `CONCURRENT_DOWNLOADS` in `config.py`

## 📊 Features Breakdown

### Persistence & Resume
- Progress is saved after each video download
- Tracks completed videos, failed videos, and skipped videos
- Separate tracking for video and audio downloads
- Automatic resume on next run

### Error Handling
- Automatic retry with exponential backoff
- Configurable retry attempts
- Fragment retry for network issues
- Detailed error logging
- Graceful handling of interrupted downloads

### Performance
- Multi-threaded concurrent downloads
- Configurable concurrency level
- Efficient progress tracking with file locking
- Smart skipping of already downloaded content

### Audio Quality
- Multiple format options: WAV (lossless), MP3, M4A, FLAC, OPUS
- Configurable bitrate (default 320k)
- Configurable sample rate (default 48kHz)
- Stereo audio support
- User choice for format selection

## 📝 Command Line Arguments

```
positional arguments:
  channel_url           YouTube channel URL

optional arguments:
  -h, --help            Show help message
  -o, --output DIR      Output directory (default: ./downloads)
  --no-video            Skip video downloads (audio only)
  --no-audio            Skip audio downloads (video only)
  --audio-format        Audio format: wav, mp3, m4a, flac, opus (default: wav)
  --resume              Resume interrupted download (enabled by default)
  --concurrent N        Number of concurrent downloads (default: 3)
  --interactive         Run in interactive mode
```

## 🔐 Privacy & Legal

- This tool is for personal use only
- Respect copyright laws and YouTube's Terms of Service
- Only download content you have permission to download
- The developers are not responsible for misuse of this tool

## 📄 License

MIT License - Feel free to use and modify as needed

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in `logs/downloader.log`
3. Ensure all dependencies are correctly installed

## 🎯 Roadmap

Future enhancements:
- [ ] GUI interface
- [ ] Playlist download support
- [ ] Custom video quality selection
- [ ] Video format conversion options
- [ ] Download scheduling
- [ ] Bandwidth limiting
- [ ] Metadata extraction

## 🙏 Acknowledgments

Built with:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [FFmpeg](https://ffmpeg.org/) - Audio/Video processing
- [colorama](https://github.com/tartley/colorama) - Colored terminal output
- [pydub](https://github.com/jiaaro/pydub) - Audio manipulation

## 👨‍💻 Author

**Haseeb Kaloya**
- 📧 Email: haseebkaloya@gmail.com
- 📱 Contact: +923294163702
- 💼 Passionate about building tools that make life easier

If you find this tool helpful, feel free to reach out with feedback or suggestions. I'm always looking to improve and add new features based on user needs.

---

**Made with ❤️ for the community**
