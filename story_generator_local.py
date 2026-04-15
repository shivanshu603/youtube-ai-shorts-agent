import json
import re
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

# Download TinyLlama GGUF model
MODEL_PATH = hf_hub_download(
    repo_id="TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
    filename="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
)

# Load the model
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,
    n_threads=4,
    verbose=False
)

def build_prompt():
    return """
<|system|>
You are a professional storyteller who creates engaging YouTube Shorts.
Always return ONLY valid JSON without any explanations or extra text.
</s>
<|user|>
Generate a completely new and original YouTube Shorts story.

Return ONLY valid JSON in this format:

{
  "story_title": "Short engaging title",
  "youtube_title": "Catchy YouTube Shorts title",
  "description": "SEO optimized YouTube description",
  "tags": ["inspiration", "shorts", "story"],
  "scenes": [
    {
      "narration": "1-2 sentence narration",
      "image_prompt": "Detailed visual description"
    },
    {
      "narration": "1-2 sentence narration",
      "image_prompt": "Detailed visual description"
    },
    {
      "narration": "1-2 sentence narration",
      "image_prompt": "Detailed visual description"
    },
    {
      "narration": "1-2 sentence narration",
      "image_prompt": "Detailed visual description"
    },
    {
      "narration": "1-2 sentence narration",
      "image_prompt": "Detailed visual description"
    }
  ]
}
</s>
<|assistant|>
"""

def extract_json(text: str):
    """Extract the first JSON object from text."""
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in the model output.")
    return match.group(0)

def generate_story(max_retries: int = 5):
    print("🧠 Generating a new story...")

    for attempt in range(1, max_retries + 1):
        print(f"🔄 Attempt {attempt}/{max_retries}...")

        response = llm(
            build_prompt(),
            max_tokens=1500,
            temperature=0.9,
            top_p=0.95,
            repeat_penalty=1.1,
            stop=["</s>"]
        )

        text = response["choices"][0]["text"].strip()
        print("🔍 Raw Model Output:\n", text[:500], "...\n")

        try:
            json_text = extract_json(text)
            data = json.loads(json_text)

            # Validate required fields
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

            if len(data["scenes"]) < 5:
                raise ValueError("Not enough scenes generated.")

            print("✅ Valid story generated successfully!")
            return data

        except Exception as e:
            print(f"⚠️ Invalid JSON detected: {e}")

    raise RuntimeError("❌ Failed to generate valid JSON after multiple attempts.")
