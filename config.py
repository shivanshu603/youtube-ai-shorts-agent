import os

BASE_DIR = os.getcwd()

VIDEO_DIR = os.path.join(BASE_DIR, "videos")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
MUSIC_DIR = os.path.join(BASE_DIR, "music")
DATA_DIR = os.path.join(BASE_DIR, "data")  # ✅ ADD THIS

FPS = 24

# Create folders
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)  # ✅ ADD THIS
