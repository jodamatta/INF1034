from core.assets import ACTIVE_TARGET, DESTROYED_TGT

class Target:
    def __init__(self, x, y, movement=None):
        self.image = ACTIVE_TARGET
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dead = False

        self.movement = movement
        if movement:
            self.start = movement.get("start", (x, y))
            self.end   = movement.get("end", (x, y))
            self.speed = movement.get("speed", 0.01) 
            self.progress = 0.0
            self.direction = 1  # 1 indo pro fim e -1 indo pro comeco

    def hit(self):
        if not self.dead:
            self.dead = True
            self.image = DESTROYED_TGT

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def update(self):
        if self.dead or not self.movement:
            return

        self.progress += self.direction * self.speed

        if self.progress >= 1:
            self.progress = 1
            self.direction = -1
        elif self.progress <= 0:
            self.progress = 0
            self.direction = 1

        x = self.lerp(self.start[0], self.end[0], self.progress)
        y = self.lerp(self.start[1], self.end[1], self.progress)
        self.rect.topleft = (x, y)

    @staticmethod
    def lerp(a, b, t):
        return a + (b - a) * t
