from core.assets import ACTIVE_TARGET, DESTROYED_TGT

class Target:
    def __init__(self, x, y):
        self.image = ACTIVE_TARGET
        self.rect  = self.image.get_rect(topleft=(x, y))
        self.dead  = False

    def hit(self):
        if not self.dead:
            self.dead = True
            self.image = DESTROYED_TGT

    def draw(self, surf): surf.blit(self.image, self.rect)
    def update(self):     pass
