import math
import os
import pygame
from config import GRAVITY, GROUND_Y, SHIP_THRUST

SIZE         = 60
JUMP_IMPULSE = -15
ROT_SPEED    = 6
VEL_MAX      = 15   # limite de velocidade vertical no modo nave


class Player:
    def __init__(self):
        self.rect           = pygame.Rect(150, GROUND_Y - SIZE, SIZE, SIZE)
        self.collision_rect = self.rect.copy()
        self.velocity_y: float = 0.0
        self.on_ground:  bool  = True
        self._angle:     float = 0.0
        self.mode:       str   = "cube"   # "cube" ou "ship"

        self._cube_sprite = self._load_sprite(
            ["assets/player.jpg", "assets/player.png"],
            fallback_color=(100, 80, 220), border_color=(160, 140, 255),
        )
        self._ship_sprite = self._load_ship_sprite()

    # ── carregamento de sprites ───────────────────────────────────────
    def _load_sprite(self, paths, fallback_color, border_color):
        for name in paths:
            if os.path.isfile(name):
                try:
                    img = pygame.image.load(name).convert_alpha()
                    return pygame.transform.scale(img, (SIZE, SIZE))
                except pygame.error:
                    pass
        s = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
        pygame.draw.rect(s, fallback_color, s.get_rect(), border_radius=4)
        pygame.draw.rect(s, border_color,   s.get_rect(), width=3, border_radius=4)
        return s

    def _load_ship_sprite(self):
        for name in ("assets/ship.jpg", "assets/ship.png"):
            if os.path.isfile(name):
                try:
                    img = pygame.image.load(name).convert_alpha()
                    return pygame.transform.scale(img, (SIZE, SIZE))
                except pygame.error:
                    pass
        # Fallback: trapézio laranja
        s = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
        pts = [
            (6,           SIZE - 8),   # base esquerda
            (SIZE - 6,    SIZE - 8),   # base direita
            (SIZE - 16,   8),          # topo direito
            (16,          8),          # topo esquerdo
        ]
        pygame.draw.polygon(s, (255, 140, 0),   pts)
        pygame.draw.polygon(s, (255, 220, 80),  pts, width=3)
        # "cockpit" no centro
        pygame.draw.circle(s, (80, 220, 255), (SIZE // 2, SIZE // 2), 10)
        return s

    # ── troca de modo ─────────────────────────────────────────────────
    def set_mode(self, new_mode: str):
        self.mode       = new_mode
        self.velocity_y = 0.0
        self.on_ground  = False

    # ── update ────────────────────────────────────────────────────────
    def update(self, dt, space_held: bool = False):
        self.velocity_y += GRAVITY

        if self.mode == "ship":
            if space_held:
                self.velocity_y -= SHIP_THRUST
            else:
                # soltou o espaço: amortece o impulso de subida rapidamente
                if self.velocity_y < 0:
                    self.velocity_y *= 0.80
            # limita velocidade vertical
            self.velocity_y = max(-VEL_MAX, min(VEL_MAX, self.velocity_y))
            # ângulo segue a direção do movimento
            self._angle = math.degrees(math.atan2(self.velocity_y, 10))
        else:
            # cubo: gira no ar, trava em múltiplo de 90° ao pousar
            if not self.on_ground:
                self._angle += ROT_SPEED

        self.rect.y += int(self.velocity_y)

        # colisão com chão
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            if self.mode == "ship":
                # nave: só para de cair, mas NÃO zera velocity se já estava subindo
                if self.velocity_y > 0:
                    self.velocity_y = 0.0
            else:
                self.velocity_y = 0.0
                self.on_ground  = True
                self._angle = round(self._angle / 90) * 90
        else:
            if self.mode == "cube":
                self.on_ground = False

    # ── pulo (só modo cubo) ───────────────────────────────────────────
    def jump(self) -> bool:
        if self.mode == "cube" and self.on_ground:
            self.velocity_y = JUMP_IMPULSE
            self.on_ground  = False
            return True
        return False

    # ── draw ──────────────────────────────────────────────────────────
    def draw(self, screen):
        sprite  = self._ship_sprite if self.mode == "ship" else self._cube_sprite
        rotated = pygame.transform.rotate(sprite, -self._angle)
        screen.blit(rotated, rotated.get_rect(center=self.rect.center))
