import json
import re
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

# Download GGUF model (public and accessible)
MODEL_PATH = hf_hub_download(
    repo_id="TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
    filename="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
)

# Load model
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=4
)

def extract_json(text: str):
    """
    Extract the first valid JSON object from the model output.
    """
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in the model output.")
    return match.group(0)

def generate_story(max_retries: int = 5):
    """
    Generate a brand-new story in strict JSON format.
    Retries automatically until valid JSON is produced.
    """
    print("🧠 Generating a new story...")

    prompt = """
You are a professional storyteller creating engaging YouTube Shorts.

Generate a completely NEW and ORIGINAL story every time.

Return ONLY valid JSON in the following format (no extra text):

{
  "story_title": "Short engaging title",
  "youtube_title": "Catchy YouTube Shorts title with hook",
  "description": "SEO optimized description for YouTube",
  "tags": ["tag1", "tag2", "tag3"],
  "scenes": [
    {
      "narration": "Scene narration text (1-2 sentences)",
      "image_prompt": "Detailed visual description for image generation"
    },
    {
      "narration": "Scene narration text",
      "image_prompt": "Detailed visual description"
    },
    {
      "narration": "Scene narration text",
      "image_prompt": "Detailed visual description"
    },
    {
      "narration": "Scene narration text",
      "image_prompt": "Detailed visual description"
    },
    {
      "narration": "Scene narration text",
      "image_prompt": "Detailed visual description"
    }
  ]
}
"""

    for attempt in range(1, max_retries + 1):
        print(f"🔄 Attempt {attempt}/{max_retries}...")

        response = llm(
            prompt,
            max_tokens=1500,
            temperature=0.9,
            top_p=0.95,
            stop=["```"]
        )

        text = response["choices"][0]["text"].strip()
        print("🔍 Raw Model Output:\n", text[:500], "...\n")

        try:
            json_text = extract_json(text)
            data = json.loads(json_text)

            # Basic validation
            required_keys = [
                "story_title",
                "youtube_title",
                "description",
                "tags",
                "scenes"
            ]
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Missing key: {key}")

            if len(data["scenes"]) < 3:
                raise ValueError("Not enough scenes generated.")

            print("✅ Valid story generated successfully!")
            return data

        except Exception as e:
            print(f"⚠️ Invalid JSON detected: {e}")

    # If all retries fail, raise an error (no fallback story)
    raise RuntimeError("❌ Failed to generate valid JSON after multiple attempts.")
