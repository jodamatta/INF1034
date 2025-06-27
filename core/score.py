import json
import os
import time

SCORES_FILE = "scores.json"
MAX_SCORES  = 10

def load_scores() -> list[dict]:
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r") as f:
            return json.load(f)
    return []

def save_score(name: str, score: int) -> list[dict]:
    scores = load_scores()
    scores.append({"name": name[:10], "score": score, "ts": time.time()})
    scores = sorted(scores, key=lambda s: -s["score"])[:MAX_SCORES]
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)
    return scores

class ScoreManager:
    not_used_bullets = 0

    @classmethod
    def get_score(cls, remaining_hp):
        print(remaining_hp)
        print(cls.not_used_bullets)
        return remaining_hp * 100 + cls.not_used_bullets * 10

