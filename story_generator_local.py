import json
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

# Public GGUF model
MODEL_REPO = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
MODEL_FILE = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

# Load model once
def load_model():
    model_path = hf_hub_download(
        repo_id=MODEL_REPO,
        filename=MODEL_FILE
    )
    return Llama(
        model_path=model_path,
        n_ctx=2048,
        n_threads=4,
        verbose=False
    )

llm = load_model()

def generate_story():
    prompt = """
    <s>[INST]
    Create a unique and engaging Hindi moral story for a YouTube Shorts video.

    Return ONLY valid JSON in the following format:
    {
      "story_title": "",
      "scenes": [
        {"narration": "", "image_prompt": ""}
      ],
      "youtube_title": "",
      "description": "",
      "tags": []
    }

    Requirements:
    - 5 scenes
    - Each narration should be 1-2 sentences.
    - Include a moral lesson.
    [/INST]
    """

    response = llm(
        prompt,
        max_tokens=800,
        temperature=0.8,
        stop=["</s>"]
    )

    text = response["choices"][0]["text"]

    # Extract JSON safely
    start = text.find("{")
    end = text.rfind("}") + 1

    if start == -1 or end == -1:
        raise ValueError("Failed to parse JSON from model output.")

    return json.loads(text[start:end])
