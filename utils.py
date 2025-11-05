"""
Utility functions for YouTube Channel Downloader
"""
import re
import os
from pathlib import Path
from typing import Optional
import logging


def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """
    Sanitize filename to be safe for all operating systems
    
    Args:
        filename: Original filename
        max_length: Maximum length for filename
    
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
    filename = re.sub(invalid_chars, '_', filename)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > max_length:
        name, ext = os.path.splitext(filename)
        filename = name[:max_length - len(ext)] + ext
    
    # Ensure filename is not empty
    if not filename:
        filename = 'untitled'
    
    return filename


def format_bytes(bytes_size: int) -> str:
    """
    Format bytes to human-readable format
    
    Args:
        bytes_size: Size in bytes
    
    Returns:
        Formatted string (e.g., "1.5 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to HH:MM:SS
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        Formatted duration string
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def check_disk_space(path: Path, required_bytes: int = 1_073_741_824) -> bool:
    """
    Check if there's enough disk space available
    
    Args:
        path: Path to check
        required_bytes: Required space in bytes (default: 1GB)
    
    Returns:
        True if enough space available, False otherwise
    """
    try:
        import shutil
        stat = shutil.disk_usage(path)
        return stat.free >= required_bytes
    except Exception:
        return True  # Assume space is available if check fails


def setup_logging(log_file: Path, level: str = "INFO") -> logging.Logger:
    """
    Setup logging configuration
    
    Args:
        log_file: Path to log file
        level: Logging level
    
    Returns:
        Configured logger
    """
    logger = logging.getLogger('YouTubeDownloader')
    logger.setLevel(getattr(logging, level))
    
    # Create log directory if it doesn't exist
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # File handler
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger


def validate_youtube_url(url: str) -> bool:
    """
    Validate if URL is a valid YouTube URL
    
    Args:
        url: URL to validate
    
    Returns:
        True if valid YouTube URL, False otherwise
    """
    youtube_patterns = [
        r'youtube\.com/channel/',
        r'youtube\.com/@',
        r'youtube\.com/c/',
        r'youtube\.com/user/',
        r'youtu\.be/'
    ]
    
    return any(re.search(pattern, url) for pattern in youtube_patterns)


def get_channel_name_from_url(url: str) -> str:
    """
    Extract channel name from URL
    
    Args:
        url: YouTube channel URL
    
    Returns:
        Channel name or identifier
    """
    # Try to extract channel name
    if '/@' in url:
        match = re.search(r'/@([^/\?]+)', url)
        if match:
            return match.group(1)
    elif '/channel/' in url:
        match = re.search(r'/channel/([^/\?]+)', url)
        if match:
            return match.group(1)
    elif '/c/' in url:
        match = re.search(r'/c/([^/\?]+)', url)
        if match:
            return match.group(1)
    elif '/user/' in url:
        match = re.search(r'/user/([^/\?]+)', url)
        if match:
            return match.group(1)
    
    return 'unknown_channel'


def create_progress_bar(current: int, total: int, width: int = 50) -> str:
    """
    Create a text-based progress bar
    
    Args:
        current: Current progress
        total: Total items
        width: Width of progress bar
    
    Returns:
        Progress bar string
    """
    if total == 0:
        percentage = 0
    else:
        percentage = (current / total) * 100
    
    filled = int(width * current / total) if total > 0 else 0
    bar = '█' * filled + '░' * (width - filled)
    
    return f'[{bar}] {percentage:.1f}% ({current}/{total})'


def estimate_total_size(video_count: int, avg_video_size_mb: int = 50, 
                       avg_audio_size_mb: int = 5) -> str:
    """
    Estimate total download size
    
    Args:
        video_count: Number of videos
        avg_video_size_mb: Average video size in MB
        avg_audio_size_mb: Average audio size in MB
    
    Returns:
        Formatted estimated size
    """
    total_mb = (avg_video_size_mb + avg_audio_size_mb) * video_count
    total_bytes = total_mb * 1024 * 1024
    return format_bytes(total_bytes)


def check_ffmpeg_installed() -> bool:
    """
    Check if FFmpeg is installed and available
    
    Returns:
        True if FFmpeg is available, False otherwise
    """
    try:
        import subprocess
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def print_system_info():
    """Print system information for debugging"""
    import platform
    import sys
    
    info = f"""
System Information:
------------------
OS: {platform.system()} {platform.release()}
Python Version: {sys.version}
Platform: {platform.platform()}
Architecture: {platform.machine()}
    """
    print(info)
