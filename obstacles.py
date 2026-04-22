import os
import pygame
from config import GROUND_Y

PLATFORM_H = 20

# largura, altura por tamanho
SIZES = {
    "small":  (22, 18),
    "medium": (34, 28),
    "large":  (46, 38),
}

# cache de sprites de espinho por tamanho
_spike_cache: dict = {}

def _load_spike_sprite(w, h):
    key = (w, h)
    if key not in _spike_cache:
        for name in ("assets/spike.jpg", "assets/spike.png"):
            if os.path.isfile(name):
                try:
                    img = pygame.image.load(name).convert()
                    _spike_cache[key] = pygame.transform.scale(img, (w, h))
                    return _spike_cache[key]
                except pygame.error:
                    pass
        _spike_cache[key] = None
    return _spike_cache[key]


class Spike:
    COLOR      = (255,  80,  30)
    COLOR_EDGE = (255, 180,  80)

    def __init__(self, x: float, size: str = "medium"):
        w, h = SIZES.get(size, SIZES["medium"])
        self._w, self._h = w, h
        self.rect = pygame.Rect(int(x), GROUND_Y - h, w, h)
        ix, iy = int(w * 0.15), int(h * 0.20)
        self.collision_rect = pygame.Rect(
            self.rect.x + ix, self.rect.y + iy,
            w - ix * 2,       h - iy,
        )
        self._sprite = _load_spike_sprite(w, h)

    def _sync(self):
        ix, iy = int(self._w * 0.15), int(self._h * 0.20)
        self.collision_rect.x = self.rect.x + ix
        self.collision_rect.y = self.rect.y + iy

    def draw(self, screen):
        if self._sprite:
            screen.blit(self._sprite, self.rect); return
        x, y, w, h = self.rect
        pts = [(x + w//2, y), (x, y + h), (x + w, y + h)]
        pygame.draw.polygon(screen, self.COLOR,      pts)
        pygame.draw.polygon(screen, self.COLOR_EDGE, pts, width=2)


class Platform:
    COLOR      = (60, 200, 120)
    COLOR_EDGE = (120, 255, 180)

    def __init__(self, x: float, y: float, width: int = 200):
        self.rect           = pygame.Rect(int(x), int(y), width, PLATFORM_H)
        self.collision_rect = self.rect.copy()

    def _sync(self):
        self.collision_rect.topleft = self.rect.topleft

    def draw(self, screen):
        pygame.draw.rect(screen, self.COLOR,      self.rect, border_radius=4)
        pygame.draw.rect(screen, self.COLOR_EDGE, self.rect, width=2, border_radius=4)
