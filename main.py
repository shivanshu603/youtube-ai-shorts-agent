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
    print("🧠 Generating a new story...")
    story_no, episode_no = get_next_episode()
    data = generate_story()

    image_paths = []
    audio_paths = []
    avatar_paths = []

    # Ensure directories exist
    os.makedirs(IMAGE_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)

    for i, scene in enumerate(data["scenes"], start=1):
        img_path = os.path.join(IMAGE_DIR, f"scene_{i}.jpg")
        aud_path = os.path.join(AUDIO_DIR, f"scene_{i}.mp3")
        avatar_path = os.path.join(VIDEO_DIR, f"avatar_scene_{i}.mp4")

        # 🎨 IMAGE
        print(f"🎨 Generating image for scene {i}...")
        try:
            generate_image(scene["image_prompt"], img_path)
        except Exception as e:
            print(f"⚠️ Image failed: {e}")
            img_path = None

        # 🎙️ AUDIO
        print(f"🎙️ Generating voice for scene {i}...")
        try:
            generate_voice(scene["narration"], aud_path)
        except Exception as e:
            print(f"⚠️ Voice failed: {e}")
            aud_path = None

        # 🧑 AVATAR (OPTIONAL)
        print(f"🧑 Generating avatar for scene {i}...")
        try:
            if os.path.exists("assets/avatar.jpg") and aud_path:
                generate_avatar("assets/avatar.jpg", aud_path, avatar_path)
                avatar_paths.append(avatar_path)
            else:
                raise Exception("Avatar image or audio missing")
        except Exception as e:
            print(f"⚠️ Avatar failed: {e}")
            avatar_paths.append(None)

        image_paths.append(img_path)
        audio_paths.append(aud_path)

    # 🎬 CREATE VIDEO
    video_path = os.path.join(
        VIDEO_DIR, f"story_{story_no}_ep_{episode_no}.mp4"
    )

    narrations = [scene["narration"] for scene in data["scenes"]]

    print("🎬 Creating final cinematic video...")
    create_video(
        image_paths=image_paths,
        audio_paths=audio_paths,
        avatar_paths=avatar_paths,
        narrations=narrations,
        output_path=video_path
    )

    # 📤 UPLOAD
    title = f"{data['youtube_title']} | Episode {episode_no}"
    description = data["description"]
    tags = data.get("tags", [])

    print("📤 Uploading video to YouTube...")
    upload_video(video_path, title, description, tags)

    print(f"✅ Episode {episode_no} uploaded successfully!")


def main():
    print("🚀 Starting Continuous YouTube AI Shorts Agent...")

    NUMBER_OF_VIDEOS = int(os.getenv("NUMBER_OF_VIDEOS", 3))
    DELAY_BETWEEN_UPLOADS = int(os.getenv("UPLOAD_DELAY", 300))

    for i in range(NUMBER_OF_VIDEOS):
        print(f"\n🎬 Creating Video {i + 1}/{NUMBER_OF_VIDEOS}")
        try:
            create_and_upload_video()
        except Exception as e:
            print(f"❌ Error while creating video {i + 1}: {e}")

        if i < NUMBER_OF_VIDEOS - 1:
            print(f"⏳ Waiting {DELAY_BETWEEN_UPLOADS} seconds...")
            time.sleep(DELAY_BETWEEN_UPLOADS)

    print("🏁 All videos created and uploaded successfully!")


if __name__ == "__main__":
    main()
