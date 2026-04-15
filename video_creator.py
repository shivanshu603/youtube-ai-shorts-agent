from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

def create_video(image_paths, audio_paths, output_path):
    clips = []

    for img, aud in zip(image_paths, audio_paths):
        audio = AudioFileClip(aud)
        clip = (
            ImageClip(img)
            .set_duration(audio.duration)
            .set_audio(audio)
            .resize((1080, 1920))  # Vertical for Shorts
        )
        clips.append(clip)

    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_path, fps=24)
