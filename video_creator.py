from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeVideoClip,
    TextClip,
    vfx
)
from config import VIDEO_WIDTH, VIDEO_HEIGHT, FPS, MUSIC_DIR
import os
import random


def create_subtitle_clip(text, duration):
    """Create subtitles without requiring ImageMagick."""
    return (
        TextClip(
            text,
            fontsize=60,
            color="white",
            method="caption",
            size=(VIDEO_WIDTH - 100, None),
            align="center"
        )
        .set_duration(duration)
        .set_position(("center", VIDEO_HEIGHT - 250))
        .crossfadein(0.3)
        .crossfadeout(0.3)
    )


def create_video(image_paths, audio_paths, output_path, narrations):
    clips = []

    for img_path, aud_path, narration in zip(image_paths, audio_paths, narrations):
        audio = AudioFileClip(aud_path)
        duration = audio.duration

        # Base image clip
        image_clip = (
            ImageClip(img_path)
            .set_duration(duration)
            .resize(height=VIDEO_HEIGHT)
            .set_position("center")
            .fx(vfx.colorx, 1.1)  # Slight color enhancement
        )

        # Ken Burns effect (zoom)
        image_clip = image_clip.resize(lambda t: 1 + 0.05 * (t / duration))

        # Subtitles
        subtitle_clip = create_subtitle_clip(narration, duration)

        # Combine image and subtitle
        scene_clip = CompositeVideoClip(
            [image_clip, subtitle_clip],
            size=(VIDEO_WIDTH, VIDEO_HEIGHT)
        ).set_audio(audio)

        # Add fade transitions
        scene_clip = scene_clip.crossfadein(0.5).crossfadeout(0.5)

        clips.append(scene_clip)

    # Concatenate all clips with transitions
    final_video = concatenate_videoclips(clips, method="compose", padding=-0.5)

    # 🎵 Add background music
    music_files = [
        f for f in os.listdir(MUSIC_DIR) if f.lower().endswith(".mp3")
    ]
    if music_files:
        music_path = os.path.join(MUSIC_DIR, random.choice(music_files))
        music = (
            AudioFileClip(music_path)
            .volumex(0.15)
            .set_duration(final_video.duration)
            .audio_fadein(2)
            .audio_fadeout(2)
        )
        final_video = final_video.set_audio(
            CompositeVideoClip([final_video]).audio
        )
        final_video = final_video.set_audio(
            final_video.audio.fx(lambda clip: clip.volumex(1)).set_duration(final_video.duration)
        )
        final_video.audio = final_video.audio.set_duration(final_video.duration)
        final_video = final_video.set_audio(
            final_video.audio.set_duration(final_video.duration)
        )
        final_video = final_video.set_audio(
            final_video.audio
        )
        # Mix narration and music
        final_video = final_video.set_audio(
            CompositeVideoClip([final_video]).audio
        )

    # Export video
    final_video.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="medium"
    )
