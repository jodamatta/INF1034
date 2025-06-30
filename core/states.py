import sys
import pygame
from typing import Any

from core.assets import load_bg, HEART
from core.level import Level, LevelManager
from core.player import Spaceship
from core.bullet import Bullet
from core.powerup import PowerUp
from core.score import save_score, load_scores, ScoreManager
from settings import WIDTH, HEIGHT

FONT_BIG = pygame.font.Font(None, 64)
FONT_MID = pygame.font.Font(None, 48)
FONT_SMALL = pygame.font.Font(None, 32)
BACKGROUND = load_bg()
STARTING_LEVEL = 0

level_manager = LevelManager()


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

    collected_hp_levels: set[int] = set()

    def __init__(self, mgr: StateManager, data: Any = None):
        self.bullets: list[Bullet] = []
        self.powerups: list[PowerUp] = []
        self.ship: Spaceship | None = None
        self.lvl: Level | None = None
        self.hp: int = 3
        self.bullet_speed: int = 16
        super().__init__(mgr, data)

    def enter(self, data):
        self.hp = data.get("hp", 3)
        self.bullet_speed = data.get("bullet_speed", 16)
        self.lvl = level_manager.get_level(data["level"])
        self.ship = Spaceship()
        self.bullets = []
        self.powerups = [
            p for p in self.lvl.powerups
            if not (p.kind == "hp" and self.lvl.idx in PlayState.collected_hp_levels)
        ]

    def handle_event(self, e):
        if e.type != pygame.KEYDOWN:
            return

        if e.key == pygame.K_p:
            self.lvl.ammo = max(self.lvl.ammo - len(self.lvl.targets), 0)
            self.advance()
            return

        if e.key == pygame.K_SPACE:
            if self.lvl.ammo:
                self.bullets.append(Bullet(self.ship.rect.centerx, self.ship.rect.top, speed=self.bullet_speed))
                self.lvl.ammo -= 1

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.ship.update(keys)

        for t in self.lvl.targets:
            t.update() 

        for b in self.bullets:
            b.update()

        for p in self.powerups:
            p.update()

        for b in self.bullets:
            for t in self.lvl.targets:
                if b.rect.colliderect(t.rect):
                    if not t.dead:
                        t.hit()
                    b.active = False

        for b in self.bullets:
            if not b.active:
                continue
            for p in self.powerups:
                if not p.collected and b.rect.colliderect(p.rect):
                    self.apply_power_up(p.kind, p.value)
                    p.collect()
                    b.active = False

        self.bullets = [b for b in self.bullets if b.active]

        if self.lvl.ammo == 0 and len(self.bullets) == 0:
            self.hp -= 1
            if self.hp >= 0:
                self.mgr.change("LOSE", {"level": self.lvl.idx, "hp": self.hp})
            else:
                self.mgr.change("GLOBAL_LOSE", {"level": self.lvl.idx})

        if all(t.dead for t in self.lvl.targets):
            self.advance()
    def advance(self):
        ScoreManager.not_used_bullets += self.lvl.ammo
        if self.lvl.idx + 1 < level_manager.count:
            self.mgr.change("WIN", {"next": self.lvl.idx + 1, "hp": self.hp})
        else:
            self.mgr.change("FIN", {"score": ScoreManager.get_score(self.hp)})

    def draw(self, surf):
        surf.blit(BACKGROUND, (0, 0))
        write_centered(surf, FONT_MID, f"fase {self.lvl.idx + 1}/{level_manager.count}", 10)
        self.ship.draw(surf)
        for t in self.lvl.targets: t.draw(surf)
        for p in self.powerups: p.draw(surf)
        for b in self.bullets: b.draw(surf)
        surf.blit(FONT_MID.render(f"x{self.lvl.ammo}", True, "YELLOW"),
                  (25, HEIGHT - 64))
        for i in range(self.hp):
            surf.blit(HEART, (WIDTH - 15 - (i+1) * 50, HEIGHT - 68))

    def apply_power_up(self, kind: str, value: int):
        match kind:
            case "hp":
                if self.lvl.idx not in PlayState.collected_hp_levels:
                    PlayState.collected_hp_levels.add(self.lvl.idx)
                self.hp = min(self.hp + value, 5)
            case "ammo":
                self.lvl.ammo += value
            case "speed":
                self.bullet_speed += value * 2

class WinState(BaseState):
    id = "WIN"

    def __init__(self, mgr: StateManager, data: Any = None):
        self.next_lvl: int | None = None
        self.hp: int = 3
        super().__init__(mgr, data)

    def enter(self, data):
        self.next_lvl = data["next"]
        self.hp = data.get("hp", 3)

    def handle_event(self, e):
        if e.type != pygame.KEYDOWN: return
        
        if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.mgr.change("PLAY", {"level": self.next_lvl, "hp": self.hp})
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
        self.lvl_file: int | None = None
        self.nxt_hp: int = 3
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

    def __init__(self, mgr: StateManager, data: Any = None):
        self.score: int = 0
        self.name: str = ""
        self.saved: bool = False
        self.scores: list[dict] = []
        super().__init__(mgr, data)

    def enter(self, data: dict):
        self.score  = data.get("score", 0)
        self.scores = load_scores()

    def handle_event(self, e):
        if e.type != pygame.KEYDOWN:
            return

        if self.saved:
            if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                ScoreManager.not_used_bullets = 0
                self.mgr.change("PLAY", {"level": STARTING_LEVEL})
            elif e.key in (pygame.K_ESCAPE, pygame.K_q):
                pygame.quit(); sys.exit()
            return

        if e.key == pygame.K_BACKSPACE:
            self.name = self.name[:-1]
        elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.scores = save_score(self.name or "ANON", self.score)
            self.saved  = True
        elif len(self.name) < 10 and e.unicode.isprintable():
            self.name += e.unicode.upper()

    def draw(self, surf):
        surf.fill("black")
        y = HEIGHT // 2 - 180
        write_centered(surf, FONT_BIG, f"Score: {self.score}", y); y += 70

        if not self.saved:
            write_centered(surf, FONT_MID, "Digite seu nome:", y); y += 50
            write_centered(surf, FONT_MID, self.name + "_", y)
        else:
            write_centered(surf, FONT_MID, "LEADERBOARD", y); y += 50
            for i, s in enumerate(self.scores, 1):
                txt = f"{i:2d}. {s['name']:<10} {s['score']:>5}"
                write_centered(surf, FONT_SMALL, txt, y); y += 35
            y += 40
            write_centered(surf, FONT_SMALL, "ENTER = jogar de novo   |   ESC = sair", y)
