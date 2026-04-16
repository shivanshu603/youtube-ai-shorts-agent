from gtts import gTTS
from pydub import AudioSegment
from pydub.utils import which
import os

# Ensure ffmpeg is available
AudioSegment.converter = which("ffmpeg")


def generate_voice(text, output_path):
    """
    Generate voice using Google TTS (fast + stable).
    """

    print("🎙️ Generating voice narration...")

    try:
        # Generate TTS
        tts = gTTS(text=text, lang="en", slow=False)
        temp_mp3 = output_path.replace(".mp3", "_temp.mp3")
        tts.save(temp_mp3)

        # Normalize audio (better sound)
        audio = AudioSegment.from_mp3(temp_mp3)
        audio = audio + 3  # increase volume slightly
        audio.export(output_path, format="mp3")

        os.remove(temp_mp3)

        print(f"✅ Voice saved at: {output_path}")

    except Exception as e:
        print(f"❌ Voice generation failed: {e}")
