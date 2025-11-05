# Quick Start Guide 🚀

Get started with YouTube Channel Downloader in 3 easy steps!

## Step 1: Install (One-time setup)

### Option A: Automatic Installation (Recommended)
Simply double-click `install.bat` and follow the prompts.

### Option B: Manual Installation
```bash
pip install -r requirements.txt
```

**Important:** Make sure FFmpeg is installed!
- Windows: `choco install ffmpeg` (requires Chocolatey)
- Or download from: https://ffmpeg.org/download.html

## Step 2: Verify Installation

Run the setup checker:
```bash
python check_setup.py
```

This will verify that everything is installed correctly.

## Step 3: Start Downloading!

### Option A: Interactive Mode (Easiest)
Double-click `run.bat` or run:
```bash
python main.py --interactive
```

Then:
1. Paste your YouTube channel URL
2. Choose what to download (videos, audio, or both)
3. Select your preferred audio format (WAV, MP3, FLAC, etc.)
4. Hit Enter and let it work!

### Option B: Command Line
```bash
python main.py "https://www.youtube.com/@channelname"
```

## Common Examples

**Download everything from a channel:**
```bash
python main.py "https://www.youtube.com/@channelname"
```

**Download only audio (default WAV format):**
```bash
python main.py "https://www.youtube.com/@channelname" --no-video
```

**Download audio in MP3 format:**
```bash
python main.py "https://www.youtube.com/@channelname" --no-video --audio-format mp3
```

**Download to a specific folder:**
```bash
python main.py "https://www.youtube.com/@channelname" -o "D:\MyDownloads"
```

**Resume an interrupted download:**
Just run the same command again! The program automatically resumes.

## Where are my downloads?

By default, downloads are saved in:
```
downloads/
├── channelid_videos/  (MP4 videos)
└── channelid_audio/   (WAV audio files)
```

## Troubleshooting

**Problem:** FFmpeg not found  
**Solution:** Install FFmpeg and add it to your system PATH

**Problem:** Download fails  
**Solution:** Check `logs/downloader.log` for details

**Problem:** Slow downloads  
**Solution:** Reduce concurrent downloads in `config.py`

## Need Help?

1. Check `README.md` for detailed documentation
2. Review `logs/downloader.log` for error messages
3. Run `python check_setup.py` to verify your setup

## Pro Tips 💡

- The program automatically saves progress - if interrupted, just run again!
- Use `--concurrent 5` to download 5 videos simultaneously (faster but uses more bandwidth)
- Choose from multiple audio formats: WAV (lossless), MP3 (compressed), FLAC (lossless), M4A, or OPUS
- Audio files are converted with high quality settings (48kHz, stereo, 320k bitrate)
- Check the `data/download_progress.json` file to see what's been downloaded

## 👨‍💻 About

Developed by **Haseeb Kaloya**  
For support or feedback: haseebkaloya@gmail.com

---

**Enjoy downloading! 🎉**
