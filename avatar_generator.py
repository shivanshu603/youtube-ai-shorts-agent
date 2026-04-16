import subprocess
import os

def generate_avatar(face_path, audio_path, output_path):
    """
    Generates a talking avatar video using Wav2Lip.
    """
    if not os.path.exists(face_path):
        raise FileNotFoundError(f"Avatar image not found: {face_path}")
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    command = [
        "python", "Wav2Lip/inference.py",
        "--checkpoint_path", "Wav2Lip/checkpoints/wav2lip_gan.pth",
        "--face", face_path,
        "--audio", audio_path,
        "--outfile", output_path,
        "--resize_factor", "1",
        "--pads", "0", "20", "0", "0"
    ]

    print(f"🧑 Generating avatar: {output_path}")
    subprocess.run(command, check=True)
    print(f"✅ Avatar video created: {output_path}")
