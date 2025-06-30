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

base_cannon = load_img("SpaceShooterAssetPack_Ships.png", (56,40,8,8), SHIP_SCALE) 

CANNON_IMGS = {
    "down": base_cannon,
    "left": pygame.transform.rotate(base_cannon, -90),
    "up": pygame.transform.rotate(base_cannon, 180),
    "right": pygame.transform.rotate(base_cannon, 90),
}

base_destroyed_cannon = load_img("SpaceShooterAssetPack_Ships.png", (64, 16, 8, 8), SHIP_SCALE)

DESTROYED_CANNON_IMGS = {
    "down": base_destroyed_cannon,
    "left": pygame.transform.rotate(base_destroyed_cannon, -90),
    "up": pygame.transform.rotate(base_destroyed_cannon, 180),
    "right": pygame.transform.rotate(base_destroyed_cannon, 90),
}

BULLET_IMGS = {
    "up": load_full_img("projectile_up.png", BULLET_SCALE),
    "down": load_full_img("projectile_down.png", BULLET_SCALE), 
    "left": load_full_img("projectile_left.png", BULLET_SCALE), 
    "right": load_full_img("projectile_right.png", BULLET_SCALE) 
}


ACTIVE_TARGET  = load_full_img("target_alive.png",  TARGET_SCALE)
DESTROYED_TGT  = load_full_img("target_dead.png", TARGET_SCALE)
HEART = load_full_img("heart.png", HEART_SCALE)