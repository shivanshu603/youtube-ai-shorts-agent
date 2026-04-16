import os
import random
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    VideoFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
    TextClip
)
from config import VIDEO_WIDTH, VIDEO_HEIGHT, FPS, MUSIC_DIR


def create_video(
    image_paths,
    audio_paths,
    output_path,
    narrations=None,
    avatar_paths=None,
):
    """
    Creates a cinematic vertical video for YouTube Shorts.
    Uses avatar videos if available; otherwise falls back to images.
    Adds subtitles and optional background music.
    """
    clips = []

    for i, audio_path in enumerate(audio_paths):
        audio = AudioFileClip(audio_path)
        duration = audio.duration

        # Use avatar video if available
        if avatar_paths and i < len(avatar_paths) and avatar_paths[i] and os.path.exists(avatar_paths[i]):
            print(f"🎬 Using avatar for scene {i+1}")
            clip = (
                VideoFileClip(avatar_paths[i])
                .resize((VIDEO_WIDTH, VIDEO_HEIGHT))
                .set_duration(duration)
                .set_audio(audio)
            )
        else:
            print(f"🖼️ Using image for scene {i+1}")
            clip = (
                ImageClip(image_paths[i])
                .resize((VIDEO_WIDTH, VIDEO_HEIGHT))
                .set_duration(duration)
                .set_audio(audio)
            )

        # Add subtitles if provided
        if narrations:
            subtitle = (
                TextClip(
                    narrations[i],
                    fontsize=60,
                    color="white",
                    font="DejaVu-Sans-Bold",
                    method="caption",
                    size=(VIDEO_WIDTH - 100, None),
                )
                .set_position(("center", VIDEO_HEIGHT - 300))
                .set_duration(duration)
            )
            clip = CompositeVideoClip([clip, subtitle])

        # Add fade transitions
        clip = clip.fadein(0.5).fadeout(0.5)
        clips.append(clip)

    # Concatenate all clips
    final_clip = concatenate_videoclips(clips, method="compose")

    # Add background music if available
    if os.path.exists(MUSIC_DIR):
        music_files = [
            f for f in os.listdir(MUSIC_DIR)
            if f.lower().endswith((".mp3", ".wav"))
        ]
        if music_files:
            music_path = os.path.join(MUSIC_DIR, random.choice(music_files))
            print(f"🎵 Adding background music: {music_path}")
            bg_music = (
                AudioFileClip(music_path)
                .volumex(0.2)
                .set_duration(final_clip.duration)
            )
            final_clip = final_clip.set_audio(
                CompositeVideoClip([final_clip]).audio
            )
            final_clip = final_clip.set_audio(
                final_clip.audio.volumex(1.0).audio_fadein(1).audio_fadeout(1)
            )

    # Export final video
    print(f"💾 Exporting video to: {output_path}")
    final_clip.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="medium"
    )

    print("✅ Video creation completed!")
