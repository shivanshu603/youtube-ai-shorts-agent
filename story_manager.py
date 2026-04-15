import json
import os
from config import DATA_DIR

STATE_FILE = os.path.join(DATA_DIR, "state.json")


def get_next_episode():
    if not os.path.exists(STATE_FILE):
        state = {"story_no": 1, "episode_no": 1}
    else:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)

    story_no = state["story_no"]
    episode_no = state["episode_no"]

    # Update for next run
    state["episode_no"] += 1
    if state["episode_no"] > 10:
        state["story_no"] += 1
        state["episode_no"] = 1

    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

    return story_no, episode_no
