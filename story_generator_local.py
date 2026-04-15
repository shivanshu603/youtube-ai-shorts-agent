import json
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

MODEL_REPO = "TheBloke/Phi-3-mini-4k-instruct-GGUF"
MODEL_FILE = "phi-3-mini-4k-instruct.Q4_K_M.gguf"

def load_model():
    model_path = hf_hub_download(
        repo_id=MODEL_REPO,
        filename=MODEL_FILE
    )
    return Llama(
        model_path=model_path,
        n_ctx=4096,
        n_threads=4
    )

def generate_story():
    llm = load_model()

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

    output = llm(
        prompt,
        max_tokens=800,
        temperature=0.8,
        stop=["</s>"]
    )

    text = output["choices"][0]["text"]

    # Extract JSON
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == -1:
        raise ValueError("Failed to parse JSON from model output.")

    return json.loads(text[start:end])
