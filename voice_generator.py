from TTS.api import TTS
import os

# Initialize TTS with a non-interactive model
tts = TTS(
    model_name="tts_models/en/ljspeech/tacotron2-DDC",
    progress_bar=False,
    gpu=False
)

def generate_voice(text: str, output_path: str):
    """
    Generate natural-sounding voice for narration.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("🎙️ Generating natural voice...")
    tts.tts_to_file(
        text=text,
        file_path=output_path
    )
