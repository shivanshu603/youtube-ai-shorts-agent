from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from PIL import Image
import numpy as np

# Compatibility patch for Pillow >= 10
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS


def create_video(image_paths, audio_paths, output_path):
    clips = []

    for img_path, aud_path in zip(image_paths, audio_paths):
        audio = AudioFileClip(aud_path)
        image = ImageClip(img_path).set_duration(audio.duration)

        # Resize for YouTube Shorts (Vertical 9:16)
        image = image.resize((1080, 1920))
        image = image.set_audio(audio)

        clips.append(image)

    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )
