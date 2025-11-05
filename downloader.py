"""
Core YouTube Channel Downloader with Resume Capability

This module handles the downloading of YouTube videos and audio files from entire channels.
It includes robust error handling, automatic retry logic, and progress tracking to ensure
reliable downloads even with unstable connections.
"""
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime
import yt_dlp
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

import config


class DownloadProgress:
    """Manages download progress and persistence"""
    
    def __init__(self, progress_file: Path = config.PROGRESS_FILE):
        self.progress_file = progress_file
        self.lock = Lock()
        self.data = self._load_progress()
    
    def _load_progress(self) -> Dict:
        """Load progress from file"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Failed to load progress file: {e}")
                return {}
        return {}
    
    def _save_progress(self):
        """Save progress to file"""
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Failed to save progress: {e}")
    
    def get_channel_progress(self, channel_id: str) -> Dict:
        """Get progress for a specific channel"""
        with self.lock:
            return self.data.get(channel_id, {
                'completed_videos': [],
                'failed_videos': [],
                'completed_audio': [],
                'failed_audio': [],
                'last_updated': None
            })
    
    def mark_video_completed(self, channel_id: str, video_id: str, video_type: str = 'video'):
        """Mark a video as completed"""
        with self.lock:
            if channel_id not in self.data:
                self.data[channel_id] = {
                    'completed_videos': [],
                    'failed_videos': [],
                    'completed_audio': [],
                    'failed_audio': [],
                    'last_updated': None
                }
            
            if video_type == 'video':
                if video_id not in self.data[channel_id]['completed_videos']:
                    self.data[channel_id]['completed_videos'].append(video_id)
                # Remove from failed if it was there
                if video_id in self.data[channel_id]['failed_videos']:
                    self.data[channel_id]['failed_videos'].remove(video_id)
            else:  # audio
                if video_id not in self.data[channel_id]['completed_audio']:
                    self.data[channel_id]['completed_audio'].append(video_id)
                if video_id in self.data[channel_id]['failed_audio']:
                    self.data[channel_id]['failed_audio'].remove(video_id)
            
            self.data[channel_id]['last_updated'] = datetime.now().isoformat()
            self._save_progress()
    
    def mark_video_failed(self, channel_id: str, video_id: str, video_type: str = 'video'):
        """Mark a video as failed"""
        with self.lock:
            if channel_id not in self.data:
                self.data[channel_id] = {
                    'completed_videos': [],
                    'failed_videos': [],
                    'completed_audio': [],
                    'failed_audio': [],
                    'last_updated': None
                }
            
            if video_type == 'video':
                if video_id not in self.data[channel_id]['failed_videos']:
                    self.data[channel_id]['failed_videos'].append(video_id)
            else:
                if video_id not in self.data[channel_id]['failed_audio']:
                    self.data[channel_id]['failed_audio'].append(video_id)
            
            self.data[channel_id]['last_updated'] = datetime.now().isoformat()
            self._save_progress()
    
    def is_completed(self, channel_id: str, video_id: str, video_type: str = 'video') -> bool:
        """Check if a video is already completed"""
        with self.lock:
            if channel_id not in self.data:
                return False
            if video_type == 'video':
                return video_id in self.data[channel_id]['completed_videos']
            else:
                return video_id in self.data[channel_id]['completed_audio']


class YouTubeChannelDownloader:
    """Main YouTube Channel Downloader with robust error handling"""
    
    def __init__(self, download_videos: bool = True, download_audio: bool = True, audio_format: str = 'wav'):
        self.download_videos = download_videos
        self.download_audio = download_audio
        self.audio_format = audio_format.lower()
        self.progress = DownloadProgress()
        self.logger = self._setup_logger()
        self.stats = {
            'total_videos': 0,
            'downloaded_videos': 0,
            'failed_videos': 0,
            'downloaded_audio': 0,
            'failed_audio': 0,
            'skipped': 0
        }
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger('YouTubeDownloader')
        logger.setLevel(getattr(logging, config.LOG_LEVEL))
        
        # File handler
        fh = logging.FileHandler(config.LOG_FILE, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    def get_channel_videos(self, channel_url: str) -> List[Dict]:
        """Fetch all videos from a YouTube channel"""
        self.logger.info(f"Fetching videos from channel: {channel_url}")
        
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'skip_download': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(channel_url, download=False)
                
                if 'entries' not in info:
                    self.logger.error("No videos found in channel")
                    return []
                
                videos = []
                for entry in info['entries']:
                    if entry:
                        videos.append({
                            'id': entry.get('id'),
                            'title': entry.get('title'),
                            'url': f"https://www.youtube.com/watch?v={entry.get('id')}",
                            'duration': entry.get('duration'),
                            'upload_date': entry.get('upload_date')
                        })
                
                self.logger.info(f"Found {len(videos)} videos in channel")
                return videos
                
        except Exception as e:
            self.logger.error(f"Error fetching channel videos: {e}")
            raise
    
    def _download_video_with_retry(self, video_info: Dict, channel_id: str, 
                                   output_path: Path, is_audio: bool = False) -> bool:
        """Download a single video with retry logic"""
        video_id = video_info['id']
        video_title = video_info['title']
        video_url = video_info['url']
        
        # Check if already completed
        video_type = 'audio' if is_audio else 'video'
        if self.progress.is_completed(channel_id, video_id, video_type):
            self.logger.info(f"Skipping already downloaded {video_type}: {video_title}")
            self.stats['skipped'] += 1
            return True
        
        for attempt in range(1, config.MAX_RETRIES + 1):
            try:
                self.logger.info(f"Downloading {video_type} (attempt {attempt}/{config.MAX_RETRIES}): {video_title}")
                
                if is_audio:
                    # Audio download options with format conversion
                    ydl_opts = {
                        'format': config.AUDIO_FORMAT,
                        'outtmpl': str(output_path / f'{video_title}.%(ext)s'),
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': self.audio_format,
                            'preferredquality': config.AUDIO_BITRATE,
                        }],
                        'postprocessor_args': [
                            '-ar', str(config.AUDIO_SAMPLE_RATE),
                            '-ac', str(config.AUDIO_CHANNELS),
                        ],
                        'quiet': False,
                        'no_warnings': False,
                        'socket_timeout': config.DOWNLOAD_TIMEOUT,
                        'retries': 3,
                        'fragment_retries': 3,
                        'ignoreerrors': False,
                    }
                else:
                    # Video download options
                    ydl_opts = {
                        'format': config.VIDEO_FORMAT,
                        'outtmpl': str(output_path / f'{video_title}.%(ext)s'),
                        'merge_output_format': 'mp4',
                        'quiet': False,
                        'no_warnings': False,
                        'socket_timeout': config.DOWNLOAD_TIMEOUT,
                        'retries': 3,
                        'fragment_retries': 3,
                        'ignoreerrors': False,
                    }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                
                # Mark as completed
                self.progress.mark_video_completed(channel_id, video_id, video_type)
                
                if is_audio:
                    self.stats['downloaded_audio'] += 1
                else:
                    self.stats['downloaded_videos'] += 1
                
                self.logger.info(f"Successfully downloaded {video_type}: {video_title}")
                return True
                
            except Exception as e:
                self.logger.warning(f"Attempt {attempt} failed for {video_title}: {e}")
                
                if attempt < config.MAX_RETRIES:
                    time.sleep(config.RETRY_DELAY * attempt)  # Exponential backoff
                else:
                    self.logger.error(f"Failed to download {video_type} after {config.MAX_RETRIES} attempts: {video_title}")
                    self.progress.mark_video_failed(channel_id, video_id, video_type)
                    
                    if is_audio:
                        self.stats['failed_audio'] += 1
                    else:
                        self.stats['failed_videos'] += 1
                    return False
        
        return False
    
    def download_channel(self, channel_url: str, output_dir: Optional[Path] = None):
        """Download all videos from a channel"""
        if output_dir is None:
            output_dir = config.DOWNLOADS_DIR
        
        output_dir = Path(output_dir)
        
        try:
            # Get channel ID from URL
            channel_id = self._extract_channel_id(channel_url)
            
            # Get all videos
            videos = self.get_channel_videos(channel_url)
            
            if not videos:
                self.logger.warning("No videos found to download")
                return
            
            self.stats['total_videos'] = len(videos)
            
            # Create output directories
            video_dir = output_dir / f"{channel_id}_videos"
            audio_dir = output_dir / f"{channel_id}_audio"
            
            if self.download_videos:
                video_dir.mkdir(parents=True, exist_ok=True)
            if self.download_audio:
                audio_dir.mkdir(parents=True, exist_ok=True)
            
            # Download videos
            if self.download_videos:
                self.logger.info(f"Starting video downloads for {len(videos)} videos...")
                self._download_batch(videos, channel_id, video_dir, is_audio=False)
            
            # Download audio
            if self.download_audio:
                self.logger.info(f"Starting audio downloads for {len(videos)} videos...")
                self._download_batch(videos, channel_id, audio_dir, is_audio=True)
            
            # Print summary
            self._print_summary()
            
        except Exception as e:
            self.logger.error(f"Error downloading channel: {e}")
            raise
    
    def _download_batch(self, videos: List[Dict], channel_id: str, 
                       output_path: Path, is_audio: bool = False):
        """Download a batch of videos using thread pool"""
        with ThreadPoolExecutor(max_workers=config.CONCURRENT_DOWNLOADS) as executor:
            futures = {
                executor.submit(
                    self._download_video_with_retry, 
                    video, 
                    channel_id, 
                    output_path, 
                    is_audio
                ): video for video in videos
            }
            
            for future in as_completed(futures):
                video = futures[future]
                try:
                    future.result()
                except Exception as e:
                    self.logger.error(f"Unexpected error downloading {video['title']}: {e}")
    
    def _extract_channel_id(self, channel_url: str) -> str:
        """Extract channel ID from URL"""
        # Simple extraction - you can make this more robust
        if '/channel/' in channel_url:
            return channel_url.split('/channel/')[-1].split('/')[0].split('?')[0]
        elif '/@' in channel_url:
            return channel_url.split('/@')[-1].split('/')[0].split('?')[0]
        else:
            # Use yt-dlp to get channel ID
            ydl_opts = {'quiet': True, 'extract_flat': True, 'skip_download': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(channel_url, download=False)
                return info.get('channel_id', 'unknown_channel')
    
    def _print_summary(self):
        """Print download summary"""
        self.logger.info("\n" + "="*60)
        self.logger.info("DOWNLOAD SUMMARY")
        self.logger.info("="*60)
        self.logger.info(f"Total videos found: {self.stats['total_videos']}")
        
        if self.download_videos:
            self.logger.info(f"Videos downloaded: {self.stats['downloaded_videos']}")
            self.logger.info(f"Videos failed: {self.stats['failed_videos']}")
        
        if self.download_audio:
            self.logger.info(f"Audio files downloaded: {self.stats['downloaded_audio']}")
            self.logger.info(f"Audio files failed: {self.stats['failed_audio']}")
        
        self.logger.info(f"Skipped (already downloaded): {self.stats['skipped']}")
        self.logger.info("="*60 + "\n")
