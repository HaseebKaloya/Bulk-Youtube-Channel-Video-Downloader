"""
YouTube Channel Bulk Video Downloader
A powerful tool to download all videos from any YouTube channel with flexible audio format options
"""

__version__ = "1.1.0"
__author__ = "Haseeb Kaloya"
__email__ = "haseebkaloya@gmail.com"
__license__ = "MIT"

from .downloader import YouTubeChannelDownloader, DownloadProgress
from . import config, utils

__all__ = ['YouTubeChannelDownloader', 'DownloadProgress', 'config', 'utils']
