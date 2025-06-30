import pygame
from core.assets import HEART, BULLET_SPRITE, DESTROYED_TGT

class PowerUp:
    TYPE_SPRITES: dict[str, pygame.Surface] = {
        "hp": HEART,
        "ammo": BULLET_SPRITE,
        "speed": DESTROYED_TGT,
    }

    def __init__(self, kind: str, x: int, y: int, value: int = 1, movement: dict | None = None):
        if kind not in self.TYPE_SPRITES:
            raise ValueError(f"Unknown power-up kind: {kind}")
        self.kind = kind
        self.value = value
        self.image = self.TYPE_SPRITES[kind]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collected = False

        self.movement = movement
        if movement:
            self.start = movement.get("start", (x, y))
            self.end = movement.get("end", (x, y))
            self.speed = movement.get("speed", 0.01)
            self.progress = 0.0
            self.direction = 1

    def update(self):
        if self.collected or not self.movement:
            return
        self.progress += self.direction * self.speed
        if self.progress >= 1:
            self.progress = 1
            self.direction = -1
        elif self.progress <= 0:
            self.progress = 0
            self.direction = 1
        x = self.lerp(self.start[0], self.end[0], self.progress)
        y = self.lerp(self.start[1], self.end[1], self.progress)
        self.rect.topleft = (int(x), int(y))

    def draw(self, surf):
        if not self.collected:
            surf.blit(self.image, self.rect)

    def collect(self):
        self.collected = True

    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        return a + (b - a) * t 