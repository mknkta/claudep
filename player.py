"""
player.py — Classe do personagem controlado pelo jogador.

O Player herda de pygame.Sprite e suporta três modos de jogo:
  - 'cube': pula ao pressionar espaço, segue a gravidade.
  - 'ship': planador que sobe com espaço pressionado.
  - 'gravity_flip': espaço inverte a direção da gravidade.
"""

import math
import os
import pygame
from config import GRAVITY, GROUND_Y, CEILING_Y, SHIP_THRUST

SIZE         = 60
JUMP_IMPULSE = -15
ROT_SPEED    = 6
VEL_MAX      = 15          # limite de velocidade vertical no modo nave
JUMP_CD      = 0.25        # cooldown de pulo em segundos (modo cubo)


class Player(pygame.sprite.Sprite):
    """Personagem principal controlado pelo jogador.

    Possui três modos: cubo (pulo), nave (thrust) e gravity_flip (inversão).
    O atributo `collision_rect` é usado para detecção de colisão; `rect`
    representa a área visual para renderização.
    """

    def __init__(self):
        """Inicializa o player na posição inicial com modo cubo."""
        super().__init__()
        self.rect               = pygame.Rect(150, GROUND_Y - SIZE, SIZE, SIZE)
        self.collision_rect     = self.rect.copy()
        self.velocity_y:        float = 0.0
        self.on_ground:         bool  = True
        self._angle:            float = 0.0
        self.mode:              str   = "cube"   # "cube", "ship" ou "gravity_flip"
        self.gravity_direction: int   = 1        # 1 = pra baixo, -1 = pra cima
        self._grav_cooldown:    float = 0.0      # cooldown após inversão de gravidade
        self._jump_cooldown:    float = 0.0      # cooldown do pulo (modo cubo)

        self._cube_sprite = self._load_sprite(
            ["assets/player.jpg", "assets/player.png"],
            fallback_color=(100, 80, 220), border_color=(160, 140, 255),
        )
        self._ship_sprite = self._load_ship_sprite()

    # ── carregamento de sprites ───────────────────────────────────────
    def _load_sprite(self, paths, fallback_color, border_color):
        """Tenta carregar sprite de uma lista de caminhos; usa fallback desenhado se não encontrar."""
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
        """Carrega o sprite da nave; usa trapézio laranja como fallback."""
        for name in ("assets/ship.jpg", "assets/ship.png"):
            if os.path.isfile(name):
                try:
                    img = pygame.image.load(name).convert_alpha()
                    return pygame.transform.scale(img, (SIZE, SIZE))
                except pygame.error:
                    pass
        s = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
        pts = [
            (6,           SIZE - 8),
            (SIZE - 6,    SIZE - 8),
            (SIZE - 16,   8),
            (16,          8),
        ]
        pygame.draw.polygon(s, (255, 140, 0),   pts)
        pygame.draw.polygon(s, (255, 220, 80),  pts, width=3)
        pygame.draw.circle(s, (80, 220, 255), (SIZE // 2, SIZE // 2), 10)
        return s

    # ── troca de modo ─────────────────────────────────────────────────
    def set_mode(self, new_mode: str):
        """Altera o modo do player e zera a velocidade vertical."""
        self.mode       = new_mode
        self.velocity_y = 0.0
        self.on_ground  = False

    # ── inversão de gravidade ─────────────────────────────────────────
    def invert_gravity(self):
        """Inverte gravity_direction e aplica cooldown para evitar inversões repetidas."""
        self.gravity_direction *= -1
        self.velocity_y        *= -0.5
        self.on_ground          = False
        self._grav_cooldown     = 0.3

    # ── cooldown do pulo ──────────────────────────────────────────────
    @property
    def jump_cooldown_ratio(self) -> float:
        """Fração do cooldown de pulo restante (0.0 = pronto, 1.0 = cheio)."""
        return min(self._jump_cooldown / JUMP_CD, 1.0)

    # ── update ────────────────────────────────────────────────────────
    def update(self, dt, space_held: bool = False):
        """
        Atualiza física, posição e ângulo do player.

        Args:
            dt: Delta de tempo em segundos desde o último frame.
            space_held: True se a tecla de ação está pressionada.
        """
        if self._grav_cooldown > 0:
            self._grav_cooldown -= dt
        if self._jump_cooldown > 0:
            self._jump_cooldown -= dt

        self.velocity_y += GRAVITY * self.gravity_direction

        if self.mode == "ship":
            thrust_dir = -self.gravity_direction
            if space_held:
                self.velocity_y += SHIP_THRUST * thrust_dir
            else:
                if self.velocity_y * self.gravity_direction < 0:
                    self.velocity_y *= 0.80
            self.velocity_y = max(-VEL_MAX, min(VEL_MAX, self.velocity_y))
            self._angle = math.degrees(math.atan2(self.velocity_y, 10))
        elif self.mode == "gravity_flip":
            if not self.on_ground:
                self._angle += ROT_SPEED * self.gravity_direction
        else:
            # cubo: auto-pulo ao tocar chão segurando espaço
            if self.on_ground and space_held:
                self.jump()
            if not self.on_ground:
                self._angle += ROT_SPEED * self.gravity_direction

        self.rect.y += int(self.velocity_y)

        if self.gravity_direction == 1:
            if self.rect.bottom >= GROUND_Y:
                self.rect.bottom = GROUND_Y
                if self.mode == "ship":
                    if self.velocity_y > 0:
                        self.velocity_y = 0.0
                else:
                    self.velocity_y = 0.0
                    self.on_ground  = True
                    self._angle = round(self._angle / 90) * 90
            else:
                if self.mode in ("cube", "gravity_flip"):
                    self.on_ground = False
        else:
            if self.rect.top <= CEILING_Y:
                self.rect.top = CEILING_Y
                if self.mode == "ship":
                    if self.velocity_y < 0:
                        self.velocity_y = 0.0
                else:
                    self.velocity_y = 0.0
                    self.on_ground  = True
                    self._angle = round(self._angle / 90) * 90
            else:
                if self.mode in ("cube", "gravity_flip"):
                    self.on_ground = False

    # ── pulo (só modo cubo) ───────────────────────────────────────────
    def jump(self) -> bool:
        """
        Executa o pulo no modo cubo, respeitando cooldown.

        Returns:
            True se o pulo foi executado, False caso contrário.
        """
        if self.mode == "cube" and self.on_ground and self._jump_cooldown <= 0:
            self.velocity_y     = JUMP_IMPULSE * self.gravity_direction
            self.on_ground      = False
            self._jump_cooldown = JUMP_CD
            return True
        return False

    # ── flip de gravidade (modo gravity_flip) ─────────────────────────
    def flip_gravity(self):
        """Inverte gravity_direction; pode ser chamado a qualquer momento no modo gravity_flip."""
        self.gravity_direction *= -1
        self.velocity_y         = 8.0 * self.gravity_direction
        self.on_ground          = False

    # ── draw ──────────────────────────────────────────────────────────
    def draw(self, screen):
        """Desenha o player rotacionado e, se em cooldown, a barra indicadora."""
        sprite = self._ship_sprite if self.mode == "ship" else self._cube_sprite
        if self.gravity_direction == -1:
            sprite = pygame.transform.flip(sprite, False, True)
        rotated = pygame.transform.rotate(sprite, -self._angle)
        screen.blit(rotated, rotated.get_rect(center=self.rect.center))

        # indicador visual de cooldown de pulo (modo cubo)
        if self.mode == "cube" and self._jump_cooldown > 0:
            self._draw_jump_cooldown(screen)

    def _draw_jump_cooldown(self, screen):
        """Desenha uma barra de cooldown de pulo abaixo do player."""
        ratio = self.jump_cooldown_ratio   # 1.0 = cheio (bloqueado), 0.0 = pronto
        bar_w = SIZE
        bar_h = 5
        bx    = self.rect.x
        by    = self.rect.bottom + 4

        # fundo
        pygame.draw.rect(screen, (40, 30, 60), (bx, by, bar_w, bar_h), border_radius=2)
        # preenchimento: cor vai de vermelho (bloqueado) para verde (pronto)
        fill_w = int(bar_w * (1.0 - ratio))
        if fill_w > 0:
            r = int(255 * ratio)
            g = int(200 * (1.0 - ratio))
            pygame.draw.rect(screen, (r, g, 80), (bx, by, fill_w, bar_h), border_radius=2)
