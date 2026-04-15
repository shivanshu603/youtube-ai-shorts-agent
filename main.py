from google import genai
from google.genai import types
import json
import os
from datetime import datetime

from config import *
from prompts import STORY_PROMPT
from story_manager import get_next_episode
from image_generator import generate_image
from voice_generator import generate_voice
from video_creator import create_video
from youtube_uploader import upload_video

# Initialize Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_story():
    response = client.models.generate_content(
        model="gemini-1.5-flash",  # ✅ Updated model
        contents=STORY_PROMPT,
        config=types.GenerateContentConfig(
            temperature=0.8,
            max_output_tokens=2048
        )
    )

    # Extract text safely
    if hasattr(response, "text") and response.text:
        text = response.text
    else:
        # Fallback extraction
        text = ""
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, "text"):
                    text += part.text

    # Extract JSON from response
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == -1:
        raise ValueError("Failed to parse JSON from Gemini response.")

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
