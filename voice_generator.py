from TTS.api import TTS

# Load model once (English example)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

def generate_voice(text, output_path):
    print("🎙️ Generating natural voice...")
    tts.tts_to_file(text=text, file_path=output_path)
