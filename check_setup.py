"""
Setup Verification Script
Checks if all dependencies and requirements are properly installed
"""
import sys
import subprocess
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)


def print_header(text):
    """Print formatted header"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{text:^60}")
    print(f"{'='*60}{Style.RESET_ALL}\n")


def check_python_version():
    """Check Python version"""
    print(f"{Fore.YELLOW}Checking Python version...{Style.RESET_ALL}")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 8:
        print(f"{Fore.GREEN}✓ Python {version.major}.{version.minor}.{version.micro} - OK{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}✗ Python {version.major}.{version.minor}.{version.micro} - Please upgrade to Python 3.8+{Style.RESET_ALL}")
        return False


def check_module(module_name, import_name=None):
    """Check if a Python module is installed"""
    if import_name is None:
        import_name = module_name
    
    try:
        __import__(import_name)
        print(f"{Fore.GREEN}✓ {module_name} - Installed{Style.RESET_ALL}")
        return True
    except ImportError:
        print(f"{Fore.RED}✗ {module_name} - Not installed{Style.RESET_ALL}")
        return False


def check_ffmpeg():
    """Check if FFmpeg is installed"""
    print(f"{Fore.YELLOW}Checking FFmpeg...{Style.RESET_ALL}")
    
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            timeout=5,
            text=True
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"{Fore.GREEN}✓ FFmpeg - Installed{Style.RESET_ALL}")
            print(f"  {version_line}")
            return True
        else:
            print(f"{Fore.RED}✗ FFmpeg - Not working properly{Style.RESET_ALL}")
            return False
            
    except FileNotFoundError:
        print(f"{Fore.RED}✗ FFmpeg - Not installed or not in PATH{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Install from: https://ffmpeg.org/download.html{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}✗ FFmpeg - Error checking: {e}{Style.RESET_ALL}")
        return False


def check_directories():
    """Check if required directories exist"""
    print(f"\n{Fore.YELLOW}Checking directories...{Style.RESET_ALL}")
    
    dirs = ['downloads', 'logs', 'data']
    all_ok = True
    
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"{Fore.GREEN}✓ {dir_name}/ - Exists{Style.RESET_ALL}")
        else:
            try:
                dir_path.mkdir(exist_ok=True)
                print(f"{Fore.GREEN}✓ {dir_name}/ - Created{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}✗ {dir_name}/ - Cannot create: {e}{Style.RESET_ALL}")
                all_ok = False
    
    return all_ok


def check_disk_space():
    """Check available disk space"""
    print(f"\n{Fore.YELLOW}Checking disk space...{Style.RESET_ALL}")
    
    try:
        import shutil
        stat = shutil.disk_usage('.')
        
        free_gb = stat.free / (1024**3)
        total_gb = stat.total / (1024**3)
        
        print(f"  Total: {total_gb:.2f} GB")
        print(f"  Free: {free_gb:.2f} GB")
        
        if free_gb < 1:
            print(f"{Fore.RED}⚠ Warning: Less than 1 GB free space{Style.RESET_ALL}")
            return False
        else:
            print(f"{Fore.GREEN}✓ Sufficient disk space{Style.RESET_ALL}")
            return True
            
    except Exception as e:
        print(f"{Fore.YELLOW}⚠ Cannot check disk space: {e}{Style.RESET_ALL}")
        return True


def check_internet():
    """Check internet connectivity"""
    print(f"\n{Fore.YELLOW}Checking internet connection...{Style.RESET_ALL}")
    
    try:
        import requests
        response = requests.get('https://www.youtube.com', timeout=5)
        
        if response.status_code == 200:
            print(f"{Fore.GREEN}✓ Internet connection - OK{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}✗ Cannot reach YouTube{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}✗ Internet connection - Failed: {e}{Style.RESET_ALL}")
        return False


def main():
    """Main verification function"""
    print_header("YouTube Channel Downloader - Setup Check")
    
    results = []
    
    # Check Python version
    results.append(("Python Version", check_python_version()))
    
    # Check required modules
    print(f"\n{Fore.YELLOW}Checking Python modules...{Style.RESET_ALL}")
    modules = [
        ('yt-dlp', 'yt_dlp'),
        ('colorama', 'colorama'),
        ('requests', 'requests'),
        ('pydub', 'pydub'),
    ]
    
    for module_name, import_name in modules:
        results.append((module_name, check_module(module_name, import_name)))
    
    # Check FFmpeg
    results.append(("FFmpeg", check_ffmpeg()))
    
    # Check directories
    results.append(("Directories", check_directories()))
    
    # Check disk space
    results.append(("Disk Space", check_disk_space()))
    
    # Check internet
    results.append(("Internet", check_internet()))
    
    # Print summary
    print_header("Summary")
    
    passed = sum(1 for _, status in results if status)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}\n")
    
    if passed == total:
        print(f"{Fore.GREEN}{'='*60}")
        print(f"{'✓ ALL CHECKS PASSED!':^60}")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}You're ready to use the YouTube Channel Downloader!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Run: python main.py --interactive{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.RED}{'='*60}")
        print(f"{'✗ SOME CHECKS FAILED':^60}")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}Please fix the issues above before using the downloader.{Style.RESET_ALL}\n")
        
        # Provide specific help
        failed_items = [name for name, status in results if not status]
        
        if 'FFmpeg' in failed_items:
            print(f"{Fore.YELLOW}To install FFmpeg:{Style.RESET_ALL}")
            print("  Windows: choco install ffmpeg")
            print("  Or download from: https://ffmpeg.org/download.html\n")
        
        if any(module in failed_items for module in ['yt-dlp', 'colorama', 'requests', 'pydub']):
            print(f"{Fore.YELLOW}To install missing Python modules:{Style.RESET_ALL}")
            print("  Run: pip install -r requirements.txt\n")


if __name__ == "__main__":
    main()
