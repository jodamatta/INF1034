from core.assets import BULLET_IMGS
from settings import WIDTH, HEIGHT

class Bullet:
    def __init__(self, x, y, dx=0, dy=-1, speed = 16, source = "player"): 
        self.speed = speed
        self.dx, self.dy = dx, dy
        self.active = True
        self.source = source

        if dx == 0 and dy < 0:
            self.direction = "up"
        elif dx == 0 and dy > 0:
            self.direction = "down"
        elif dx < 0 and dy == 0:
            self.direction = "left"
        elif dx > 0 and dy == 0:
            self.direction = "right"
        else:
            self.direction = "up" 

        self.image = BULLET_IMGS[self.direction]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed 

        if (self.rect.right < 0 or self.rect.left > WIDTH or
            self.rect.bottom < 0 or self.rect.top > HEIGHT):
            self.active = False

    def draw(self, surf):
        surf.blit(self.image, self.rect)

