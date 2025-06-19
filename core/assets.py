import pygame, pathlib
from settings import WIDTH, HEIGHT

TILE = 8
SHIP_SCALE = 8
TARGET_SCALE = 8
BULLET_SCALE = 6
HEART_SCALE = 7

ROOT = pathlib.Path(__file__).parents[1] / "assets" / "SpaceShooterAssets"

def load_img(sheet, rect, scale):
    surf = pygame.image.load(ROOT / sheet).convert_alpha()
    x, y, w, h = rect
    return pygame.transform.scale(surf.subsurface((x, y, w, h)),
                                  (w*scale, h*scale))

def load_full_img(filename, scale):
    img = pygame.image.load(ROOT / filename).convert_alpha()
    return pygame.transform.scale(img, (img.get_width()*scale, img.get_height()*scale))

def load_bg():
    bg = pygame.image.load(ROOT / "background.png").convert()
    return pygame.transform.scale(bg, (WIDTH, HEIGHT))


SHIP_LEFT  = load_img("SpaceShooterAssetPack_Ships.png", (0, 8, 8, 8),  SHIP_SCALE)
SHIP_IDLE  = load_img("SpaceShooterAssetPack_Ships.png", (8, 8, 8, 8),  SHIP_SCALE)
SHIP_RIGHT = load_img("SpaceShooterAssetPack_Ships.png", (16, 8, 8, 8), SHIP_SCALE)


ACTIVE_TARGET  = load_full_img("target_alive.png",  TARGET_SCALE)
DESTROYED_TGT  = load_full_img("target_dead.png", TARGET_SCALE)
BULLET_SPRITE  = load_full_img("projectile.png", BULLET_SCALE)
HEART = load_full_img("heart.png", HEART_SCALE)