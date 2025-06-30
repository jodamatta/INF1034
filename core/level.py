import json, pathlib

from dataclasses import dataclass
from core.target import Target
from core.powerup import PowerUp
from core.cannon import Cannon

DATA = pathlib.Path(__file__).parents[1] / "levels"

@dataclass
class Level:
    idx: int
    targets: list
    powerups: list
    ammo: int
    cannons: list

def load_level(name, idx):
    cfg = json.loads((DATA/name).read_text())
    targets = [Target(t["x"], t["y"], t.get("movement")) for t in cfg["targets"]]
    cannons = [Cannon(c["x"], c["y"], c.get("direction", "up")) for c in cfg.get("cannons", [])]

    powerups_cfg = cfg.get("powerups", [])
    powerups = [
        PowerUp(p["type"], p["x"], p["y"], p.get("value", 1), p.get("movement"))
        for p in powerups_cfg
    ]

    return Level(idx=idx, cannons = cannons, targets=targets, powerups=powerups, ammo=cfg.get("ammo", 0))

class LevelManager:
    def __init__(self, dir_path: pathlib.Path = DATA):
        self.files = sorted(p for p in dir_path.iterdir() if p.suffix == ".json")

    def __len__(self): return len(self.files)
    @property
    def count(self):  return len(self.files)

    def get_level(self, idx: int) -> Level:
        if not (0 <= idx < len(self.files)):
            raise IndexError("level index out of range")
        return load_level(self.files[idx].name, idx)
