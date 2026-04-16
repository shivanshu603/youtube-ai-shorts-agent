import os
import subprocess
from config import VIDEO_DIR

WAV2LIP_DIR = "Wav2Lip"
CHECKPOINT_PATH = os.path.join(WAV2LIP_DIR, "checkpoints", "wav2lip_gan.pth")


def generate_avatar(face_image, audio_path, output_path):
    """
    Generates a lip-synced talking avatar using Wav2Lip.
    """
    if not os.path.exists(WAV2LIP_DIR):
        subprocess.run(
            ["git", "clone", "https://github.com/Rudrabha/Wav2Lip.git"],
            check=True
        )

    command = [
        "python",
        os.path.join(WAV2LIP_DIR, "inference.py"),
        "--checkpoint_path", CHECKPOINT_PATH,
        "--face", face_image,
        "--audio", audio_path,
        "--outfile", output_path
    ]

    subprocess.run(command, check=True)
