# Project Structure

Overview of the YouTube Channel Bulk Downloader project structure and file purposes.

## Directory Tree

```
BulkYoutubeVideoDownloader/
│
├── 📄 main.py                    # Main CLI entry point
├── 📄 downloader.py              # Core downloader logic with resume capability
├── 📄 config.py                  # Configuration settings
├── 📄 utils.py                   # Utility functions
├── 📄 __init__.py                # Package initialization
│
├── 📄 requirements.txt           # Python dependencies
│
├── 🪟 install.bat                # Windows installation script
├── 🪟 run.bat                    # Windows run script
├── 🪟 check_setup.bat            # Windows setup verification
│
├── 📄 check_setup.py             # Setup verification tool
│
├── 📖 README.md                  # Main documentation
├── 📖 QUICKSTART.md             # Quick start guide
├── 📖 EXAMPLES.md               # Usage examples
├── 📖 CHANGELOG.md              # Version history
├── 📖 PROJECT_STRUCTURE.md      # This file
│
├── 📄 config_example.py         # Advanced configuration examples
├── 📄 LICENSE                    # MIT License
├── 📄 .gitignore                # Git ignore rules
│
├── 📁 downloads/                 # Downloaded content (created at runtime)
│   ├── 📁 {channel_id}_videos/  # Video files (MP4)
│   └── 📁 {channel_id}_audio/   # Audio files (WAV)
│
├── 📁 logs/                      # Log files (created at runtime)
│   └── 📄 downloader.log        # Detailed application logs
│
└── 📁 data/                      # Application data (created at runtime)
    ├── 📄 download_progress.json # Download progress tracking
    └── 📄 channel_cache.json    # Channel information cache
```

## File Descriptions

### Core Application Files

#### `main.py`
- **Purpose**: Main entry point for the application
- **Features**: 
  - Command-line argument parsing
  - Interactive mode
  - User input validation
  - Colored console output
- **Usage**: `python main.py [options]`

#### `downloader.py`
- **Purpose**: Core downloading functionality
- **Classes**:
  - `YouTubeChannelDownloader`: Main downloader class
  - `DownloadProgress`: Progress tracking and persistence
- **Features**:
  - Video and audio downloading
  - Retry logic with exponential backoff
  - Concurrent downloads
  - Progress persistence
  - Error handling

#### `config.py`
- **Purpose**: Application configuration
- **Contains**:
  - Download settings (retries, timeout, concurrency)
  - File format preferences
  - Audio quality settings
  - Directory paths
  - Logging configuration

#### `utils.py`
- **Purpose**: Utility and helper functions
- **Functions**:
  - Filename sanitization
  - Format conversion (bytes, duration)
  - Disk space checking
  - URL validation
  - FFmpeg detection
  - System information

#### `__init__.py`
- **Purpose**: Package initialization
- **Contains**:
  - Version information
  - Package exports
  - Module imports

### Installation & Setup Files

#### `requirements.txt`
- **Purpose**: Python package dependencies
- **Packages**:
  - yt-dlp (YouTube downloading)
  - pydub (Audio processing)
  - colorama (Colored terminal output)
  - tqdm (Progress bars)
  - requests (HTTP requests)
  - ffmpeg-python (FFmpeg wrapper)

#### `install.bat`
- **Purpose**: Automated installation for Windows
- **Actions**:
  - Checks Python installation
  - Upgrades pip
  - Installs dependencies
  - Provides FFmpeg installation instructions

#### `run.bat`
- **Purpose**: Quick launcher for Windows
- **Actions**:
  - Launches application in interactive mode
  - Verifies Python installation

#### `check_setup.bat`
- **Purpose**: Windows wrapper for setup verification
- **Actions**: Runs `check_setup.py`

#### `check_setup.py`
- **Purpose**: Comprehensive setup verification
- **Checks**:
  - Python version
  - Required modules
  - FFmpeg installation
  - Directory creation
  - Disk space
  - Internet connectivity

### Documentation Files

#### `README.md`
- **Purpose**: Main documentation
- **Sections**:
  - Features overview
  - Installation instructions
  - Usage examples
  - Configuration guide
  - Troubleshooting
  - FAQ

#### `QUICKSTART.md`
- **Purpose**: Quick start guide for beginners
- **Content**:
  - 3-step setup
  - Basic examples
  - Common use cases
  - Quick troubleshooting

#### `EXAMPLES.md`
- **Purpose**: Comprehensive usage examples
- **Content**:
  - Basic usage
  - Advanced options
  - Real-world scenarios
  - Batch processing
  - Configuration examples

#### `CHANGELOG.md`
- **Purpose**: Version history and changes
- **Content**:
  - Release notes
  - Feature additions
  - Bug fixes
  - Future roadmap

#### `PROJECT_STRUCTURE.md`
- **Purpose**: Project organization guide
- **Content**:
  - File structure
  - File descriptions
  - Data flow
  - Module relationships

