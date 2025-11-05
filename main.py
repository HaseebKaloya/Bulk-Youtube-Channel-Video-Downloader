"""
YouTube Channel Bulk Downloader - Main CLI Interface
"""
import argparse
import sys
from pathlib import Path
from colorama import init, Fore, Style

from downloader import YouTubeChannelDownloader
import config

# Initialize colorama for colored terminal output
init(autoreset=True)


def print_banner():
    """Print application banner"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        YouTube Channel Bulk Video Downloader v1.1           ║
║                                                              ║
║  Download entire YouTube channels with flexible audio       ║
║  format options and automatic resume capability             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def validate_url(url: str) -> bool:
    """Validate YouTube channel URL"""
    valid_patterns = [
        'youtube.com/channel/',
        'youtube.com/@',
        'youtube.com/c/',
        'youtube.com/user/',
    ]
    return any(pattern in url for pattern in valid_patterns)


def main():
    """Main entry point"""
    print_banner()
    
    parser = argparse.ArgumentParser(
        description='Download all videos from a YouTube channel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download both videos and audio
  python main.py https://www.youtube.com/@channelname
  
  # Download only videos
  python main.py https://www.youtube.com/@channelname --no-audio
  
  # Download only audio (WAV format)
  python main.py https://www.youtube.com/@channelname --no-video
  
  # Specify custom output directory
  python main.py https://www.youtube.com/@channelname -o /path/to/output
  
  # Resume interrupted download
  python main.py https://www.youtube.com/@channelname --resume
        """
    )
    
    parser.add_argument(
        'channel_url',
        nargs='?',
        help='YouTube channel URL'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help=f'Output directory (default: {config.DOWNLOADS_DIR})'
    )
    
    parser.add_argument(
        '--no-video',
        action='store_true',
        help='Skip video downloads (audio only)'
    )
    
    parser.add_argument(
        '--no-audio',
        action='store_true',
        help='Skip audio downloads (video only)'
    )
    
    parser.add_argument(
        '--resume',
        action='store_true',
        help='Resume interrupted download (automatically enabled)'
    )
    
    parser.add_argument(
        '--concurrent',
        type=int,
        default=config.CONCURRENT_DOWNLOADS,
        help=f'Number of concurrent downloads (default: {config.CONCURRENT_DOWNLOADS})'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '--audio-format',
        type=str,
        default='wav',
        choices=['wav', 'mp3', 'm4a', 'flac', 'opus'],
        help='Audio format for conversion (default: wav)'
    )
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive or not args.channel_url:
        print(f"{Fore.YELLOW}Running in interactive mode...{Style.RESET_ALL}\n")
        
        while True:
            channel_url = input(f"{Fore.GREEN}Enter YouTube channel URL (or 'quit' to exit): {Style.RESET_ALL}").strip()
            
            if channel_url.lower() in ['quit', 'exit', 'q']:
                print(f"\n{Fore.CYAN}Thank you for using YouTube Channel Downloader!{Style.RESET_ALL}")
                sys.exit(0)
            
            if not validate_url(channel_url):
                print(f"{Fore.RED}Invalid YouTube channel URL. Please try again.{Style.RESET_ALL}\n")
                continue
            
            print(f"\n{Fore.YELLOW}Download options:{Style.RESET_ALL}")
            print("1. Videos and Audio (default)")
            print("2. Videos only")
            print("3. Audio only")
            
            choice = input(f"\n{Fore.GREEN}Select option (1-3): {Style.RESET_ALL}").strip() or "1"
            
            download_videos = choice in ['1', '2']
            download_audio = choice in ['1', '3']
            
            # Ask for audio format if downloading audio
            audio_format = 'wav'
            if download_audio:
                print(f"\n{Fore.YELLOW}Audio format options:{Style.RESET_ALL}")
                print("1. WAV (High quality, large file size)")
                print("2. MP3 (Good quality, smaller size)")
                print("3. M4A (AAC, good balance)")
                print("4. FLAC (Lossless, very large)")
                print("5. OPUS (Modern codec, efficient)")
                
                format_choice = input(f"\n{Fore.GREEN}Select audio format (1-5, default: 1): {Style.RESET_ALL}").strip() or "1"
                
                format_map = {
                    '1': 'wav',
                    '2': 'mp3',
                    '3': 'm4a',
                    '4': 'flac',
                    '5': 'opus'
                }
                audio_format = format_map.get(format_choice, 'wav')
            
            output_dir = input(f"{Fore.GREEN}Output directory (press Enter for default): {Style.RESET_ALL}").strip()
            if not output_dir:
                output_dir = None
            
            # Confirm and start download
            print(f"\n{Fore.CYAN}Configuration:{Style.RESET_ALL}")
            print(f"  Channel URL: {channel_url}")
            print(f"  Download Videos: {download_videos}")
            print(f"  Download Audio: {download_audio}")
            if download_audio:
                print(f"  Audio Format: {audio_format.upper()}")
            print(f"  Output Directory: {output_dir or config.DOWNLOADS_DIR}")
            print(f"  Concurrent Downloads: {config.CONCURRENT_DOWNLOADS}")
            
            confirm = input(f"\n{Fore.GREEN}Start download? (y/n): {Style.RESET_ALL}").strip().lower()
            
            if confirm == 'y':
                try:
                    downloader = YouTubeChannelDownloader(
                        download_videos=download_videos,
                        download_audio=download_audio,
                        audio_format=audio_format
                    )
                    downloader.download_channel(channel_url, output_dir)
                    
                    print(f"\n{Fore.GREEN}✓ Download completed successfully!{Style.RESET_ALL}")
                    
                except Exception as e:
                    print(f"\n{Fore.RED}✗ Error during download: {e}{Style.RESET_ALL}")
            
            another = input(f"\n{Fore.GREEN}Download another channel? (y/n): {Style.RESET_ALL}").strip().lower()
            if another != 'y':
                print(f"\n{Fore.CYAN}Thank you for using YouTube Channel Downloader!{Style.RESET_ALL}")
                break
    
    else:
        # Command-line mode
        channel_url = args.channel_url
        
        if not validate_url(channel_url):
            print(f"{Fore.RED}Error: Invalid YouTube channel URL{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}URL must contain one of: /channel/, /@, /c/, /user/{Style.RESET_ALL}")
            sys.exit(1)
        
        download_videos = not args.no_video
        download_audio = not args.no_audio
        
        if not download_videos and not download_audio:
            print(f"{Fore.RED}Error: Cannot skip both video and audio downloads{Style.RESET_ALL}")
            sys.exit(1)
        
        # Update concurrent downloads if specified
        if args.concurrent != config.CONCURRENT_DOWNLOADS:
            config.CONCURRENT_DOWNLOADS = args.concurrent
        
        print(f"{Fore.CYAN}Starting download...{Style.RESET_ALL}")
        print(f"  Channel URL: {channel_url}")
        print(f"  Download Videos: {download_videos}")
        print(f"  Download Audio: {download_audio}")
        if download_audio:
            print(f"  Audio Format: {args.audio_format.upper()}")
        print(f"  Output Directory: {args.output or config.DOWNLOADS_DIR}")
        print(f"  Resume Enabled: Yes (automatic)")
        print()
        
        try:
            downloader = YouTubeChannelDownloader(
                download_videos=download_videos,
                download_audio=download_audio,
                audio_format=args.audio_format
            )
            downloader.download_channel(channel_url, args.output)
            
            print(f"\n{Fore.GREEN}✓ Download completed successfully!{Style.RESET_ALL}")
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Download interrupted by user.{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Progress has been saved. Run the same command to resume.{Style.RESET_ALL}")
            sys.exit(0)
            
        except Exception as e:
            print(f"\n{Fore.RED}✗ Error during download: {e}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Check {config.LOG_FILE} for detailed error logs.{Style.RESET_ALL}")
            sys.exit(1)


if __name__ == "__main__":
    main()
