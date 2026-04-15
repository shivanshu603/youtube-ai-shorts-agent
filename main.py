import os
import json
from datetime import datetime
import google.generativeai as genai

from config import *
from prompts import STORY_PROMPT
from story_manager import get_next_episode
from image_generator import generate_image
from voice_generator import generate_voice
from video_creator import create_video
from youtube_uploader import upload_video

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

def generate_story():
    response = model.generate_content(STORY_PROMPT)
    text = response.text
    start = text.find("{")
    end = text.rfind("}") + 1
    return json.loads(text[start:end])

def main():
    story_no, episode_no = get_next_episode()
    data = generate_story()

    image_paths = []
    audio_paths = []

    for i, scene in enumerate(data["scenes"]):
        img_path = f"{IMAGE_DIR}/scene_{i}.jpg"
        aud_path = f"{AUDIO_DIR}/scene_{i}.mp3"
        generate_image(scene["image_prompt"], img_path)
        generate_voice(scene["narration"], aud_path)
        image_paths.append(img_path)
        audio_paths.append(aud_path)

    video_path = f"{VIDEO_DIR}/story_{story_no}_ep_{episode_no}.mp4"
    create_video(image_paths, audio_paths, video_path)

    title = f"{data['youtube_title']} | Episode {episode_no}"
    upload_video(video_path, title, data["description"], data["tags"])

if __name__ == "__main__":
    main()
