from PIL import Image, ImageDraw, ImageFont
import os
from config import IMAGE_DIR

os.makedirs(IMAGE_DIR, exist_ok=True)

def generate_image(prompt, path):
    img = Image.new("RGB", (1080, 1920), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
    except:
        font = ImageFont.load_default()

    draw.text((100, 900), prompt[:80], fill=(255, 255, 255), font=font)
    img.save(path)
