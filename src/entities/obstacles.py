# obstacles.py — classes de obstáculos do jogo
#
# Hierarquia:
#   Obstacle (base)
#   ├── Spike    — triângulo/espinho no chão, 3 tamanhos (small/medium/large)
#   └── Platform — plataforma flutuante, player pode pousar em cima
#
# Tamanhos dos espinhos (largura × altura):
#   small  → 30 × 25
#   medium → 45 × 38
#   large  → 58 × 48   ← maior tamanho disponível
#
# Limite de pulo: não empilhar espinhos cuja largura total ultrapasse
# ~210 px (equivalente a 3.5 × o espinho "large" antigo de 60 px).

import os
import pygame
from config import GROUND_Y

PLATFORM_HEIGHT = 20

# Dimensões por tamanho de espinho
_SPIKE_SIZES = {
    "small":  (30, 25),
    "medium": (45, 38),
    "large":  (58, 48),
}


class Obstacle:
    """Classe base. Todo obstáculo tem um rect de desenho e um collision_rect."""

    def __init__(self, x: float, y: float, width: int, height: int):
        self.rect = pygame.Rect(int(x), int(y), width, height)
        self.collision_rect = self.rect.copy()

    def _sync_collision_rect(self):
        self.collision_rect.topleft = self.rect.topleft

    def draw(self, screen: pygame.Surface):
        raise NotImplementedError


# ======================================================================
class Spike(Obstacle):
    """Espinho triangular apoiado no chão.

    size: "small" | "medium" | "large"  (padrão: "medium")
    Hitbox com inset de 15% em cada lado e 20% no topo.
    """

    _COLOR      = (255,  80,  30)
    _COLOR_EDGE = (255, 180,  80)

    def __init__(self, x: float, size: str = "medium"):
        w, h = _SPIKE_SIZES.get(size, _SPIKE_SIZES["medium"])
        y = GROUND_Y - h
        super().__init__(x, y, w, h)
        self._w = w
        self._h = h

        inset_x = int(w * 0.15)
        inset_y = int(h * 0.20)
        self.collision_rect = pygame.Rect(
            self.rect.x + inset_x,
            self.rect.y + inset_y,
            w - inset_x * 2,
            h - inset_y,
        )

        self._surface = self._load_sprite(w, h)

    def _load_sprite(self, w: int, h: int) -> pygame.Surface | None:
        path = os.path.join("assets", "sprites", "spike.jpg")
        if os.path.isfile(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(img, (w, h))
            except pygame.error:
                pass
        return None

    def _sync_collision_rect(self):
        inset_x = int(self._w * 0.15)
        inset_y = int(self._h * 0.20)
        self.collision_rect.x      = self.rect.x + inset_x
        self.collision_rect.y      = self.rect.y + inset_y
        self.collision_rect.width  = self._w - inset_x * 2
        self.collision_rect.height = self._h - inset_y

    def draw(self, screen: pygame.Surface):
        if self._surface:
            screen.blit(self._surface, self.rect)
            return

        x, y, w, h = self.rect
        points = [
            (x + w // 2, y),
            (x,          y + h),
            (x + w,      y + h),
        ]
        pygame.draw.polygon(screen, self._COLOR, points)
        pygame.draw.polygon(screen, self._COLOR_EDGE, points, width=2)


# ======================================================================
class Platform(Obstacle):
    """Retângulo flutuante. Player pode pousar em cima."""

    _COLOR      = (60, 200, 120)
    _COLOR_EDGE = (120, 255, 180)

    def __init__(self, x: float, y: float, width: int = 200):
        super().__init__(x, y, width, PLATFORM_HEIGHT)
        self.collision_rect = self.rect.copy()

    def _sync_collision_rect(self):
        self.collision_rect.topleft = self.rect.topleft

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self._COLOR, self.rect, border_radius=4)
        pygame.draw.rect(screen, self._COLOR_EDGE, self.rect, width=2, border_radius=4)
