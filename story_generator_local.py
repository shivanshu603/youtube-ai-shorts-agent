import json
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

# Download the Mistral model
MODEL_PATH = hf_hub_download(
    repo_id="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
    filename="mistral-7b-instruct-v0.2.Q4_K_M.gguf"
)

# Load the model
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,
    n_threads=4,
    verbose=False
)

# JSON schema to strictly enforce structure
JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "story_title": {"type": "string"},
        "youtube_title": {"type": "string"},
        "description": {"type": "string"},
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 3
        },
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
        }
    },
    "required": [
        "story_title",
        "youtube_title",
        "description",
        "tags",
        "scenes"
    ]
}

def generate_story(max_retries: int = 5):
    print("🧠 Generating a new story...")

    prompt = (
        "Create a completely new and original YouTube Shorts story. "
        "Respond ONLY with valid JSON following the provided schema."
    )

    for attempt in range(1, max_retries + 1):
        print(f"🔄 Attempt {attempt}/{max_retries}...")

        try:
            response = llm.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a creative storyteller."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                top_p=0.95,
                response_format={
                    "type": "json_object",
                    "schema": JSON_SCHEMA
                },
                max_tokens=1500
            )

            content = response["choices"][0]["message"]["content"]
            data = json.loads(content)

            # Final validation
            if len(data["scenes"]) != 5:
                raise ValueError("Invalid number of scenes.")

            print("✅ Valid story generated successfully!")
            return data

        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")

    raise RuntimeError("❌ Failed to generate valid JSON after multiple attempts.")
