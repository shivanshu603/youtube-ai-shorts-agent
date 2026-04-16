import os
from gtts import gTTS
from pydub import AudioSegment

def generate_voice(text, output_path, lang="en"):
    """
    Generate natural-sounding voice narration using gTTS.
    Converts the audio to high-quality MP3 suitable for YouTube Shorts.
    """
    try:
        print("🎙️ Generating voice narration...")

        # Temporary file
        temp_path = output_path.replace(".mp3", "_temp.mp3")

        # Generate speech
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(temp_path)

        # Enhance audio quality
        audio = AudioSegment.from_mp3(temp_path)
        audio = audio.set_frame_rate(44100).set_channels(2)
        audio.export(output_path, format="mp3", bitrate="192k")

        # Remove temporary file
        os.remove(temp_path)

        print(f"✅ Voice saved at: {output_path}")

    except Exception as e:
        print(f"❌ Error generating voice: {e}")
        raise
