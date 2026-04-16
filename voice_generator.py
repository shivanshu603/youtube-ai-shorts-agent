import os
from TTS.api import TTS

# Load multilingual model (Hindi supported)
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

def generate_voice(text, output_path):
    print("🎙️ Generating Hindi male voice...")

    # Add natural speaking style
    text = f"{text}..."

    tts.tts_to_file(
        text=text,
        file_path=output_path,
        speaker_wav="assets/male_voice.wav",  # 👈 IMPORTANT
        language="hi"
    )

    print(f"✅ Voice saved: {output_path}")
