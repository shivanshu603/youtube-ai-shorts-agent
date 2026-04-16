from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeVideoClip
)
from moviepy.audio.fx.all import audio_loop, volumex
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

WIDTH, HEIGHT = 1080, 1920

def create_subtitle(text):
    img = Image.new("RGBA", (WIDTH, 300), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)

    # Text wrapping
    words = text.split()
    lines, line = [], ""
    for word in words:
        if len(line + word) < 40:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    y = 20
    for l in lines:
        w, h = draw.textbbox((0, 0), l, font=font)[2:]
        draw.text(((WIDTH - w) / 2, y), l, font=font, fill="white")
        y += h + 10

    return np.array(img)

def create_video(image_paths, audio_paths, output_path, narrations):
    clips = []

    for img_path, aud_path, narration in zip(image_paths, audio_paths, narrations):
        audio = AudioFileClip(aud_path)

        # Image with cinematic zoom
        img_clip = (
            ImageClip(img_path)
            .set_duration(audio.duration)
            .resize(height=HEIGHT)
            .crop(x_center=540, width=WIDTH)
            .resize(lambda t: 1 + 0.05 * t)
        )

        subtitle = (
            ImageClip(create_subtitle(narration))
            .set_duration(audio.duration)
            .set_position(("center", "bottom"))
        )

        final = CompositeVideoClip([img_clip, subtitle]).set_audio(audio)
        clips.append(final)

    video = concatenate_videoclips(clips, method="compose", padding=-0.5)

    # Add background music
    if os.path.exists("music/bgm.mp3"):
        bgm = AudioFileClip("music/bgm.mp3")
        bgm = audio_loop(bgm, duration=video.duration)
        bgm = volumex(bgm, 0.2)
        final_audio = CompositeVideoClip([video]).audio
        video = video.set_audio(final_audio.set_duration(video.duration).fx(volumex, 1))
        video = video.set_audio(final_audio)

    video.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac"
    )
