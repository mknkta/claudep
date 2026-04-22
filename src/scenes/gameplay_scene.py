# gameplay_scene.py — cena principal da Fase 1 (modo Cubo)
#
# Esta cena orquestra:
#   - O Player (cubo com pulo único e rotação).
#   - A grade de fundo que rola para criar ilusão de movimento.
#   - O chão sólido.
#   - O spawner de obstáculos sincronizado com o tempo da fase.
#   - Detecção de colisão player ↔ obstáculos.
#   - Leitura de input (Espaço → pular, ESC → sair).

import pygame
from src.scenes.scene import Scene
from src.entities.player import Player
from src.entities.obstacles import Platform
from src.systems.level_loader import load_level
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    GROUND_Y, COLORS, SPEED_MEDIUM,
)

GRID_SPACING = 100
LEVEL_PATH   = "levels/level1.json"


class GameplayScene(Scene):
    def __init__(self):
        self.player = Player()

        # Velocidade do mundo (pixels/segundo).
        self.world_speed: float = SPEED_MEDIUM

        # Pixels rolados desde o início — equivalente ao "tempo de jogo * world_speed".
        self._camera_x: float = 0.0

        # Carrega a fase: devolve (music_path, lista de ObstacleDef ordenada por spawn_x).
        _music, self._pending = load_level(LEVEL_PATH, self.world_speed)

        # Obstáculos visíveis / próximos da tela.
        self.active_obstacles = []

    # ------------------------------------------------------------------
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._paused = not getattr(self, "_paused", False)

    # ------------------------------------------------------------------
    def update(self, dt: float):
        if getattr(self, "_paused", False):
            return
        self._camera_x += self.world_speed * dt

        # Pulo contínuo: se Espaço estiver pressionado e o player estiver no chão
        # (ou em cima de plataforma), pula imediatamente — sem esperar KEYDOWN.
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.player.jump()

        self.player.update(dt)

        # --- Spawnar obstáculos ---
        # spawn_x = time * world_speed + SCREEN_WIDTH
        # O obstáculo deve entrar pela direita quando camera_x == time * world_speed,
        # ou seja, quando camera_x + SCREEN_WIDTH == spawn_x.
        # Condição de spawn: camera_x >= spawn_x - SCREEN_WIDTH
        while self._pending and self._camera_x >= self._pending[0].spawn_x - SCREEN_WIDTH:
            defn = self._pending.pop(0)
            # Posição na tela no momento do spawn.
            screen_x = defn.spawn_x - self._camera_x
            obs = defn.instantiate(screen_x)
            self.active_obstacles.append(obs)

        # --- Mover obstáculos para a esquerda ---
        for obs in self.active_obstacles:
            obs.update(self.world_speed, dt)

        # --- Remover os que saíram pela esquerda (economiza memória) ---
        self.active_obstacles = [
            obs for obs in self.active_obstacles if obs.rect.right > 0
        ]

        self._check_collisions()

    # ------------------------------------------------------------------
    def _check_collisions(self):
        pr = self.player.rect

        for obs in self.active_obstacles:
            if not pr.colliderect(obs.collision_rect):
                continue

            if isinstance(obs, Platform):
                # Pousa no topo: player descendo e base do player perto do topo da plataforma.
                if self.player.velocity_y >= 0 and pr.bottom <= obs.collision_rect.top + 15:
                    pr.bottom = obs.collision_rect.top
                    self.player.velocity_y = 0.0
                    self.player.on_ground = True
            else:
                pass  # TODO: game over

    # ------------------------------------------------------------------
    def draw(self, screen: pygame.Surface):
        screen.fill(COLORS["background"])
        self._draw_grid(screen)

        pygame.draw.line(
            screen, COLORS["ground"],
            (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y),
            width=4,
        )

        for obs in self.active_obstacles:
            obs.draw(screen)

        self.player.draw(screen)

    # ------------------------------------------------------------------
    def _draw_grid(self, screen: pygame.Surface):
        offset = self._camera_x % GRID_SPACING

        x = -offset
        while x < SCREEN_WIDTH:
            pygame.draw.line(screen, COLORS["grid"], (int(x), 0), (int(x), SCREEN_HEIGHT))
            x += GRID_SPACING

        y = 0
        while y < GROUND_Y:
            pygame.draw.line(screen, COLORS["grid"], (0, y), (SCREEN_WIDTH, y))
            y += GRID_SPACING
