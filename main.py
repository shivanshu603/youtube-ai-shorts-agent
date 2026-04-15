import os
from datetime import datetime

from config import IMAGE_DIR, AUDIO_DIR, VIDEO_DIR
from story_manager import get_next_episode
from story_generator_local import generate_story
from image_generator import generate_image
from voice_generator import generate_voice
from video_creator import create_video
from youtube_uploader import upload_video
from huggingface_hub import hf_hub_download

model_path = hf_hub_download(
    repo_id="microsoft/Phi-3-mini-4k-instruct",
    filename="model.gguf",
    token=os.getenv("HF_TOKEN")
)

def main():
    print("🚀 Starting YouTube AI Shorts Agent...")

    # Get next story and episode number
    story_no, episode_no = get_next_episode()

    # Generate story using local model
    data = generate_story()

    image_paths = []
    audio_paths = []

    # Generate images and voice for each scene
    for i, scene in enumerate(data["scenes"], start=1):
        img_path = os.path.join(IMAGE_DIR, f"scene_{i}.jpg")
        aud_path = os.path.join(AUDIO_DIR, f"scene_{i}.mp3")

        print(f"🎨 Generating image for scene {i}...")
        generate_image(scene["image_prompt"], img_path)

        print(f"🎙️ Generating voice for scene {i}...")
        generate_voice(scene["narration"], aud_path)

        image_paths.append(img_path)
        audio_paths.append(aud_path)

    # Create final video
    video_path = os.path.join(
        VIDEO_DIR, f"story_{story_no}_ep_{episode_no}.mp4"
    )
    print("🎬 Creating final video...")
    create_video(image_paths, audio_paths, video_path)

    # Upload to YouTube
    title = f"{data['youtube_title']} | Episode {episode_no}"
    description = data["description"]
    tags = data.get("tags", [])

    print("📤 Uploading video to YouTube...")
    upload_video(video_path, title, description, tags)

    print("✅ Video successfully uploaded!")


if __name__ == "__main__":
    main()
