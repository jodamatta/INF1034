import json, pathlib
from core.target import Target
from core.assets import load_bg

DATA = pathlib.Path(__file__).parents[1] / "levels"

def load_level(name):
    cfg = json.loads((DATA/name).read_text())
    bg_rect = tuple(cfg["background_rect"])
    bg = load_bg(bg_rect)
    targets = [Target(t["x"], t["y"]) for t in cfg["targets"]]
    next_lv = cfg.get("next")
    return bg, targets, next_lv
