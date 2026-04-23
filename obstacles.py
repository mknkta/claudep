"""
obstacles.py — Classes de todos os obstáculos do jogo.

Cada classe herda de pygame.Sprite e possui ao menos __init__ e draw.
O atributo `rect` representa a área visual; `collision_rect` representa
a área usada para detecção de colisão.
"""

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
    """Carrega (e cacheia) sprite de espinho para as dimensões dadas."""
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
class Spike(pygame.sprite.Sprite):
    """Espinho triangular posicionado no chão. Mata o player no toque."""

    COLOR      = (255,  80,  30)
    COLOR_EDGE = (255, 180,  80)

    def __init__(self, x: float, size: str = "medium"):
        """
        Inicializa o espinho.

        Args:
            x: Posição horizontal de spawn em pixels.
            size: Tamanho ('small', 'medium' ou 'large').
        """
        super().__init__()
        w, h = SIZES.get(size, SIZES["medium"])
        self._w, self._h = w, h
        self.rect = pygame.Rect(int(x), GROUND_Y - h, w, h)
        ix, iy = int(w * 0.15), int(h * 0.20)
        self.collision_rect = pygame.Rect(
            self.rect.x + ix, self.rect.y + iy, w - ix * 2, h - iy)
        self._sprite = _load_spike_sprite(w, h)

    def _sync(self):
        """Sincroniza collision_rect com a posição atual de rect."""
        ix, iy = int(self._w * 0.15), int(self._h * 0.20)
        self.collision_rect.x = self.rect.x + ix
        self.collision_rect.y = self.rect.y + iy

    def collides_with(self, pr: pygame.Rect) -> bool:
        """Retorna True se o rect fornecido colide com collision_rect."""
        return pr.colliderect(self.collision_rect)

    def draw(self, screen):
        """Desenha o espinho na tela."""
        if self._sprite:
            screen.blit(self._sprite, self.rect)
            return
        x, y, w, h = self.rect
        pts = [(x + w//2, y), (x, y+h), (x+w, y+h)]
        pygame.draw.polygon(screen, self.COLOR,      pts)
        pygame.draw.polygon(screen, self.COLOR_EDGE, pts, width=2)


# ── Espinho do teto ───────────────────────────────────────────────────
class CeilingSpike(pygame.sprite.Sprite):
    """Espinho triangular invertido posicionado no teto. Mata no toque."""

    COLOR      = (255,  80,  30)
    COLOR_EDGE = (255, 180,  80)

    def __init__(self, x: float, size: str = "medium"):
        """
        Inicializa o espinho de teto.

        Args:
            x: Posição horizontal de spawn em pixels.
            size: Tamanho ('small', 'medium' ou 'large').
        """
        super().__init__()
        w, h = CEILING_SIZES.get(size, CEILING_SIZES["medium"])
        self._w, self._h = w, h
        self.rect = pygame.Rect(int(x), CEILING_Y, w, h)
        ix = int(w * 0.15)
        self.collision_rect = pygame.Rect(self.rect.x + ix, self.rect.y, w - ix * 2, h)

    def _sync(self):
        """Sincroniza collision_rect com a posição atual de rect."""
        ix = int(self._w * 0.15)
        self.collision_rect.x     = self.rect.x + ix
        self.collision_rect.y     = self.rect.y
        self.collision_rect.width = self._w - ix * 2

    def collides_with(self, pr: pygame.Rect) -> bool:
        """Retorna True se o rect fornecido colide com collision_rect."""
        return pr.colliderect(self.collision_rect)

    def draw(self, screen):
        """Desenha o espinho de teto na tela."""
        x, y, w, h = self.rect
        pts = [(x, y), (x+w, y), (x + w//2, y+h)]
        pygame.draw.polygon(screen, self.COLOR,      pts)
        pygame.draw.polygon(screen, self.COLOR_EDGE, pts, width=2)


# ── Plataforma ────────────────────────────────────────────────────────
class Platform(pygame.sprite.Sprite):
    """Plataforma horizontal em que o player pode pousar."""

    COLOR      = (60, 200, 120)
    COLOR_EDGE = (120, 255, 180)

    def __init__(self, x: float, y: float, width: int = 200):
        """
        Inicializa a plataforma.

        Args:
            x: Posição horizontal de spawn em pixels.
            y: Posição vertical em pixels (topo da plataforma).
            width: Largura da plataforma em pixels.
        """
        super().__init__()
        self.rect           = pygame.Rect(int(x), int(y), width, PLATFORM_H)
        self.collision_rect = self.rect.copy()

    def _sync(self):
        """Sincroniza collision_rect com a posição atual de rect."""
        self.collision_rect.topleft = self.rect.topleft

    def collides_with(self, pr: pygame.Rect) -> bool:
        """Retorna True se o rect fornecido colide com collision_rect."""
        return pr.colliderect(self.collision_rect)

    def draw(self, screen):
        """Desenha a plataforma na tela."""
        pygame.draw.rect(screen, self.COLOR,      self.rect, border_radius=4)
        pygame.draw.rect(screen, self.COLOR_EDGE, self.rect, width=2, border_radius=4)


# ── Portal ────────────────────────────────────────────────────────────
class Portal(pygame.sprite.Sprite):
    """Portal que altera o modo do player ao ser tocado (cubo ↔ nave)."""

    MODE_COLORS = {"ship": (0, 200, 255), "cube": (255, 140, 0)}

    def __init__(self, x: float, target_mode: str):
        """
        Inicializa o portal.

        Args:
            x: Posição horizontal de spawn em pixels.
            target_mode: Modo que o player assume ao tocar o portal ('ship' ou 'cube').
        """
        super().__init__()
        self.target_mode = target_mode
        self._color      = self.MODE_COLORS.get(target_mode, (200, 200, 200))
        w = 28; h = GROUND_Y - CEILING_Y
        self.rect           = pygame.Rect(int(x), CEILING_Y, w, h)
        self.collision_rect = self.rect.copy()
        self.triggered      = False

    def _sync(self):
        """Sincroniza collision_rect com a posição atual de rect."""
        self.collision_rect.topleft = self.rect.topleft

    def collides_with(self, pr: pygame.Rect) -> bool:
        """Retorna True se o rect fornecido colide com collision_rect."""
        return pr.colliderect(self.collision_rect)

    def draw(self, screen):
        """Desenha o portal na tela com ícone do modo alvo."""
        pygame.draw.rect(screen, self._color, self.rect, border_radius=14)
        pygame.draw.rect(screen, (255, 255, 255), self.rect.inflate(-8, -8), width=2, border_radius=10)
        cx, cy = self.rect.center
        if self.target_mode == "ship":
            pts = [(cx, cy-14), (cx-10, cy+10), (cx+10, cy+10)]
        else:
            pts = [(cx-10, cy-10), (cx+10, cy-10), (cx+10, cy+10), (cx-10, cy+10)]
        pygame.draw.polygon(screen, (255, 255, 255), pts)


# ── Portal de Gravidade ───────────────────────────────────────────────
class GravityPortal(pygame.sprite.Sprite):
    """Portal amarelo: inverte gravity_direction do player ao colidir."""

    def __init__(self, x: float):
        """
        Inicializa o portal de gravidade.

        Args:
            x: Posição horizontal de spawn em pixels.
        """
        super().__init__()
        w = 28; h = GROUND_Y - CEILING_Y
        self.rect           = pygame.Rect(int(x), CEILING_Y, w, h)
        self.collision_rect = self.rect.copy()
        self.triggered      = False

    def _sync(self):
        """Sincroniza collision_rect com a posição atual de rect."""
        self.collision_rect.topleft = self.rect.topleft

    def collides_with(self, pr: pygame.Rect) -> bool:
        """Retorna True se o rect fornecido colide com collision_rect."""
        return pr.colliderect(self.collision_rect)

    def draw(self, screen):
        """Desenha o portal de gravidade com seta dupla indicando inversão."""
        color = (255, 220, 0)
        pygame.draw.rect(screen, color, self.rect, border_radius=14)
        pygame.draw.rect(screen, (255, 255, 180), self.rect.inflate(-8, -8), width=2, border_radius=10)
        cx, cy = self.rect.center
        for dy, sign in ((-16, -1), (16, 1)):
            pts = [(cx, cy + dy), (cx - 9, cy + dy - sign*10), (cx + 9, cy + dy - sign*10)]
            pygame.draw.polygon(screen, (255, 255, 255), pts)


# ── Portal de Gravity Flip (espaço inverte gravidade) ────────────────
class GravityFlipPortal(pygame.sprite.Sprite):
    """Portal roxo: muda o modo do player para 'gravity_flip'.

    Nesse modo o espaço inverte a direção da queda a qualquer momento.
    """

    def __init__(self, x: float):
        """
        Inicializa o portal de gravity flip.

        Args:
            x: Posição horizontal de spawn em pixels.
        """
        super().__init__()
        w = 28; h = GROUND_Y - CEILING_Y
        self.rect           = pygame.Rect(int(x), CEILING_Y, w, h)
        self.collision_rect = self.rect.copy()
        self.triggered      = False

    def _sync(self):
        """Sincroniza collision_rect com a posição atual de rect."""
        self.collision_rect.topleft = self.rect.topleft

    def collides_with(self, pr: pygame.Rect) -> bool:
        """Retorna True se o rect fornecido colide com collision_rect."""
        return pr.colliderect(self.collision_rect)

    def draw(self, screen):
        """Desenha o portal roxo com seta dupla e barra central."""
        color = (160, 60, 255)
        pygame.draw.rect(screen, color, self.rect, border_radius=14)
        pygame.draw.rect(screen, (220, 180, 255), self.rect.inflate(-8, -8), width=2, border_radius=10)
        cx, cy = self.rect.center
        for dy, sign in ((-18, -1), (18, 1)):
            pts = [(cx, cy + dy + sign * 10),
                   (cx - 10, cy + dy - sign * 4),
                   (cx + 10, cy + dy - sign * 4)]
            pygame.draw.polygon(screen, (255, 255, 255), pts)
        pygame.draw.line(screen, (255, 255, 255), (cx, cy - 6), (cx, cy + 6), 3)


# ── Muro com gap (passar a nave pelo buraco) ──────────────────────────
class Wall(pygame.sprite.Sprite):
    """Muro vertical que vai do teto ao chão com um buraco no meio.

    A nave deve se alinhar com o buraco para passar. Possui dois
    collision_rects (parte superior e inferior).
    """

    COLOR      = (60,  45,  90)
    COLOR_EDGE = (120, 90, 160)
    SPIKE_COL  = (255, 80,  30)
    WIDTH      = 45

    def __init__(self, x: float, gap_y: int, gap_h: int = 210):
        """
        Inicializa o muro com buraco.

        Args:
            x: Posição horizontal de spawn em pixels.
            gap_y: Centro vertical do buraco em pixels.
            gap_h: Altura do buraco em pixels.
        """
        super().__init__()
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
        """Atualiza a posição de todos os rects internos conforme rect.x."""
        x = self.rect.x
        self._rt.x = x;  self._rb.x = x
        self._ct.x = x;  self._cb.x = x
        self.collision_rect = self._ct

    def collides_with(self, pr: pygame.Rect) -> bool:
        """Retorna True se pr colide com a parte superior ou inferior do muro."""
        return pr.colliderect(self._ct) or pr.colliderect(self._cb)

    def draw(self, screen):
        """Desenha o muro com espinhos nas bordas do buraco."""
        for r in (self._rt, self._rb):
            if r.height <= 0:
                continue
            pygame.draw.rect(screen, self.COLOR,      r)
            pygame.draw.rect(screen, self.COLOR_EDGE, r, width=2)

        if self._rt.height > 0:
            bx = self._rt.x; by = self._rt.bottom
            for i in range(self.WIDTH // 12 + 1):
                cx = bx + i * 12 + 6
                pts = [(cx-6, by), (cx+6, by), (cx, by+12)]
                pygame.draw.polygon(screen, self.SPIKE_COL, pts)

        if self._rb.height > 0:
            bx = self._rb.x; by = self._rb.top
            for i in range(self.WIDTH // 12 + 1):
                cx = bx + i * 12 + 6
                pts = [(cx-6, by), (cx+6, by), (cx, by-12)]
                pygame.draw.polygon(screen, self.SPIKE_COL, pts)


# ── Laser horizontal pulsante ────────────────────────────────────────
class PulseLaser(pygame.sprite.Sprite):
    """Feixe laser horizontal que pisca entre ativo (mortal) e inativo (seguro).

    Atravessa a tela como qualquer obstáculo; o jogador deve passar quando
    o laser está apagado.
    """

    HEIGHT    = 18
    COLOR_ON  = (255,  40,  80)
    COLOR_OFF = ( 80,  30,  50)
    GLOW      = (255, 120, 160)

    def __init__(self, x: float, y: int, freq: float = 2.0, phase: float = 0.0, width: int = 900):
        """
        Inicializa o laser pulsante.

        Args:
            x: Posição horizontal de spawn em pixels.
            y: Posição vertical central do laser em pixels.
            freq: Frequência de pulsação em Hz.
            phase: Fase inicial em radianos.
            width: Largura total do laser em pixels.
        """
        super().__init__()
        self.y      = y
        self.freq   = freq
        self._ph    = phase
        self.active = True
        self.rect           = pygame.Rect(int(x), y - self.HEIGHT // 2, width, self.HEIGHT)
        self.collision_rect = self.rect.copy()

    def update(self, t: float):
        """Atualiza o estado ativo/inativo com base no tempo da música."""
        self.active = math.sin(t * self.freq + self._ph) > 0

    def _sync(self):
        """Sincroniza collision_rect com a posição horizontal de rect."""
        self.collision_rect.x = self.rect.x

    def collides_with(self, pr: pygame.Rect) -> bool:
        """Retorna True se ativo e o rect fornecido colide com collision_rect."""
        return self.active and pr.colliderect(self.collision_rect)

    def draw(self, screen):
        """Desenha o laser com efeito de brilho quando ativo."""
        color = self.COLOR_ON if self.active else self.COLOR_OFF
        pygame.draw.rect(screen, color, self.rect, border_radius=4)
        if self.active:
            inner = self.rect.inflate(-4, -8)
            pygame.draw.rect(screen, self.GLOW, inner, border_radius=3)
            pygame.draw.line(screen, self.GLOW,
                             (self.rect.left,  self.rect.centery),
                             (self.rect.right, self.rect.centery), 2)


# ── Bola espinhosa oscilante ──────────────────────────────────────────
class SpikeBall(pygame.sprite.Sprite):
    """Bola espinhosa que oscila verticalmente. Mata no toque."""

    RADIUS    = 22
    SPIKE_LEN = 14
    N_SPIKES  = 10
    COLOR     = (200,  40,  40)
    COL_EDGE  = (255, 100, 100)

    def __init__(self, x: float, base_y: int, amplitude: int = 120, speed: float = 1.8):
        """
        Inicializa a bola espinhosa.

        Args:
            x: Posição horizontal de spawn em pixels.
            base_y: Centro vertical de oscilação em pixels.
            amplitude: Amplitude da oscilação em pixels.
            speed: Velocidade angular da oscilação em rad/s.
        """
        super().__init__()
        self.base_y    = base_y
        self.amplitude = amplitude
        self.speed     = speed
        self._phase    = random.uniform(0, math.pi * 2)

        r = self.RADIUS + self.SPIKE_LEN
        self.rect           = pygame.Rect(int(x) - r, base_y - r, r * 2, r * 2)
        self.collision_rect = pygame.Rect(int(x) - self.RADIUS, base_y - self.RADIUS,
                                          self.RADIUS * 2, self.RADIUS * 2)

    def update_y(self, t: float):
        """Atualiza a posição vertical da bola com base no tempo da música."""
        cy = int(self.base_y + math.sin(t * self.speed + self._phase) * self.amplitude)
        r  = self.RADIUS + self.SPIKE_LEN
        self.rect.centery           = cy
        self.collision_rect.centery = cy

    def _sync(self):
        """Sincroniza o centro horizontal do collision_rect com rect."""
        self.collision_rect.centerx = self.rect.centerx

    def collides_with(self, pr: pygame.Rect) -> bool:
        """Retorna True se o rect fornecido colide com collision_rect."""
        return pr.colliderect(self.collision_rect)

    def draw(self, screen):
        """Desenha a bola espinhosa com corpo, espinhos e olho."""
        cx, cy = self.rect.center
        for i in range(self.N_SPIKES):
            ang = math.radians(i * 360 / self.N_SPIKES)
            ix = cx + math.cos(ang) * self.RADIUS
            iy = cy + math.sin(ang) * self.RADIUS
            ox = cx + math.cos(ang) * (self.RADIUS + self.SPIKE_LEN)
            oy = cy + math.sin(ang) * (self.RADIUS + self.SPIKE_LEN)
            pygame.draw.line(screen, (255, 140, 40), (int(ix), int(iy)), (int(ox), int(oy)), 3)
        pygame.draw.circle(screen, self.COLOR,    (cx, cy), self.RADIUS)
        pygame.draw.circle(screen, self.COL_EDGE, (cx, cy), self.RADIUS, width=2)
        pygame.draw.circle(screen, (255, 220, 80), (cx, cy), 6)
