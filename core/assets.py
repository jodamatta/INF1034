import pygame, pathlib, os
from settings import TILE, SHIP_SCALE, TARGET_SCALE, BULLET_SCALE, WIDTH, HEIGHT

ROOT = pathlib.Path(__file__).parents[1] / "assets" / "SpaceShooterAssets"

def load_img(sheet, rect, scale):
    surf = pygame.image.load(ROOT / sheet).convert_alpha()
    x, y, w, h = rect
    return pygame.transform.scale(surf.subsurface((x, y, w, h)),
                                  (w*scale, h*scale))

def load_bg(rect=(128, 0, 128, 128)):
    sheet = pygame.image.load(ROOT / "SpaceShooterAssetPack_Backgrounds.png").convert()
    bg = sheet.subsurface(rect)
    return pygame.transform.scale(bg, (WIDTH, HEIGHT))


SHIP_LEFT  = load_img("SpaceShooterAssetPack_Ships.png", (0, 8, 8, 8),  SHIP_SCALE)
SHIP_IDLE  = load_img("SpaceShooterAssetPack_Ships.png", (8, 8, 8, 8),  SHIP_SCALE)
SHIP_RIGHT = load_img("SpaceShooterAssetPack_Ships.png", (16, 8, 8, 8), SHIP_SCALE)


ACTIVE_TARGET  = load_img("SpaceShooterAssetPack_Projectiles.png", (0*TILE,4*TILE, TILE, TILE), TARGET_SCALE)
DESTROYED_TGT  = load_img("SpaceShooterAssetPack_Projectiles.png", (4*TILE,3*TILE, TILE, TILE), TARGET_SCALE)
BULLET_SPRITE  = load_img("SpaceShooterAssetPack_Projectiles.png", (16, 0, TILE, TILE), BULLET_SCALE)
