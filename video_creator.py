from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os

def create_video(image_paths, audio_paths, output_path):
    clips = []

    for img, aud in zip(image_paths, audio_paths):
        audio = AudioFileClip(aud)
        clip = (
            ImageClip(img)
            .set_duration(audio.duration)
            .set_audio(audio)
            .resize((1080, 1920))
        )
        clips.append(clip)

    final_video = concatenate_videoclips(clips, method="compose")
    final_video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )
