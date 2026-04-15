import os

# Gemini API
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# YouTube API Credentials
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Directories
BASE_DIR = "assets"
IMAGE_DIR = f"{BASE_DIR}/images"
AUDIO_DIR = f"{BASE_DIR}/audio"
VIDEO_DIR = f"{BASE_DIR}/videos"
THUMBNAIL_DIR = f"{BASE_DIR}/thumbnails"
SUBTITLE_DIR = f"{BASE_DIR}/subtitles"
