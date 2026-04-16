import os

BASE_DIR = os.getcwd()

VIDEO_DIR = os.path.join(BASE_DIR, "videos")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
MUSIC_DIR = os.path.join(BASE_DIR, "music")

FPS = 24

os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)
