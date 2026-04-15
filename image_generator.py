# from PIL import Image, ImageDraw, ImageFont
# import os
# from config import IMAGE_DIR

# os.makedirs(IMAGE_DIR, exist_ok=True)

# def generate_image(prompt, path):
#     img = Image.new("RGB", (1080, 1920), color=(20, 20, 20))
#     draw = ImageDraw.Draw(img)
#     try:
#         font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
#     except:
#         font = ImageFont.load_default()

#     draw.text((100, 900), prompt[:80], fill=(255, 255, 255), font=font)
#     img.save(path)
import requests

def generate_image(prompt, output_path):
    url = f"https://image.pollinations.ai/prompt/{prompt}?width=1024&height=1792&seed=42"
    response = requests.get(url)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)
