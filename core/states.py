import sys
import pygame
from typing import Any

from core.assets import load_bg, HEART
from core.level import load_level, Level
from core.player import Spaceship
from core.bullet import Bullet
from settings import WIDTH, HEIGHT

FONT_BIG = pygame.font.Font(None, 64)
FONT_MID = pygame.font.Font(None, 48)
FONT_SMALL = pygame.font.Font(None, 32)
STARTING_LEVEL = "1.json"
BACKGROUND = load_bg()

def write_centered(surf, font, text, y, color="white"):
    img = font.render(text, True, color)
    rect = img.get_rect(midtop=(surf.get_width() // 2, y))
    surf.blit(img, rect)
    return rect


class StateManager:
    def __init__(self, first_id: str, first_data: Any = None):
        self.state = None
        self._registry: dict[str, type[BaseState]] = {}
        for cls in (BootState, PlayState, WinState, LoseState, GlobalLoseState, FinishedState):
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
            self.mgr.change("PLAY", {"level": STARTING_LEVEL})

    def draw(self, surf):
        surf.fill("black")
        write_centered(surf, FONT_MID, "ENTER para começar", HEIGHT // 2 - 150)

class PlayState(BaseState):
    id = "PLAY"

    def __init__(self, mgr: StateManager, data: Any = None):
        self.bullets: list[Bullet] | None = None
        self.ship: Spaceship | None = None
        self.lvl_file: str | None = None
        self.lvl: Level | None = None
        self.hp: int | None = None
        super().__init__(mgr, data)

    def enter(self, data):
        self.lvl_file = data["level"]
        self.hp = data.get("hp", 3)
        self.lvl = load_level(self.lvl_file)
        self.ship, self.bullets = Spaceship(), []

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            if self.lvl.ammo:
                self.bullets.append(Bullet(self.ship.rect.centerx, self.ship.rect.top))
                self.lvl.ammo -= 1

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.ship.update(keys)
        for b in self.bullets: b.update()

        for b in self.bullets:
            for t in self.lvl.targets:
                if b.rect.colliderect(t.rect):
                    t.hit()
                    b.active = False
        self.bullets = [b for b in self.bullets if b.active]

        if self.lvl.ammo == 0 and len(self.bullets) == 0:
            self.hp -= 1
            if self.hp:
                self.mgr.change("LOSE", {"level": self.lvl_file, "hp": self.hp})
            else:
                #perde global
                self.mgr.change("GLOBAL_LOSE", {"level": self.lvl_file})

        if all(t.dead for t in self.lvl.targets):
            if self.lvl.next:
                self.mgr.change("WIN", {"next": self.lvl.next})
            else:
                self.mgr.change("FIN")

    def draw(self, surf):
        surf.blit(BACKGROUND, (0, 0))
        self.ship.draw(surf)
        for t in self.lvl.targets: t.draw(surf)
        for b in self.bullets: b.draw(surf)
        surf.blit(FONT_MID.render(f"x{self.lvl.ammo}", True, "YELLOW"),
                  (25, HEIGHT - 64))
        for i in range(self.hp):
            surf.blit(HEART, (WIDTH - 15 - (i+1) * 50, HEIGHT - 68))

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
            self.mgr.change("PLAY", {"level": self.next_lvl})
        elif e.key in (pygame.K_ESCAPE, pygame.K_q):
            pygame.quit()
            sys.exit()

    def draw(self, surf):
        surf.fill("black")
        write_centered(surf, FONT_BIG, "Você venceu!", HEIGHT // 2 - 150)
        write_centered(surf, FONT_SMALL, "ENTER = continuar | ESC = sair", HEIGHT // 2 - 100)


class LoseState(BaseState):
    id = "LOSE"

    def __init__(self, mgr: StateManager, data: Any = None):
        self.lvl_file = None
        self.nxt_hp = None
        super().__init__(mgr, data)

    def enter(self, data):
        self.lvl_file = data["level"]
        self.nxt_hp = data["hp"]

    def handle_event(self, e):
        if e.type != pygame.KEYDOWN: return
        if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_r):
            self.mgr.change("PLAY", {"level": self.lvl_file, "hp": self.nxt_hp})
        elif e.key in (pygame.K_ESCAPE, pygame.K_q):
            pygame.quit()
            sys.exit()

    def draw(self, surf):
        surf.fill("black")
        write_centered(surf, FONT_BIG, "Você perdeu!", HEIGHT // 2 - 150)
        write_centered(surf, FONT_SMALL, "ENTER = rejogar fase | ESC = sair", HEIGHT // 2 - 100)


class GlobalLoseState(BaseState):
    id = "GLOBAL_LOSE"

    def __init__(self, mgr: StateManager, data: Any = None):
        self.lvl_file = None
        super().__init__(mgr, data)

    def enter(self, data):
        self.lvl_file = data["level"]

    def handle_event(self, e):
        if e.type != pygame.KEYDOWN: return
        if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_r):
            self.mgr.change("PLAY", {"level": STARTING_LEVEL})
        elif e.key in (pygame.K_ESCAPE, pygame.K_q):
            pygame.quit()
            sys.exit()

    def draw(self, surf):
        surf.fill("black")
        write_centered(surf, FONT_BIG, "Sem vidas!", HEIGHT // 2 - 150)
        write_centered(surf, FONT_SMALL, "ENTER = recomeçar | ESC = sair", HEIGHT // 2 - 100)


class FinishedState(BaseState):
    id = "FIN"

    def handle_event(self, e):
        if e.type != pygame.KEYDOWN: return
        if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_r):
            self.mgr.change("PLAY", {"level": STARTING_LEVEL})
        elif e.key in (pygame.K_ESCAPE, pygame.K_q):
            pygame.quit()
            sys.exit()

    def draw(self, surf):
        surf.fill("black")
        write_centered(surf, FONT_BIG, "Parabens!", HEIGHT // 2 - 150)
        write_centered(surf, FONT_SMALL, "ENTER = jogar novamente | ESC = sair", HEIGHT // 2 - 100)

