from huggingface_hub import InferenceClient
from PIL import Image
import os

client = InferenceClient(
    model="stabilityai/stable-diffusion-xl-base-1.0",
    token=os.getenv("HF_TOKEN")
)

def generate_image(prompt, output_path):
    print(f"🖼️ Generating image: {prompt}")
    image = client.text_to_image(
        prompt=prompt,
        negative_prompt="blurry, low quality, distorted, cartoonish",
        height=1920,
        width=1080,
        num_inference_steps=30
    )
    image.save(output_path)
