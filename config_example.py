"""
Advanced Configuration Examples
Copy settings from here to config.py to customize your downloads
"""

# ============================================
# DOWNLOAD PERFORMANCE SETTINGS
# ============================================

# Number of videos to download simultaneously
# Lower = more stable, Higher = faster (but uses more bandwidth/CPU)
CONCURRENT_DOWNLOADS = 3  # Default: 3, Range: 1-10

# Maximum retry attempts for failed downloads
MAX_RETRIES = 5  # Default: 5

# Delay between retries (in seconds)
# Increases exponentially: 3s, 6s, 12s, 24s, 48s
RETRY_DELAY = 3  # Default: 3

# Download timeout (in seconds)
DOWNLOAD_TIMEOUT = 600  # Default: 600 (10 minutes)


# ============================================
# VIDEO QUALITY SETTINGS
# ============================================

# Video format preference
# Options:
# - "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" (default - best quality MP4)
# - "bestvideo+bestaudio/best" (best quality, any format)
# - "worst" (smallest size)
# For specific resolution:
# - "bestvideo[height<=1080]+bestaudio/best[height<=1080]" (max 1080p)
# - "bestvideo[height<=720]+bestaudio/best[height<=720]" (max 720p)
VIDEO_FORMAT = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

# Video quality preference (simplified)
VIDEO_QUALITY = "best"  # Options: best, 1080p, 720p, 480p


# ============================================
# AUDIO SETTINGS
# ============================================

# Audio extraction format
AUDIO_FORMAT = "bestaudio/best"

# Output audio format after conversion
OUTPUT_AUDIO_FORMAT = "wav"  # Options: wav, mp3, m4a, flac, opus

# Audio bitrate (for compressed formats like mp3)
AUDIO_BITRATE = "320k"  # Options: 128k, 192k, 256k, 320k

# Audio sample rate in Hz
# Higher = better quality but larger file size
AUDIO_SAMPLE_RATE = 48000  # Options: 44100, 48000, 96000

# Number of audio channels
AUDIO_CHANNELS = 2  # 1 = Mono, 2 = Stereo


# ============================================
# FILE ORGANIZATION
# ============================================

# Custom output template for videos
# Available fields: title, id, upload_date, uploader, etc.
# Example: "%(upload_date)s - %(title)s.%(ext)s"
VIDEO_OUTPUT_TEMPLATE = "%(title)s.%(ext)s"

# Custom output template for audio
AUDIO_OUTPUT_TEMPLATE = "%(title)s.%(ext)s"


# ============================================
# BANDWIDTH & SIZE LIMITS
# ============================================

# Limit download speed (in KB/s)
# Set to None for unlimited
RATE_LIMIT = None  # Example: 1024 for 1MB/s

# Maximum file size to download (in MB)
# Set to None for no limit
MAX_FILESIZE = None  # Example: 500 for 500MB


# ============================================
# FILTERING OPTIONS
# ============================================

# Date range for downloads
# Format: YYYYMMDD
DATE_AFTER = None   # Example: "20230101" (only videos after Jan 1, 2023)
DATE_BEFORE = None  # Example: "20231231" (only videos before Dec 31, 2023)

# Minimum video duration (in seconds)
MIN_DURATION = None  # Example: 60 (skip videos shorter than 1 minute)

# Maximum video duration (in seconds)
MAX_DURATION = None  # Example: 3600 (skip videos longer than 1 hour)


# ============================================
# ADVANCED FEATURES
# ============================================

# Download subtitles
DOWNLOAD_SUBTITLES = False
SUBTITLE_LANGUAGES = ['en', 'en-US']  # Preferred subtitle languages

# Download thumbnail
DOWNLOAD_THUMBNAIL = False

# Download video description
DOWNLOAD_DESCRIPTION = False

# Embed metadata in files
EMBED_METADATA = True

# Embed thumbnail in audio files
EMBED_THUMBNAIL_IN_AUDIO = False


# ============================================
# NETWORK SETTINGS
# ============================================

# Socket timeout (in seconds)
SOCKET_TIMEOUT = 30

# Number of fragment retries
FRAGMENT_RETRIES = 10

# Use IPv4 or IPv6
# Options: None (auto), 4 (IPv4 only), 6 (IPv6 only)
FORCE_IPV = None

# Proxy settings
# Example: "http://127.0.0.1:8080"
PROXY = None


# ============================================
# LOGGING & DEBUG
# ============================================

# Logging level
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = "INFO"

# Enable verbose output
VERBOSE = False

# Print download statistics
PRINT_STATS = True


# ============================================
# PRESET CONFIGURATIONS
# ============================================

# Uncomment one of these preset configurations:

# PRESET: Maximum Quality (Large files)
"""
CONCURRENT_DOWNLOADS = 2
VIDEO_FORMAT = "bestvideo+bestaudio/best"
AUDIO_SAMPLE_RATE = 96000
AUDIO_BITRATE = "320k"
OUTPUT_AUDIO_FORMAT = "flac"
"""

# PRESET: Balanced (Good quality, reasonable size)
"""
CONCURRENT_DOWNLOADS = 3
VIDEO_FORMAT = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
AUDIO_SAMPLE_RATE = 48000
AUDIO_BITRATE = "256k"
OUTPUT_AUDIO_FORMAT = "wav"
"""

# PRESET: Fast Download (Lower quality, smaller files)
"""
CONCURRENT_DOWNLOADS = 5
VIDEO_FORMAT = "bestvideo[height<=720]+bestaudio/best[height<=720]"
AUDIO_SAMPLE_RATE = 44100
AUDIO_BITRATE = "192k"
OUTPUT_AUDIO_FORMAT = "mp3"
MAX_FILESIZE = 100  # 100MB max per file
"""

# PRESET: Audio Only (Podcast/Music)
"""
CONCURRENT_DOWNLOADS = 5
VIDEO_FORMAT = None  # Skip videos
AUDIO_SAMPLE_RATE = 48000
AUDIO_BITRATE = "320k"
OUTPUT_AUDIO_FORMAT = "mp3"
EMBED_THUMBNAIL_IN_AUDIO = True
EMBED_METADATA = True
"""

# PRESET: Slow Connection
"""
CONCURRENT_DOWNLOADS = 1
MAX_RETRIES = 10
RETRY_DELAY = 5
VIDEO_FORMAT = "bestvideo[height<=480]+bestaudio/best[height<=480]"
RATE_LIMIT = 512  # 512 KB/s
"""
