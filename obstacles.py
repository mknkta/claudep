import os
import pygame
from config import GROUND_Y, CEILING_Y

PLATFORM_H = 20

SIZES = {
    "small":  (22, 18),
    "medium": (34, 28),
    "large":  (46, 38),
}

# Tamanhos dos espinhos de teto (mais altos para dificultar a nave)
CEILING_SIZES = {
    "small":  (28, 70),
    "medium": (40, 110),
    "large":  (52, 150),
}

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


# ── Espinho do chão ───────────────────────────────────────────────────
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
            w - ix * 2, h - iy,
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
        pts = [(x + w//2, y), (x, y+h), (x+w, y+h)]
        pygame.draw.polygon(screen, self.COLOR,      pts)
        pygame.draw.polygon(screen, self.COLOR_EDGE, pts, width=2)


# ── Espinho do teto (pendurado, ponta pra baixo) ─────────────────────
class CeilingSpike:
    COLOR      = (255,  80,  30)
    COLOR_EDGE = (255, 180,  80)

    def __init__(self, x: float, size: str = "medium"):
        w, h = CEILING_SIZES.get(size, CEILING_SIZES["medium"])
        self._w, self._h = w, h
        self.rect = pygame.Rect(int(x), CEILING_Y, w, h)
        ix = int(w * 0.15)
        # hitbox: toda a altura (a ponta é a parte perigosa)
        self.collision_rect = pygame.Rect(
            self.rect.x + ix, self.rect.y,
            w - ix * 2, h,
        )

    def _sync(self):
        ix = int(self._w * 0.15)
        self.collision_rect.x     = self.rect.x + ix
        self.collision_rect.y     = self.rect.y
        self.collision_rect.width = self._w - ix * 2

    def draw(self, screen):
        x, y, w, h = self.rect
        # triângulo pendurado: base no topo, ponta no fundo
        pts = [
            (x,          y),      # topo esquerdo
            (x + w,      y),      # topo direito
            (x + w // 2, y + h),  # ponta baixo
        ]
        pygame.draw.polygon(screen, self.COLOR,      pts)
        pygame.draw.polygon(screen, self.COLOR_EDGE, pts, width=2)


# ── Plataforma ────────────────────────────────────────────────────────
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


# ── Portal (muda o modo do player) ───────────────────────────────────
class Portal:
    # Cores por modo de destino
    MODE_COLORS = {
        "ship": (0,   200, 255),   # ciano → modo nave
        "cube": (255, 140,   0),   # laranja → modo cubo
    }

    def __init__(self, x: float, target_mode: str):
        self.target_mode = target_mode
        w, h = 28, GROUND_Y - CEILING_Y   # portal ocupa toda a altura jogável
        self._color = self.MODE_COLORS.get(target_mode, (200, 200, 200))
        self.rect           = pygame.Rect(int(x), CEILING_Y, w, h)
        self.collision_rect = self.rect.copy()
        self.triggered      = False

    def _sync(self):
        self.collision_rect.topleft = self.rect.topleft

    def draw(self, screen):
        # anel externo
        pygame.draw.rect(screen, self._color, self.rect, border_radius=14)
        # brilho interno (mais estreito)
        inner = self.rect.inflate(-8, -8)
        pygame.draw.rect(screen, (255, 255, 255), inner, width=2, border_radius=10)
        # ícone central
        cx, cy = self.rect.center
        if self.target_mode == "ship":
            # triângulo (nave)
            pts = [(cx, cy-14), (cx-10, cy+10), (cx+10, cy+10)]
        else:
            # quadrado (cubo)
            pts = [(cx-10, cy-10), (cx+10, cy-10), (cx+10, cy+10), (cx-10, cy+10)]
        pygame.draw.polygon(screen, (255, 255, 255), pts)
