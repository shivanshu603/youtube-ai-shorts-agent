import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_DIR = os.path.join(BASE_DIR, "images")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
VIDEO_DIR = os.path.join(BASE_DIR, "videos")
MUSIC_DIR = os.path.join(BASE_DIR, "music")
DATA_DIR = os.path.join(BASE_DIR, "data")

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 30

# Ensure directories exist
for directory in [IMAGE_DIR, AUDIO_DIR, VIDEO_DIR, MUSIC_DIR, DATA_DIR]:
    os.makedirs(directory, exist_ok=True)
