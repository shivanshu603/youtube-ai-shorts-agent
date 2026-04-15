from gtts import gTTS
from pydub import AudioSegment
import os

def generate_voice(text, output_path):
    temp_path = output_path.replace(".mp3", "_temp.mp3")
    
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(temp_path)

    # Normalize and enhance audio
    audio = AudioSegment.from_mp3(temp_path)
    audio = audio.normalize()
    audio.export(output_path, format="mp3")

    os.remove(temp_path)