### Configuration Files

#### `config_example.py`
- **Purpose**: Advanced configuration examples
- **Content**:
  - Preset configurations
  - Performance tuning
  - Quality settings
  - Network options
  - Feature flags

#### `.gitignore`
- **Purpose**: Git ignore rules
- **Excludes**:
  - Python cache files
  - Virtual environments
  - Downloaded content
  - Log files
  - Temporary files

#### `LICENSE`
- **Purpose**: MIT License
- **Content**:
  - Usage terms
  - Liability disclaimer
  - Copyright information

### Runtime Directories

#### `downloads/`
- **Purpose**: Downloaded content storage
- **Created**: Automatically at first run
- **Structure**:
  - `{channel_id}_videos/`: Video files in MP4 format
  - `{channel_id}_audio/`: Audio files in WAV format

#### `logs/`
- **Purpose**: Application logs
- **Created**: Automatically at first run
- **Files**:
  - `downloader.log`: Detailed application logs with timestamps

#### `data/`
- **Purpose**: Application data and cache
- **Created**: Automatically at first run
- **Files**:
  - `download_progress.json`: Download progress tracking
  - `channel_cache.json`: Channel information cache

## Data Flow

```
User Input (Channel URL)
        ↓
    main.py (CLI Interface)
        ↓
    downloader.py (Core Logic)
        ↓
    yt-dlp (Download)
        ↓
    FFmpeg (Convert to WAV)
        ↓
    downloads/ (Save Files)
        ↓
    data/download_progress.json (Track Progress)
```

## Module Relationships

```
main.py
  ├─→ downloader.py
  │     ├─→ config.py
  │     ├─→ utils.py
  │     └─→ yt_dlp (external)
  │
  ├─→ config.py
  └─→ utils.py

check_setup.py
  ├─→ config.py
  └─→ utils.py
```

## Key Features by File

### Resume Capability
- **File**: `downloader.py`
- **Class**: `DownloadProgress`
- **Storage**: `data/download_progress.json`

### Error Handling
- **File**: `downloader.py`
- **Method**: `_download_video_with_retry()`
- **Features**: Exponential backoff, retry counter, error logging

### Concurrent Downloads
- **File**: `downloader.py`
- **Method**: `_download_batch()`
- **Config**: `config.CONCURRENT_DOWNLOADS`

### Audio Conversion
- **File**: `downloader.py`
- **Tool**: FFmpeg
- **Formats**: WAV, MP3, M4A, FLAC, OPUS (user-selectable)
- **Selection**: Interactive mode or `--audio-format` CLI argument

### Progress Tracking
- **File**: `downloader.py`
- **Class**: `DownloadProgress`
- **Persistence**: JSON file with file locking

## Configuration Hierarchy

1. **Default Config**: `config.py`
2. **User Customization**: Edit `config.py` directly
3. **Examples**: See `config_example.py` for presets
4. **Runtime Override**: Command-line arguments in `main.py`

## Logging System

```
Application Event
      ↓
logging.Logger
      ↓
  ┌───┴───┐
  │       │
File    Console
  │       │
  ↓       ↓
.log    stdout
```

**Log Levels**:
- DEBUG: Detailed debugging information
- INFO: General informational messages
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical errors

## Extension Points

Want to extend the application? Here are the key extension points:

1. **Custom Downloaders**: Extend `YouTubeChannelDownloader` class
2. **New Formats**: Modify `config.py` and `downloader.py`
3. **Progress Tracking**: Extend `DownloadProgress` class
4. **UI Changes**: Modify `main.py` for CLI or create new GUI
5. **Post-Processing**: Add hooks in `_download_video_with_retry()`

## Best Practices

### For Users
1. Start with `QUICKSTART.md`
2. Run `check_setup.py` before first use
3. Check `EXAMPLES.md` for common scenarios
4. Review `logs/downloader.log` if issues occur

### For Developers
1. Follow the existing code structure
2. Update documentation when adding features
3. Add logging for new functionality
4. Maintain backward compatibility
5. Update `CHANGELOG.md` for changes

## Support Files Priority

1. **First Time Users**: `QUICKSTART.md`
2. **General Usage**: `README.md`
3. **Specific Examples**: `EXAMPLES.md`
4. **Troubleshooting**: `logs/downloader.log` + `README.md`
5. **Advanced Config**: `config_example.py`
6. **Development**: `PROJECT_STRUCTURE.md` (this file)

---

## 👨‍💻 Author

**Haseeb Kaloya**  
Developer & Maintainer

📧 Email: haseebkaloya@gmail.com  
📱 Contact: +923294163702

This project was built with the goal of making YouTube channel archiving simple and reliable. If you have suggestions for improvements or run into any issues, feel free to reach out!

---

**Last Updated**: 2024-11-06  
**Version**: 1.1.0
