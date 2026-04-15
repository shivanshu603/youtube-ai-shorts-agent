import os
import json
from datetime import datetime
from llama_cpp import Llama, LlamaGrammar
from huggingface_hub import hf_hub_download

# -------------------------------
# Model Configuration
# -------------------------------
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


# Load the model once
llm = load_model()

# -------------------------------
# JSON Schema for Structured Output
# -------------------------------
json_schema = {
    "type": "object",
    "properties": {
        "story_title": {"type": "string"},
        "scenes": {
            "type": "array",
            "minItems": 5,
            "maxItems": 5,
            "items": {
                "type": "object",
                "properties": {
                    "narration": {"type": "string"},
                    "image_prompt": {"type": "string"}
                },
                "required": ["narration", "image_prompt"]
            }
        },
        "youtube_title": {"type": "string"},
        "description": {"type": "string"},
        "tags": {
            "type": "array",
            "minItems": 3,
            "maxItems": 5,
            "items": {"type": "string"}
        }
    },
    "required": [
        "story_title",
        "scenes",
        "youtube_title",
        "description",
        "tags"
    ]
}

# ✅ Convert dictionary to JSON string
json_grammar = LlamaGrammar.from_json_schema(json.dumps(json_schema))


def generate_story():
    """
    Generate a brand-new, unique Hindi moral story
    with guaranteed valid JSON output.
    """
    unique_seed = datetime.utcnow().isoformat()

    prompt = f"""
You are a creative storyteller for YouTube Shorts.

Create a completely new and unique Hindi moral story using this seed: {unique_seed}

Requirements:
- Exactly 5 scenes.
- Each scene must include "narration" and "image_prompt".
- The final scene should clearly present a moral lesson.
- Use simple Hindi suitable for all ages.
- Provide an engaging YouTube title, description, and 3-5 relevant tags.
- Respond ONLY with valid JSON.
"""

    print("🧠 Generating a new story...")

    response = llm(
        prompt,
        max_tokens=800,
        temperature=0.9,
        top_p=0.95,
        grammar=json_grammar
    )

    text = response["choices"][0]["text"].strip()
    print("✅ Generated JSON:\n", text)

    # Parse JSON safely
    data = json.loads(text)

    # Final validation
    if len(data.get("scenes", [])) != 5:
        raise ValueError("Generated story does not contain exactly 5 scenes.")

    return data
