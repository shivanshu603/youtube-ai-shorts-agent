import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directories for storing generated assets
IMAGE_DIR = os.path.join(BASE_DIR, "images")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
VIDEO_DIR = os.path.join(BASE_DIR, "videos")
DATA_DIR = os.path.join(BASE_DIR, "data")  # ✅ Required for story_manager

# Create directories if they don't exist
for directory in [IMAGE_DIR, AUDIO_DIR, VIDEO_DIR, DATA_DIR]:
    os.makedirs(directory, exist_ok=True)
