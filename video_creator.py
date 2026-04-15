from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os

def create_video(image_paths, audio_paths, output_path):
    clips = []

    for img_path, aud_path in zip(image_paths, audio_paths):
        audio = AudioFileClip(aud_path)
        image = ImageClip(img_path).set_duration(audio.duration)
        image = image.set_audio(audio)
        image = image.resize((1080, 1920))  # Vertical format for YouTube Shorts
        clips.append(image)

    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    final_clip.close()

    # Clean up temporary files
    for clip in clips:
        clip.close()
