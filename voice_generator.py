from TTS.api import TTS
import os

# Initialize a stable, non-interactive TTS model
# This model is high quality and works well in GitHub Actions.
tts = TTS(
    model_name="tts_models/en/ljspeech/tacotron2-DDC",
    progress_bar=False,
    gpu=False
)

def generate_voice(text: str, output_path: str):
    """
    Generate natural-sounding narration audio.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("🎙️ Generating natural voice...")
    tts.tts_to_file(
        text=text,
        file_path=output_path
    )
