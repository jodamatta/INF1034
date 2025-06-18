import sys
import pygame
from typing import Any


FONT_BIG = pygame.font.Font(None, 64)
FONT_MID = pygame.font.Font(None, 48)
FONT_SMALL = pygame.font.Font(None, 32)

from core.level import load_level
from core.player import Spaceship
from core.bullet import Bullet
from settings import WIDTH, HEIGHT


class StateManager:
    def __init__(self, first_id: str, first_data: Any = None):
        self.state = None
        self._registry: dict[str, type[BaseState]] = {}
        for cls in (BootState, PlayState, WinState, LoseState, FinishedState):
            self._registry[cls.id] = cls
        self.change(first_id, first_data)

    def handle_event(self, e): self.state.handle_event(e)

    def update(self, dt): self.state.update(dt)

    def draw(self, surf): self.state.draw(surf)

    def change(self, state_id: str, data: Any = None):
        cls = self._registry[state_id]
        self.state = cls(self, data)


class BaseState:
    id: str = "BASE"

    def __init__(self, mgr: StateManager, data: Any = None):
        self.mgr = mgr
        self.enter(data)

    def enter(self, data): pass

    def handle_event(self, e): pass

    def update(self, dt): pass

    def draw(self, surf): pass


class BootState(BaseState):
    id = "BOOT"

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
            self.mgr.change("PLAY", {"level": "1.json"})

    def draw(self, surf):
        surf.fill("black")
        txt = FONT_MID.render("ENTER para começar", True, "white")
        surf.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))


class PlayState(BaseState):
    id = "PLAY"

    def __init__(self, mgr: StateManager, data: Any = None):
        self.bullets = None
        self.next_lvl = None
        self.targets = None
        self.ship = None
        self.bg = None
        self.lvl_file = None
        super().__init__(mgr, data)

    def enter(self, data):
        self.lvl_file = data["level"]
        self.bg, self.targets, self.next_lvl = load_level(self.lvl_file)
        self.ship, self.bullets = Spaceship(), []

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            self.bullets.append(Bullet(self.ship.rect.centerx, self.ship.rect.top))

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.ship.update(keys)
        for b in self.bullets: b.update()

        for b in self.bullets:
            for t in self.targets:
                if not t.dead and b.rect.colliderect(t.rect):
                    t.hit()
                    b.active = False
        self.bullets = [b for b in self.bullets if b.active]

        if all(t.dead for t in self.targets):
            self.mgr.change("WIN", {"next": self.next_lvl})

        #    self.mgr.change("LOSE", {"level": self.lvl_file})

    def draw(self, surf):
        surf.blit(self.bg, (0, 0))
        self.ship.draw(surf)
        for t in self.targets: t.draw(surf)
        for b in self.bullets: b.draw(surf)


class WinState(BaseState):
    id = "WIN"

    def __init__(self, mgr: StateManager, data: Any = None):
        self.next_lvl = None
        super().__init__(mgr, data)

    def enter(self, data):
        self.next_lvl = data["next"]

    def handle_event(self, e):
        if e.type != pygame.KEYDOWN: return
        if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            if self.next_lvl:
                self.mgr.change("PLAY", {"level": self.next_lvl})
            else:
                self.mgr.change("FIN")
        elif e.key in (pygame.K_ESCAPE, pygame.K_q):
            pygame.quit()
            sys.exit()

    def draw(self, surf):
        surf.fill("black")
        surf.blit(FONT_BIG.render("Você venceu!", True, "white"), (WIDTH // 2 - 150, HEIGHT // 2 - 40))
        surf.blit(FONT_SMALL.render("ENTER = continuar  ESC = sair", True, "white"),
                  (WIDTH // 2 - 170, HEIGHT // 2 + 20))


class LoseState(BaseState):
    id = "LOSE"

    def __init__(self, mgr: StateManager, data: Any = None):
        self.lvl_file = None
        super().__init__(mgr, data)

    def enter(self, data):
        self.lvl_file = data["level"]

    def handle_event(self, e):
        if e.type != pygame.KEYDOWN: return
        if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_r):
            self.mgr.change("PLAY", {"level": self.lvl_file})
        elif e.key in (pygame.K_ESCAPE, pygame.K_q):
            pygame.quit()
            sys.exit()

    def draw(self, surf):
        surf.fill("black")
        surf.blit(FONT_BIG.render("Você perdeu!", True, "white"), (WIDTH // 2 - 160, HEIGHT // 2 - 40))
        surf.blit(FONT_SMALL.render("ENTER/R = de novo  ESC = sair", True, "white"),
                  (WIDTH // 2 - 210, HEIGHT // 2 + 20))


class FinishedState(BaseState):
    id = "FIN"

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            pygame.quit()
            sys.exit()

    def draw(self, surf):
        surf.fill("black")
        txt = FONT_MID.render("Jogo completo! 👍", True, "white")
        surf.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
