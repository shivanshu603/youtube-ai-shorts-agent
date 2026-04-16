from TTS.api import TTS
from pydub import AudioSegment
from pydub.utils import which
import os

# Ensure pydub can find ffmpeg
AudioSegment.converter = which("ffmpeg")

# Initialize TTS model
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

def generate_voice(text, output_path):
    """
    Generate natural-sounding voice narration for a scene.
    """
    print("🎙️ Generating voice narration...")

    temp_wav = output_path.replace(".mp3", ".wav")
    tts.tts_to_file(text=text, file_path=temp_wav)

    # Convert WAV to MP3
    audio = AudioSegment.from_wav(temp_wav)
    audio.export(output_path, format="mp3")
    os.remove(temp_wav)

    print(f"✅ Voice saved at: {output_path}")
