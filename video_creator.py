import os
import random
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    VideoFileClip,
    CompositeVideoClip,
    concatenate_videoclips
)
from config import VIDEO_WIDTH, VIDEO_HEIGHT, FPS, MUSIC_DIR


def create_video(
    image_paths,
    audio_paths,
    output_path,
    narrations=None,
    avatar_paths=None,
):
    clips = []

    for i, audio_path in enumerate(audio_paths):

        if not audio_path or not os.path.exists(audio_path):
            print(f"⚠️ Skipping scene {i+1} (no audio)")
            continue

        audio = AudioFileClip(audio_path)
        duration = audio.duration

        # 🎬 AVATAR OR IMAGE
        if avatar_paths and i < len(avatar_paths) and avatar_paths[i] and os.path.exists(avatar_paths[i]):
            print(f"🎬 Using avatar for scene {i+1}")
            clip = VideoFileClip(avatar_paths[i]).resize((VIDEO_WIDTH, VIDEO_HEIGHT))
        else:
            if not image_paths[i] or not os.path.exists(image_paths[i]):
                print(f"⚠️ Skipping scene {i+1} (no image)")
                continue

            print(f"🖼️ Using image for scene {i+1}")
            clip = ImageClip(image_paths[i]).resize((VIDEO_WIDTH, VIDEO_HEIGHT))

        clip = clip.set_duration(duration).set_audio(audio)

        # 🎞️ Cinematic zoom (Ken Burns effect)
        clip = clip.resize(lambda t: 1 + 0.05 * t)

        # ✨ Smooth fade
        clip = clip.fadein(0.5).fadeout(0.5)

        clips.append(clip)

    if not clips:
        raise RuntimeError("❌ No valid clips to render video")

    final_clip = concatenate_videoclips(clips, method="compose")

    # 🎵 BACKGROUND MUSIC (FIXED)
    if os.path.exists(MUSIC_DIR):
        music_files = [
            f for f in os.listdir(MUSIC_DIR)
            if f.lower().endswith((".mp3", ".wav"))
        ]

        if music_files:
            music_path = os.path.join(MUSIC_DIR, random.choice(music_files))
            print(f"🎵 Adding background music: {music_path}")

            bg_music = AudioFileClip(music_path).volumex(0.15)

            bg_music = bg_music.set_duration(final_clip.duration)

            final_audio = CompositeVideoClip([final_clip]).audio
            final_audio = final_audio.volumex(1.0)

            final_audio = final_audio.set_duration(final_clip.duration)

            final_clip = final_clip.set_audio(
                final_audio.audio_fadein(1).audio_fadeout(1)
            )

    # 💾 EXPORT
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
