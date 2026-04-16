from TTS.api import TTS
import os

# High-quality multi-speaker model
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

def generate_voice(text: str, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("🎙️ Generating high-quality voice...")
    tts.tts_to_file(
        text=text,
        file_path=output_path,
        speaker="female",
        language="en"
    )
