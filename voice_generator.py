import os
from gtts import gTTS
from pydub import AudioSegment
from pydub.utils import which

AudioSegment.converter = which("ffmpeg")

def generate_voice(text, output_path):
    print("🎙️ Generating Hindi voice...")

    tts = gTTS(text=text, lang="hi")

    temp_mp3 = output_path.replace(".mp3", "_temp.mp3")
    tts.save(temp_mp3)

    audio = AudioSegment.from_mp3(temp_mp3)

    # Slight deep voice effect
    audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * 0.9)
    }).set_frame_rate(audio.frame_rate)

    audio.export(output_path, format="mp3")
    os.remove(temp_mp3)

    print(f"✅ Voice saved: {output_path}")
