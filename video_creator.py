import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from moviepy.audio.AudioClip import CompositeAudioClip
from config import FPS, MUSIC_DIR


def create_video(video_paths, audio_paths, output_path):
    clips = []

    for i, video_path in enumerate(video_paths):
        print(f"🎬 Processing scene {i+1}")

        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_paths[i])

        clip = video.set_audio(audio).set_duration(audio.duration)

        # smooth transitions
        clip = clip.fadein(0.5).fadeout(0.5)

        clips.append(clip)

    final_clip = concatenate_videoclips(clips, method="compose")

    # 🎵 Background Music
    if os.path.exists(MUSIC_DIR):
        files = [f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")]

        if files:
            music_path = os.path.join(MUSIC_DIR, random.choice(files))
            print(f"🎵 Adding music: {music_path}")

            bg_music = AudioFileClip(music_path).volumex(0.2)
            bg_music = bg_music.set_duration(final_clip.duration)

            final_audio = CompositeAudioClip([final_clip.audio, bg_music])
            final_clip = final_clip.set_audio(final_audio)

    print(f"💾 Exporting: {output_path}")
    final_clip.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac"
    )

    print("✅ Video ready!")
