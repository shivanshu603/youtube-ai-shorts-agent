import os
import time
from config import IMAGE_DIR, AUDIO_DIR, VIDEO_DIR
from story_manager import get_next_episode
from story_generator_local import generate_story
from image_generator import generate_image
from voice_generator import generate_voice
from video_creator import create_video
from youtube_uploader import upload_video
from avatar_generator import generate_avatar


def create_and_upload_video():
    story_no, episode_no = get_next_episode()
    data = generate_story()

    image_paths = []
    audio_paths = []
    avatar_paths = []

    for i, scene in enumerate(data["scenes"], start=1):
        img_path = os.path.join(IMAGE_DIR, f"scene_{i}.jpg")
        aud_path = os.path.join(AUDIO_DIR, f"scene_{i}.mp3")
        avatar_video_path = os.path.join(VIDEO_DIR, f"avatar_scene_{i}.mp4")

        print(f"🎨 Generating image for scene {i}...")
        generate_image(scene["image_prompt"], img_path)

        print(f"🎙️ Generating voice for scene {i}...")
        generate_voice(scene["narration"], aud_path)

        print(f"🧑 Generating avatar for scene {i}...")
        generate_avatar("assets/avatar.jpg", aud_path, avatar_video_path)

        image_paths.append(img_path)
        audio_paths.append(aud_path)
        avatar_paths.append(avatar_video_path)

    video_path = os.path.join(
        VIDEO_DIR, f"story_{story_no}_ep_{episode_no}.mp4"
    )
    narrations = [scene["narration"] for scene in data["scenes"]]

    print("🎬 Creating final video...")
    create_video(image_paths, audio_paths, video_path, narrations, avatar_paths)

    title = f"{data['youtube_title']} | Episode {episode_no}"
    description = data["description"]
    tags = data.get("tags", [])

    print("📤 Uploading video to YouTube...")
    upload_video(video_path, title, description, tags)

    print(f"✅ Episode {episode_no} uploaded successfully!")


def main():
    print("🚀 Starting Continuous YouTube AI Shorts Agent...")

    number_of_videos = int(os.getenv("NUMBER_OF_VIDEOS", 3))
    delay_between_uploads = int(os.getenv("UPLOAD_DELAY", 300))

    for i in range(number_of_videos):
        print(f"\n🎬 Creating Video {i + 1}/{number_of_videos}")
        try:
            create_and_upload_video()
        except Exception as e:
            print(f"❌ Error while creating video {i + 1}: {e}")

        if i < number_of_videos - 1:
            print(f"⏳ Waiting {delay_between_uploads} seconds...")
            time.sleep(delay_between_uploads)

    print("🏁 All videos created and uploaded successfully!")


if __name__ == "__main__":
    main()
