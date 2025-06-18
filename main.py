import pygame, sys
from settings import WIDTH, HEIGHT, FPS

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
clock  = pygame.time.Clock()

from core.states import StateManager
mgr = StateManager("BOOT")

running = True
while running:
    dt = clock.tick(FPS) / 1000
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        else:
            mgr.handle_event(e)

    mgr.update(dt)
    mgr.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
