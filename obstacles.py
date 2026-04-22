import math
import os
import random
import pygame
from config import GROUND_Y, CEILING_Y

PLATFORM_H = 20

SIZES = {
    "small":  (22, 18),
    "medium": (34, 28),
    "large":  (46, 38),
}
CEILING_SIZES = {
    "small":  (28,  70),
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
            self.rect.x + ix, self.rect.y + iy, w - ix * 2, h - iy)
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


# ── Espinho do teto ───────────────────────────────────────────────────
class CeilingSpike:
    COLOR      = (255,  80,  30)
    COLOR_EDGE = (255, 180,  80)

    def __init__(self, x: float, size: str = "medium"):
        w, h = CEILING_SIZES.get(size, CEILING_SIZES["medium"])
        self._w, self._h = w, h
        self.rect = pygame.Rect(int(x), CEILING_Y, w, h)
        ix = int(w * 0.15)
        self.collision_rect = pygame.Rect(self.rect.x + ix, self.rect.y, w - ix * 2, h)

    def _sync(self):
        ix = int(self._w * 0.15)
        self.collision_rect.x     = self.rect.x + ix
        self.collision_rect.y     = self.rect.y
        self.collision_rect.width = self._w - ix * 2

    def draw(self, screen):
        x, y, w, h = self.rect
        pts = [(x, y), (x+w, y), (x + w//2, y+h)]
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


# ── Portal ────────────────────────────────────────────────────────────
class Portal:
    MODE_COLORS = {"ship": (0, 200, 255), "cube": (255, 140, 0)}

    def __init__(self, x: float, target_mode: str):
        self.target_mode = target_mode
        self._color      = self.MODE_COLORS.get(target_mode, (200, 200, 200))
        w = 28; h = GROUND_Y - CEILING_Y
        self.rect           = pygame.Rect(int(x), CEILING_Y, w, h)
        self.collision_rect = self.rect.copy()
        self.triggered      = False

    def _sync(self):
        self.collision_rect.topleft = self.rect.topleft

    def draw(self, screen):
        pygame.draw.rect(screen, self._color, self.rect, border_radius=14)
        pygame.draw.rect(screen, (255, 255, 255), self.rect.inflate(-8, -8), width=2, border_radius=10)
        cx, cy = self.rect.center
        if self.target_mode == "ship":
            pts = [(cx, cy-14), (cx-10, cy+10), (cx+10, cy+10)]
        else:
            pts = [(cx-10, cy-10), (cx+10, cy-10), (cx+10, cy+10), (cx-10, cy+10)]
        pygame.draw.polygon(screen, (255, 255, 255), pts)


# ── Muro com gap (passar a nave pelo buraco) ──────────────────────────
class Wall:
    """Muro vertical que vai do teto ao chão com um buraco no meio.
    A nave deve se alinhar com o buraco para passar.
    """
    COLOR      = (60,  45,  90)
    COLOR_EDGE = (120, 90, 160)
    SPIKE_COL  = (255, 80,  30)
    WIDTH      = 45

    def __init__(self, x: float, gap_y: int, gap_h: int = 210):
        """gap_y: centro vertical do buraco. gap_h: altura do buraco."""
        self.gap_top    = max(CEILING_Y, gap_y - gap_h // 2)
        self.gap_bottom = min(GROUND_Y,  gap_y + gap_h // 2)

        h_top    = max(0, self.gap_top    - CEILING_Y)
        h_bottom = max(0, GROUND_Y        - self.gap_bottom)

        self._rt = pygame.Rect(int(x), CEILING_Y,        self.WIDTH, h_top)
        self._rb = pygame.Rect(int(x), self.gap_bottom,  self.WIDTH, h_bottom)

        # rect principal: usado para scroll/despawn
        self.rect           = pygame.Rect(int(x), CEILING_Y, self.WIDTH, GROUND_Y - CEILING_Y)
        self.collision_rect = self._rt   # referência mínima para o loop padrão

        self._ct = self._rt.copy()
        self._cb = self._rb.copy()

    def _sync(self):
        x = self.rect.x
        self._rt.x = x;  self._rb.x = x
        self._ct.x = x;  self._cb.x = x
        self.collision_rect = self._ct

    def collides_with(self, pr: pygame.Rect) -> bool:
        return pr.colliderect(self._ct) or pr.colliderect(self._cb)

    def draw(self, screen):
        for r in (self._rt, self._rb):
            if r.height <= 0: continue
            pygame.draw.rect(screen, self.COLOR,      r)
            pygame.draw.rect(screen, self.COLOR_EDGE, r, width=2)

        # espinhos na borda do buraco (topo)
        if self._rt.height > 0:
            bx = self._rt.x; by = self._rt.bottom
            for i in range(self.WIDTH // 12 + 1):
                cx = bx + i * 12 + 6
                pts = [(cx-6, by), (cx+6, by), (cx, by+12)]
                pygame.draw.polygon(screen, self.SPIKE_COL, pts)

        # espinhos na borda do buraco (baixo)
        if self._rb.height > 0:
            bx = self._rb.x; by = self._rb.top
            for i in range(self.WIDTH // 12 + 1):
                cx = bx + i * 12 + 6
                pts = [(cx-6, by), (cx+6, by), (cx, by-12)]
                pygame.draw.polygon(screen, self.SPIKE_COL, pts)


# ── Laser horizontal pulsante ────────────────────────────────────────
class PulseLaser:
    """Feixe laser horizontal que pisca entre ativo (mortal) e inativo (seguro).
    Atravessa a tela como qualquer obstacle; o jogador deve passar quando está apagado.
    """
    HEIGHT   = 18
    COLOR_ON  = (255,  40,  80)
    COLOR_OFF = ( 80,  30,  50)
    GLOW      = (255, 120, 160)

    def __init__(self, x: float, y: int, freq: float = 2.0, phase: float = 0.0, width: int = 900):
        self.y     = y
        self.freq  = freq
        self._ph   = phase
        self.active = True
        self.rect           = pygame.Rect(int(x), y - self.HEIGHT // 2, width, self.HEIGHT)
        self.collision_rect = self.rect.copy()

    def update(self, t: float):
        self.active = math.sin(t * self.freq + self._ph) > 0

    def _sync(self):
        self.collision_rect.x = self.rect.x

    def draw(self, screen):
        color = self.COLOR_ON if self.active else self.COLOR_OFF
        pygame.draw.rect(screen, color, self.rect, border_radius=4)
        if self.active:
            # inner bright core
            inner = self.rect.inflate(-4, -8)
            pygame.draw.rect(screen, self.GLOW, inner, border_radius=3)
            # glow lines
            pygame.draw.line(screen, self.GLOW,
                             (self.rect.left,  self.rect.centery),
                             (self.rect.right, self.rect.centery), 2)


# ── Bola espinhosa oscilante ──────────────────────────────────────────
class SpikeBall:
    """Bola que oscila verticalmente. Mata no toque."""
    RADIUS    = 22
    SPIKE_LEN = 14
    N_SPIKES  = 10
    COLOR     = (200,  40,  40)
    COL_EDGE  = (255, 100, 100)

    def __init__(self, x: float, base_y: int, amplitude: int = 120, speed: float = 1.8):
        self.base_y    = base_y
        self.amplitude = amplitude
        self.speed     = speed
        self._phase    = random.uniform(0, math.pi * 2)

        r = self.RADIUS + self.SPIKE_LEN
        self.rect           = pygame.Rect(int(x) - r, base_y - r, r * 2, r * 2)
        self.collision_rect = pygame.Rect(int(x) - self.RADIUS, base_y - self.RADIUS,
                                          self.RADIUS * 2, self.RADIUS * 2)

    def update_y(self, t: float):
        cy = int(self.base_y + math.sin(t * self.speed + self._phase) * self.amplitude)
        r  = self.RADIUS + self.SPIKE_LEN
        self.rect.centery           = cy
        self.collision_rect.centery = cy

    def _sync(self):
        self.collision_rect.centerx = self.rect.centerx

    def draw(self, screen):
        cx, cy = self.rect.center
        # espinhos
        for i in range(self.N_SPIKES):
            ang = math.radians(i * 360 / self.N_SPIKES)
            ix = cx + math.cos(ang) * self.RADIUS
            iy = cy + math.sin(ang) * self.RADIUS
            ox = cx + math.cos(ang) * (self.RADIUS + self.SPIKE_LEN)
            oy = cy + math.sin(ang) * (self.RADIUS + self.SPIKE_LEN)
            pygame.draw.line(screen, (255, 140, 40), (int(ix), int(iy)), (int(ox), int(oy)), 3)
        # corpo
        pygame.draw.circle(screen, self.COLOR,    (cx, cy), self.RADIUS)
        pygame.draw.circle(screen, self.COL_EDGE, (cx, cy), self.RADIUS, width=2)
        # olho
        pygame.draw.circle(screen, (255, 220, 80), (cx, cy), 6)
