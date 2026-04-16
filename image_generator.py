from diffusers import StableDiffusionPipeline
import torch
import os

# Load the model once
MODEL_ID = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float32,
    safety_checker=None
)
pipe.to("cpu")

def generate_image(prompt: str, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"🎨 Generating image: {prompt}")
    image = pipe(
        prompt=prompt,
        num_inference_steps=20,
        guidance_scale=7.5,
        height=1024,
        width=576  # Vertical format for Shorts
    ).images[0]

    image.save(output_path)
