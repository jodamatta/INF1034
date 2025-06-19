import pygame
from settings import WIDTH, HEIGHT
from core.assets import SHIP_LEFT, SHIP_IDLE, SHIP_RIGHT

class Spaceship:
    def __init__(self):
        self.image = SHIP_IDLE
        self.rect = self.image.get_rect(midbottom=(WIDTH//2, HEIGHT-100))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.image = SHIP_LEFT
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.image = SHIP_RIGHT
        else:
            self.image = SHIP_IDLE
        self.rect.clamp_ip(pygame.Rect(0,0,WIDTH,HEIGHT))

    def draw(self, surf):
        surf.blit(self.image, self.rect)
