from core.assets import BULLET_SPRITE

class Bullet:
    def __init__(self, x, y, speed=16):
        self.image = BULLET_SPRITE
        self.rect  = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.active = True
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0: self.active = False
    def draw(self, surf): surf.blit(self.image, self.rect)
