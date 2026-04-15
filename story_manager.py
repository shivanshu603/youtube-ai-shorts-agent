import json
import os

STATE_FILE = "data/story_state.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"story_number": 1, "episode": 1}

    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def get_next_episode():
    state = load_state()
    story_no = state["story_number"]
    episode_no = state["episode"]

    # Update for next run
    state["episode"] += 1
    if state["episode"] > 5:
        state["story_number"] += 1
        state["episode"] = 1

    save_state(state)
    return story_no, episode_no
