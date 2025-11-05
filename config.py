"""
Configuration settings for YouTube Channel Downloader
"""
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = BASE_DIR / "downloads"
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"

# Create directories if they don't exist
DOWNLOADS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Download settings
MAX_RETRIES = 5
RETRY_DELAY = 3  # seconds
CONCURRENT_DOWNLOADS = 3
DOWNLOAD_TIMEOUT = 600  # seconds

# File formats
VIDEO_FORMAT = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
AUDIO_FORMAT = "bestaudio/best"
OUTPUT_AUDIO_FORMAT = "wav"  # Default format, can be changed via CLI: wav, mp3, m4a, flac, opus

# Progress file
PROGRESS_FILE = DATA_DIR / "download_progress.json"
CHANNEL_CACHE_FILE = DATA_DIR / "channel_cache.json"

# Logging
LOG_FILE = LOGS_DIR / "downloader.log"
LOG_LEVEL = "INFO"

# Video quality preferences
VIDEO_QUALITY = "best"  # best, 1080p, 720p, 480p, etc.

# Audio settings for WAV conversion
AUDIO_BITRATE = "320k"
AUDIO_SAMPLE_RATE = 48000  # Hz
AUDIO_CHANNELS = 2  # Stereo
