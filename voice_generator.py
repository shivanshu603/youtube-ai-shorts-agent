from gtts import gTTS
import os
from config import AUDIO_DIR

os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_voice(text, path, lang="hi"):
    tts = gTTS(text=text, lang=lang)
    tts.save(path)
