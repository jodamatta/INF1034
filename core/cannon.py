import pygame
from core.assets import CANNON_IMGS, DESTROYED_CANNON_IMGS
from core.bullet import Bullet

DIRECTION_VECTORS = {
    "up":    ( 0, -1),
    "down":  ( 0,  1),
    "left":  (-1,  0),
    "right": ( 1,  0)
}

class Cannon:
    def __init__(self, x, y, direction="up"):
        self.x, self.y = x, y
        self.direction = direction
        self.image = CANNON_IMGS[direction]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.active = True

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def fire(self):
        if not self.active:
            return None
        dx, dy = DIRECTION_VECTORS[self.direction]
        return Bullet(self.rect.centerx, self.rect.centery, dx, dy, source ="cannon")
    
    def hit(self):
        if self.active:
            self.active = False
            self.image = DESTROYED_CANNON_IMGS[self.direction]
