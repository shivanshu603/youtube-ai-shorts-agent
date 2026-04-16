import os
import torch
from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig
from torch.serialization import add_safe_globals

# Allow PyTorch to load XTTS configuration safely
add_safe_globals([XttsConfig])

# Initialize XTTS model
tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/xtts_v2",
    progress_bar=False,
    gpu=False
)

def generate_voice(text: str, output_path: str, speaker_wav: str = None, language: str = "en"):
    """
    Generate high-quality multilingual voice using XTTS v2.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("🎙️ Generating XTTS voice...")
    tts.tts_to_file(
        text=text,
        file_path=output_path,
        speaker_wav=speaker_wav,
        language=language
    )
