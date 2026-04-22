import pygame
from config import GRAVITY, GROUND_Y

SIZE         = 60
JUMP_IMPULSE = -15
ROT_SPEED    = 6

class Player:
    def __init__(self):
        self.rect = pygame.Rect(150, GROUND_Y - SIZE, SIZE, SIZE)
        self.collision_rect = self.rect.copy()
        self.velocity_y: float = 0.0
        self.on_ground:  bool  = True
        self._angle:     float = 0.0
        self._sprite = self._load()

    def _load(self):
        import os
        for name in ("assets/player.jpg", "assets/player.png"):
            if os.path.isfile(name):
                try:
                    img = pygame.image.load(name).convert_alpha()
                    return pygame.transform.scale(img, (SIZE, SIZE))
                except pygame.error:
                    pass
        # fallback colorido (SRCALPHA para cantos transparentes ao rotacionar)
        s = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
        pygame.draw.rect(s, (100, 80, 220), s.get_rect(), border_radius=4)
        pygame.draw.rect(s, (160, 140, 255), s.get_rect(), width=3, border_radius=4)
        return s

    def update(self, dt):
        self.velocity_y += GRAVITY
        self.rect.y += int(self.velocity_y)
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.velocity_y  = 0.0
            self.on_ground   = True
            self._angle = round(self._angle / 90) * 90
        else:
            self.on_ground = False
            self._angle   += ROT_SPEED

    def jump(self) -> bool:
        if self.on_ground:
            self.velocity_y = JUMP_IMPULSE
            self.on_ground  = False
            return True
        return False

    def draw(self, screen):
        rotated  = pygame.transform.rotate(self._sprite, -self._angle)
        draw_rect = rotated.get_rect(center=self.rect.center)
        screen.blit(rotated, draw_rect)
