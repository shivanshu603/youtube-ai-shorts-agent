import json
import os
import re
import time
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

MODEL_REPO = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
MODEL_FILE = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"


def load_model():
    """Download and load the TinyLlama GGUF model."""
    model_path = hf_hub_download(
        repo_id=MODEL_REPO,
        filename=MODEL_FILE,
        token=os.getenv("HF_TOKEN")  # Optional but recommended
    )
    return Llama(
        model_path=model_path,
        n_ctx=2048,
        n_threads=4,
        verbose=False
    )


# Load model once
llm = load_model()


def extract_json(text: str) -> str:
    """Extract the first JSON object from the model output."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in the model output.")
    return match.group(0)


def validate_story(data: dict) -> bool:
    """Validate the structure of the generated story."""
    required_keys = [
        "story_title",
        "scenes",
        "youtube_title",
        "description",
        "tags",
    ]

    if not all(key in data for key in required_keys):
        return False

    if not isinstance(data["scenes"], list) or len(data["scenes"]) != 5:
        return False

    for scene in data["scenes"]:
        if "narration" not in scene or "image_prompt" not in scene:
            return False

    return True


def generate_story(max_retries: int = 5):
    """
    Generate a new unique story using the local LLM.
    Retries until valid JSON is produced.
    """
    for attempt in range(1, max_retries + 1):
        print(f"🧠 Generating story (Attempt {attempt}/{max_retries})...")

        prompt = f"""
<s>[INST]
You are a creative storyteller.

Create a completely new and unique Hindi moral story for a YouTube Shorts video.
Do not repeat previous stories. Ensure originality.

Respond ONLY with valid JSON in the following format:
{{
  "story_title": "",
  "scenes": [
    {{"narration": "", "image_prompt": ""}},
    {{"narration": "", "image_prompt": ""}},
    {{"narration": "", "image_prompt": ""}},
    {{"narration": "", "image_prompt": ""}},
    {{"narration": "", "image_prompt": ""}}
  ],
  "youtube_title": "",
  "description": "",
  "tags": []
}}

Requirements:
- Exactly 5 scenes.
- Each narration should be 1–2 sentences.
- The final scene must include a clear moral lesson.
- Use simple Hindi language suitable for all ages.
- Do not include any explanation or extra text.
[/INST]
"""

        try:
            response = llm(
                prompt,
                max_tokens=900,
                temperature=0.9,  # Higher temperature for uniqueness
                top_p=0.95,
                stop=["</s>"]
            )

            raw_text = response["choices"][0]["text"]
            print("🔍 Raw Model Output:\n", raw_text)

            json_text = extract_json(raw_text)
            data = json.loads(json_text)

            if validate_story(data):
                print("✅ Successfully generated a new unique story.")
                return data
            else:
                print("⚠️ Invalid structure. Retrying...")

        except Exception as e:
            print(f"⚠️ Error during generation: {e}")

        # Small delay before retrying
        time.sleep(2)

    # If all retries fail, raise an error (no fallback as requested)
    raise RuntimeError(
        "❌ Failed to generate a valid story after multiple attempts."
    )
