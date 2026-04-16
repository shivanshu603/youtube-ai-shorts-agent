from TTS.api import TTS
import os

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)


def generate_voice(text, output_path):
    print("🎙️ Generating voice...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    tts.tts_to_file(text=text, file_path=output_path)
