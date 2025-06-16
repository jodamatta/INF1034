import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 512, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
clock = pygame.time.Clock()
FPS = 30

ships_sprite_sheet = pygame.image.load("SpaceShooterAssetPack/SpaceShooterAssets/SpaceShooterAssetPack_Ships.png").convert_alpha()
background_sheet = pygame.image.load("SpaceShooterAssetPack/SpaceShooterAssets/SpaceShooterAssetPack_Backgrounds.png").convert()
projectile_sheet = pygame.image.load("SpaceShooterAssetPack/SpaceShooterAssets/SpaceShooterAssetPack_Projectiles.png").convert_alpha()

TILE_SIZE = 8

SHIP_SCALE = 8
SHIP_SIZE = (TILE_SIZE * SHIP_SCALE, TILE_SIZE * SHIP_SCALE)
SHIP_LEFT = pygame.transform.scale(ships_sprite_sheet.subsurface((0, 8, 8, 8)), SHIP_SIZE)
SHIP_IDLE = pygame.transform.scale(ships_sprite_sheet.subsurface((8, 8, 8, 8)), SHIP_SIZE)
SHIP_RIGHT = pygame.transform.scale(ships_sprite_sheet.subsurface((16, 8, 8, 8)), SHIP_SIZE)

BG_WIDTH, BG_HEIGHT = 128, 128  
BG_RECT = pygame.Rect(BG_WIDTH, 0, BG_WIDTH, BG_HEIGHT)
background = background_sheet.subsurface(BG_RECT)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

TARGET_SCALE = 8
TARGET_SIZE = TILE_SIZE * TARGET_SCALE

rect = pygame.Rect(0 * TILE_SIZE, 4 * TILE_SIZE, TILE_SIZE, TILE_SIZE)
ACTIVE_TARGET_SPRITE = pygame.transform.scale(projectile_sheet.subsurface(rect), (TARGET_SIZE, TARGET_SIZE))
rect = pygame.Rect(4 * TILE_SIZE, 3 * TILE_SIZE, TILE_SIZE, TILE_SIZE)
DESTROYED_TARGET_SPRITE = pygame.transform.scale(projectile_sheet.subsurface(rect), (TARGET_SIZE, TARGET_SIZE))

BULLET_SCALE = 6
BULLET_SIZE = (TILE_SIZE * BULLET_SCALE, TILE_SIZE * BULLET_SCALE)
BULLET_SPRITE = pygame.transform.scale(projectile_sheet.subsurface((16, 0, TILE_SIZE, TILE_SIZE)), BULLET_SIZE)

class Spaceship:
    def __init__(self):
        self.image = SHIP_IDLE
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 40))
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

        self.rect.clamp_ip(screen.get_rect())

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Target:
    def __init__(self, x, y):
        self.image = ACTIVE_TARGET_SPRITE
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_destroyed = False

    def hit(self):
        if not self.is_destroyed:
            self.is_destroyed = True
            self.image = DESTROYED_TARGET_SPRITE

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        pass  # movimento

class Bullet:
    def __init__(self, x, y, speed=16):
        self.image = BULLET_SPRITE
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.active = True

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.active = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

ship = Spaceship()
targets = [
    Target(100, 100),
    Target(200, 100),
    Target(300, 100)
]
bullets = []

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = ship.rect.centerx 
                bullet_y = ship.rect.top
                bullets.append(Bullet(bullet_x, bullet_y))

    ship.update(keys)

    screen.blit(background, (0, 0))
    ship.draw(screen)
    for target in targets:
        target.draw(screen)

    for bullet in bullets[:]:  
        bullet.update()
        bullet.draw(screen)

        for target in targets:
            if not target.is_destroyed and bullet.rect.colliderect(target.rect):
                target.hit()
                bullet.active = False
                break  

    bullets = [b for b in bullets if b.active]

    pygame.display.flip()
    clock.tick(FPS)
