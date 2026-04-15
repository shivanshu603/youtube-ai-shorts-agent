from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeAudioClip,
)
import os


def create_video(image_paths, audio_paths, output_path):
    clips = []

    for img_path, aud_path in zip(image_paths, audio_paths):
        audio = AudioFileClip(aud_path)
        duration = audio.duration

        # Ken Burns effect (zoom-in)
        image_clip = (
            ImageClip(img_path)
            .set_duration(duration)
            .resize(height=1920)
            .resize(lambda t: 1 + 0.05 * t)  # slight zoom
            .set_audio(audio)
            .crossfadein(0.5)
        )

        clips.append(image_clip)

    final_clip = concatenate_videoclips(clips, method="compose")

    # Add background music if available
    music_path = "assets/background_music.mp3"
    if os.path.exists(music_path):
        music = AudioFileClip(music_path).volumex(0.2)
        final_audio = CompositeAudioClip([final_clip.audio, music])
        final_clip = final_clip.set_audio(final_audio)

    final_clip.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        bitrate="8000k"
    )
