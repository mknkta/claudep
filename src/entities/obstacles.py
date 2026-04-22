# obstacles.py — classes de obstáculos do jogo
#
# Hierarquia:
#   Obstacle (base)
#   ├── Spike    — triângulo/espinho no chão, mata o player
#   └── Platform — plataforma flutuante, player pode pousar em cima

import os
import pygame
from config import GROUND_Y, SCREEN_WIDTH

# Dimensões padrão dos obstáculos
SPIKE_WIDTH  = 60
SPIKE_HEIGHT = 50

PLATFORM_HEIGHT = 20


class Obstacle:
    """Classe base. Todo obstáculo tem um rect de desenho e um collision_rect."""

    def __init__(self, x: float, y: float, width: int, height: int):
        self.rect = pygame.Rect(int(x), int(y), width, height)
        # Subclasses definem collision_rect com a hitbox reduzida.
        self.collision_rect = self.rect.copy()

    # ------------------------------------------------------------------
    def update(self, world_speed: float, dt: float):
        """Move o obstáculo para a esquerda conforme o mundo avança."""
        self.rect.x -= int(world_speed * dt)
        # Mantém collision_rect sincronizado com rect.
        self._sync_collision_rect()

    def _sync_collision_rect(self):
        """Subclasses sobrescrevem para posicionar a hitbox em relação ao rect."""
        self.collision_rect.topleft = self.rect.topleft

    # ------------------------------------------------------------------
    def draw(self, screen: pygame.Surface):
        raise NotImplementedError


# ======================================================================
class Spike(Obstacle):
    """Espinho triangular apoiado no chão. Hitbox 20% menor que o visual."""

    # Cor de fallback (vermelho-laranja neon)
    _COLOR       = (255, 80,  30)
    _COLOR_EDGE  = (255, 180, 80)

    def __init__(self, x: float):
        y = GROUND_Y - SPIKE_HEIGHT
        super().__init__(x, y, SPIKE_WIDTH, SPIKE_HEIGHT)

        # Hitbox 20% menor (10% de cada lado / topo).
        inset_x = int(SPIKE_WIDTH  * 0.10)
        inset_y = int(SPIKE_HEIGHT * 0.20)
        self.collision_rect = pygame.Rect(
            self.rect.x      + inset_x,
            self.rect.y      + inset_y,
            SPIKE_WIDTH      - inset_x * 2,
            SPIKE_HEIGHT     - inset_y,
        )

        # Tenta carregar sprite externo.
        self._surface = self._load_sprite()

    # ------------------------------------------------------------------
    def _load_sprite(self) -> pygame.Surface | None:
        path = os.path.join("assets", "sprites", "spike.png")
        if os.path.isfile(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(img, (SPIKE_WIDTH, SPIKE_HEIGHT))
            except pygame.error:
                pass
        return None

    def _sync_collision_rect(self):
        inset_x = int(SPIKE_WIDTH  * 0.10)
        inset_y = int(SPIKE_HEIGHT * 0.20)
        self.collision_rect.x      = self.rect.x + inset_x
        self.collision_rect.y      = self.rect.y + inset_y
        self.collision_rect.width  = SPIKE_WIDTH  - inset_x * 2
        self.collision_rect.height = SPIKE_HEIGHT - inset_y

    # ------------------------------------------------------------------
    def draw(self, screen: pygame.Surface):
        if self._surface:
            screen.blit(self._surface, self.rect)
            return

        # Fallback: desenha triângulo.
        x, y, w, h = self.rect
        points = [
            (x + w // 2, y),          # ponta do topo
            (x,          y + h),       # base esquerda
            (x + w,      y + h),       # base direita
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
        # Hitbox igual ao rect visual para plataformas.
        self.collision_rect = self.rect.copy()

    def _sync_collision_rect(self):
        self.collision_rect.topleft = self.rect.topleft

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self._COLOR, self.rect, border_radius=4)
        pygame.draw.rect(screen, self._COLOR_EDGE, self.rect, width=2, border_radius=4)
