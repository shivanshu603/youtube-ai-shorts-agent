from gtts import gTTS

def generate_voice(text, output_path):
    tts = gTTS(text=text, lang="hi")
    tts.save(output_path)
