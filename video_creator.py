from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeVideoClip
)
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import textwrap


def create_subtitle_clip(text, duration, video_size=(1080, 1920)):
    """Create subtitle overlay using Pillow instead of ImageMagick."""
    width, height = video_size
    subtitle_height = 300

    # Create transparent image
    img = Image.new("RGBA", (width, subtitle_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Load default font (safe for GitHub Actions)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
    except:
        font = ImageFont.load_default()

    # Wrap text
    wrapped_text = textwrap.fill(text, width=30)

    # Calculate text position
    bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align="center")
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) // 2
    y = (subtitle_height - text_height) // 2

    # Draw semi-transparent background
    background = Image.new("RGBA", (width, subtitle_height), (0, 0, 0, 150))
    img = Image.alpha_composite(background, img)
    draw = ImageDraw.Draw(img)

    # Draw text
    draw.multiline_text(
        (x, y),
        wrapped_text,
        font=font,
        fill="white",
        align="center",
        stroke_width=2,
        stroke_fill="black"
    )

    # Convert to MoviePy clip
    subtitle_clip = (
        ImageClip(np.array(img))
        .set_duration(duration)
        .set_position(("center", "bottom"))
    )

    return subtitle_clip


def create_video(image_paths, audio_paths, output_path, narrations=None):
    """Create a vertical YouTube Shorts video with subtitles and smooth motion."""
    clips = []

    for i, (img_path, aud_path) in enumerate(zip(image_paths, audio_paths)):
        audio = AudioFileClip(aud_path)
        duration = audio.duration

        # Base image clip
        image_clip = (
            ImageClip(img_path)
            .set_duration(duration)
            .resize((1080, 1920))
            .resize(lambda t: 1 + 0.05 * t)  # Ken Burns zoom effect
            .set_position("center")
        )

        # Add subtitles if provided
        if narrations and i < len(narrations):
            subtitle_clip = create_subtitle_clip(
                narrations[i], duration, video_size=(1080, 1920)
            )
            video = CompositeVideoClip([image_clip, subtitle_clip])
        else:
            video = image_clip

        video = video.set_audio(audio)
        clips.append(video.crossfadein(0.5))

    # Concatenate all scenes
    final_clip = concatenate_videoclips(clips, method="compose")

    # Export final video
    final_clip.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        bitrate="8000k",
        preset="medium"
    )
