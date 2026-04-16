import os
import time
from config import VIDEO_DIR, AUDIO_DIR
from story_manager import get_next_episode
from story_generator_local import generate_story
from media_fetcher import fetch_video
from voice_generator import generate_voice
from video_creator import create_video
from youtube_uploader import upload_video


def create_and_upload_video():
    print("🧠 Generating story...")
    story_no, episode_no = get_next_episode()
    data = generate_story()

    video_clips = []
    audio_paths = []

    for i, scene in enumerate(data["scenes"], start=1):
        video_path = os.path.join(VIDEO_DIR, f"scene_{i}.mp4")
        audio_path = os.path.join(AUDIO_DIR, f"scene_{i}.mp3")

        print(f"🎥 Fetching video for scene {i}...")
        fetch_video(scene["image_prompt"], video_path)

        print(f"🎙️ Generating voice for scene {i}...")
        generate_voice(scene["narration"], audio_path)

        video_clips.append(video_path)
        audio_paths.append(audio_path)

    final_video = os.path.join(
        VIDEO_DIR, f"story_{story_no}_ep_{episode_no}.mp4"
    )

    print("🎬 Creating final video...")
    create_video(video_clips, audio_paths, final_video)

    print("📤 Uploading to YouTube...")
    upload_video(
        final_video,
        f"{data['youtube_title']} | Ep {episode_no}",
        data["description"],
        data.get("tags", []),
    )

    print("✅ Upload done!")


def main():
    NUMBER_OF_VIDEOS = int(os.getenv("NUMBER_OF_VIDEOS", 3))
    DELAY = int(os.getenv("UPLOAD_DELAY", 300))

    for i in range(NUMBER_OF_VIDEOS):
        print(f"\n🎬 Video {i+1}/{NUMBER_OF_VIDEOS}")
        try:
            create_and_upload_video()
        except Exception as e:
            print(f"❌ Error: {e}")

        if i < NUMBER_OF_VIDEOS - 1:
            print(f"⏳ Waiting {DELAY} sec...")
            time.sleep(DELAY)


if __name__ == "__main__":
    main()
