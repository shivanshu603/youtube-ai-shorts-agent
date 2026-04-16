import requests
import os
from PIL import Image
from io import BytesIO


def generate_image(prompt: str, output_path: str):
    """
    Generate image using Pollinations AI (fast + free).
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"🎨 Generating image: {prompt}")

    try:
        # Improve prompt quality automatically
        enhanced_prompt = f"{prompt}, cinematic lighting, ultra realistic, 4k, detailed, dramatic"

        url = f"https://image.pollinations.ai/prompt/{enhanced_prompt}"

        response = requests.get(url, timeout=60)

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code}")

        image = Image.open(BytesIO(response.content))

        # Resize to vertical Shorts format
        image = image.resize((1080, 1920))

        image.save(output_path)

        print(f"✅ Image saved: {output_path}")

    except Exception as e:
        print(f"❌ Image generation failed: {e}")
