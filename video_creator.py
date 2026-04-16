from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeVideoClip
)
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

WIDTH, HEIGHT = 1080, 1920

def create_subtitle(text):
    img = Image.new("RGBA", (WIDTH, 300), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
    except:
        font = ImageFont.load_default()

    # Wrap text
    lines = []
    words = text.split()
    line = ""
    for word in words:
        if len(line + word) < 40:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    y = 20
    for l in lines:
        w, h = draw.textsize(l, font=font)
        draw.text(((WIDTH - w) / 2, y), l, font=font, fill="white")
        y += h + 10

    return np.array(img)

def create_video(image_paths, audio_paths, output_path, narrations):
    clips = []

    for img_path, aud_path, narration in zip(image_paths, audio_paths, narrations):
        audio = AudioFileClip(aud_path)

        # Resize image to vertical format
        img = ImageClip(img_path).set_duration(audio.duration)
        img = img.resize(height=HEIGHT)
        img = img.crop(x_center=img.w / 2, width=WIDTH)

        # Ken Burns zoom effect
        img = img.resize(lambda t: 1 + 0.05 * t)

        # Subtitle
        subtitle_img = create_subtitle(narration)
        subtitle = (
            ImageClip(subtitle_img)
            .set_duration(audio.duration)
            .set_position(("center", "bottom"))
        )

        final = CompositeVideoClip([img, subtitle]).set_audio(audio)
        clips.append(final)

    final_video = concatenate_videoclips(clips, method="compose")
    final_video.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        threads=4
    )
