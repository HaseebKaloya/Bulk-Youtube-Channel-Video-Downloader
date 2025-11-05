# Usage Examples

Comprehensive examples for using the YouTube Channel Bulk Downloader.

## Basic Usage

### 1. Download Everything (Videos + Audio)
```bash
python main.py "https://www.youtube.com/@examplechannel"
```
- Downloads all videos in MP4 format
- Downloads all audio in WAV format
- Automatically resumes if interrupted

### 2. Interactive Mode
```bash
python main.py --interactive
```
or simply double-click `run.bat`

Follow the prompts to:
- Enter channel URL
- Choose download options
- Select output directory

## Video Only Downloads

### Download only videos (skip audio)
```bash
python main.py "https://www.youtube.com/@examplechannel" --no-audio
```

### Download videos to custom directory
```bash
python main.py "https://www.youtube.com/@examplechannel" --no-audio -o "D:\Videos"
```

## Audio Only Downloads

### Download only audio in WAV format (default)
```bash
python main.py "https://www.youtube.com/@examplechannel" --no-video
```

### Download audio in MP3 format
```bash
python main.py "https://www.youtube.com/@examplechannel" --no-video --audio-format mp3
```

### Download audio in FLAC format (lossless)
```bash
python main.py "https://www.youtube.com/@examplechannel" --no-video --audio-format flac
```

### Download audio to music folder with custom format
```bash
python main.py "https://www.youtube.com/@examplechannel" --no-video --audio-format mp3 -o "D:\Music"
```

## Audio Format Selection

### Available Audio Formats

**WAV** - Lossless quality, large files
```bash
python main.py "https://www.youtube.com/@channel" --audio-format wav
```

**MP3** - Good quality, smaller files (recommended for music)
```bash
python main.py "https://www.youtube.com/@channel" --audio-format mp3
```

**FLAC** - Lossless compression, medium size
```bash
python main.py "https://www.youtube.com/@channel" --audio-format flac
```

**M4A** - AAC codec, good balance of quality and size
```bash
python main.py "https://www.youtube.com/@channel" --audio-format m4a
```

**OPUS** - Modern codec, very efficient
```bash
python main.py "https://www.youtube.com/@channel" --audio-format opus
```

## Advanced Options

### Adjust concurrent downloads
```bash
# Download 5 videos simultaneously (faster)
python main.py "https://www.youtube.com/@examplechannel" --concurrent 5

# Download 1 at a time (slower connection)
python main.py "https://www.youtube.com/@examplechannel" --concurrent 1
```

### Custom output directory
```bash
python main.py "https://www.youtube.com/@examplechannel" -o "E:\YouTube Downloads"
```

## Channel URL Formats

The tool supports all YouTube channel URL formats:

```bash
# Handle format (@username)
python main.py "https://www.youtube.com/@mkbhd"

# Channel ID format
python main.py "https://www.youtube.com/channel/UCBJycsmduvYEL83R_U4JriQ"

# Custom URL format
python main.py "https://www.youtube.com/c/LinusTechTips"

# User format (legacy)
python main.py "https://www.youtube.com/user/marquesbrownlee"
```

## Resume Interrupted Downloads

The tool **automatically resumes** interrupted downloads. Just run the same command again:

```bash
# First run (interrupted)
python main.py "https://www.youtube.com/@examplechannel"
# ... download interrupted ...

# Second run (automatically resumes)
python main.py "https://www.youtube.com/@examplechannel"
# Skips already downloaded videos and continues
```

## Real-World Scenarios

### Scenario 1: Download a Tech Channel
```bash
# Download videos and audio from a tech channel
python main.py "https://www.youtube.com/@mkbhd" -o "D:\Tech Videos"
```

### Scenario 2: Music Channel - Audio Only
```bash
# Download only audio from a music channel in MP3 format
python main.py "https://www.youtube.com/@artistchannel" --no-video --audio-format mp3 -o "D:\Music\Artist Name"
```

### Scenario 3: Educational Content
```bash
# Download educational videos with 3 concurrent downloads
python main.py "https://www.youtube.com/@crashcourse" --concurrent 3 -o "D:\Education"
```

### Scenario 4: Podcast Archive
```bash
# Download podcast episodes as audio only in MP3
python main.py "https://www.youtube.com/@podcastchannel" --no-video --audio-format mp3 -o "D:\Podcasts"
```

### Scenario 5: Slow Connection
```bash
# Download one at a time on slow connection
python main.py "https://www.youtube.com/@examplechannel" --concurrent 1
```

