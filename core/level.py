import json, pathlib

from dataclasses import dataclass
from core.target import Target

DATA = pathlib.Path(__file__).parents[1] / "levels"

@dataclass
class Level:
    targets: list
    ammo: int
    next: str | None

def load_level(name):
    cfg = json.loads((DATA/name).read_text())
    targets = [Target(t["x"], t["y"], t.get("movement")) for t in cfg["targets"]]
    return Level(targets=targets, ammo=cfg.get("ammo", 0), next=cfg.get("next"))