## Batch Processing

Create a batch script to download multiple channels:

**download_multiple.bat:**
```batch
@echo off
echo Downloading multiple channels...

python main.py "https://www.youtube.com/@channel1" -o "D:\Downloads\Channel1"
python main.py "https://www.youtube.com/@channel2" -o "D:\Downloads\Channel2"
python main.py "https://www.youtube.com/@channel3" -o "D:\Downloads\Channel3"

echo All downloads complete!
pause
```

## PowerShell Script for Multiple Channels

**download_multiple.ps1:**
```powershell
$channels = @(
    "https://www.youtube.com/@channel1",
    "https://www.youtube.com/@channel2",
    "https://www.youtube.com/@channel3"
)

foreach ($channel in $channels) {
    Write-Host "Downloading: $channel" -ForegroundColor Green
    python main.py $channel
}

Write-Host "All downloads complete!" -ForegroundColor Cyan
```

## Configuration Examples

### High Quality Downloads
Edit `config.py`:
```python
CONCURRENT_DOWNLOADS = 2
VIDEO_FORMAT = "bestvideo+bestaudio/best"
AUDIO_SAMPLE_RATE = 96000
AUDIO_BITRATE = "320k"
OUTPUT_AUDIO_FORMAT = "flac"
```

### Fast Downloads (Lower Quality)
```python
CONCURRENT_DOWNLOADS = 5
VIDEO_FORMAT = "bestvideo[height<=720]+bestaudio/best[height<=720]"
AUDIO_SAMPLE_RATE = 44100
AUDIO_BITRATE = "192k"
OUTPUT_AUDIO_FORMAT = "mp3"
```

### Bandwidth Limited
```python
CONCURRENT_DOWNLOADS = 1
MAX_RETRIES = 10
RATE_LIMIT = 512  # 512 KB/s
```

## Troubleshooting Examples

### Check if everything is installed correctly
```bash
python check_setup.py
```

### View detailed logs
```bash
# Windows
type logs\downloader.log

# PowerShell
Get-Content logs\downloader.log -Tail 50
```

### Check download progress
```bash
# View progress file
type data\download_progress.json
```

### Clear progress and start fresh
```bash
# Delete progress file to start over
del data\download_progress.json

# Then run download again
python main.py "https://www.youtube.com/@examplechannel"
```

## Tips & Tricks

### 1. Test with a small channel first
```bash
# Find a channel with only a few videos to test
python main.py "https://www.youtube.com/@smallchannel"
```

### 2. Monitor disk space
The tool downloads to `downloads/` by default. Make sure you have enough space!

### 3. Check logs if something fails
```bash
# Logs are in logs/downloader.log
# Check them if downloads fail
```

### 4. Use interactive mode for learning
```bash
python main.py --interactive
# Best for first-time users
```

### 5. Organize downloads by date
Rename output folders by date:
```bash
python main.py "https://www.youtube.com/@channel" -o "D:\Downloads\2024-01-15_ChannelName"
```

## Error Recovery

### If FFmpeg is not found:
```bash
# Install FFmpeg first
choco install ffmpeg

# Then verify
ffmpeg -version

# Then try download again
python main.py "https://www.youtube.com/@examplechannel"
```

### If download fails repeatedly:
```bash
# Check logs
type logs\downloader.log

# Try with single download
python main.py "https://www.youtube.com/@examplechannel" --concurrent 1

# Or increase retry delay in config.py
RETRY_DELAY = 10
```

### If you run out of disk space:
```bash
# Specify a different drive
python main.py "https://www.youtube.com/@examplechannel" -o "E:\Downloads"
```

## Common Workflows

### Daily Workflow: Update Channel Archive
```bash
# Run daily to get new videos from favorite channels
python main.py "https://www.youtube.com/@favorite" -o "D:\Archive\Favorite"
# Only new videos will be downloaded
```

### Weekly Workflow: Multiple Channels
```batch
# weekly_download.bat
python main.py "https://www.youtube.com/@tech1" -o "D:\Archive\Tech"
python main.py "https://www.youtube.com/@music1" --no-video -o "D:\Music"
python main.py "https://www.youtube.com/@podcast1" --no-video -o "D:\Podcasts"
```

---

## 👨‍💻 Author

**Haseeb Kaloya**  
📧 Email: haseebkaloya@gmail.com  
📱 Contact: +923294163702

Feel free to reach out with questions, suggestions, or feedback!

---

**Need more help?** Check `README.md` for detailed documentation or run `python check_setup.py` to verify your installation.
