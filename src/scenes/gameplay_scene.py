# gameplay_scene.py — cena principal da Fase 1 (modo Cubo)
#
# Fonte da verdade do tempo: get_music_time() — não acumula dt.
# Isso garante que travamentos de frame não dessincronizam os obstáculos.
#
# Posição X de cada obstáculo ativo é recalculada todo frame como:
#   screen_x = spawn_x_original - music_time * world_speed
# onde spawn_x_original = time_musical * world_speed + SCREEN_WIDTH.

import pygame
from src.scenes.scene import Scene
from src.entities.player import Player
from src.entities.obstacles import Platform
from src.systems.level_loader import load_level
from src.systems import audio_manager as audio
from src.systems import debug_overlay
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    GROUND_Y, COLORS, SPEED_MEDIUM,
)

GRID_SPACING = 100
LEVEL_PATH   = "levels/level1.json"
SFX_JUMP     = "assets/sfx/jump.wav"


class GameplayScene(Scene):
    def __init__(self):
        self.player = Player()
        self.world_speed: float = SPEED_MEDIUM

        # Carrega a fase.
        music_path, self._all_defs = load_level(LEVEL_PATH, self.world_speed)

        # _all_defs contém TODOS os obstáculos ordenados por spawn_x.
        # Usamos índice para saber quais já foram instanciados.
        self._next_def_idx: int = 0

        # Obstáculos ativos na tela (instanciados, ainda não saíram pela esquerda).
        self.active_obstacles = []

        # Inicia a música (silencioso se o arquivo não existir).
        audio.play_music(music_path)

        # Estado
        self._paused:    bool = False
        self._debug:     bool = False

        # Referência ao clock — será injetada pelo draw() via GameplayScene.set_clock().
        self._clock: pygame.time.Clock | None = None

    def set_clock(self, clock: pygame.time.Clock):
        """Recebe o clock do main loop para o overlay de debug."""
        self._clock = clock

    # ------------------------------------------------------------------
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._paused = not self._paused
                elif event.key == pygame.K_F3:
                    self._debug = not self._debug

    # ------------------------------------------------------------------
    def update(self, dt: float):
        if self._paused:
            return

        # Fonte da verdade: tempo da música (não dt acumulado).
        music_t = audio.get_music_time()

        # camera_x serve apenas para a grade de fundo rolante.
        # Deriva diretamente do tempo da música — sem acúmulo de erro.
        self._camera_x = music_t * self.world_speed

        # --- Pulo contínuo ---
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if self.player.jump():
                audio.play_sfx(SFX_JUMP)

        self.player.update(dt)

        # --- Spawnar obstáculos ---
        # Condição: o tempo da música já passou do instante de spawn.
        # spawn_x = time * world_speed + SCREEN_WIDTH
        # → time = (spawn_x - SCREEN_WIDTH) / world_speed
        while (self._next_def_idx < len(self._all_defs) and
               music_t >= (self._all_defs[self._next_def_idx].spawn_x - SCREEN_WIDTH) / self.world_speed):
            defn = self._all_defs[self._next_def_idx]
            self._next_def_idx += 1
            # Posição na tela no momento do spawn.
            screen_x = defn.spawn_x - self._camera_x
            obs = defn.instantiate(screen_x)
            # Guarda spawn_x original para recálculo preciso todo frame.
            obs._spawn_x = defn.spawn_x
            self.active_obstacles.append(obs)

        # --- Reposicionar obstáculos com base no tempo da música ---
        # Em vez de mover por dt (acumulando erro), calculamos a posição exata.
        for obs in self.active_obstacles:
            new_x = int(obs._spawn_x - self._camera_x)
            dx = new_x - obs.rect.x
            obs.rect.x = new_x
            obs.collision_rect.x += dx

        # --- Remover os que saíram pela esquerda ---
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

        if self._debug and self._clock:
            debug_overlay.draw(
                screen,
                self._clock,
                audio.get_music_time(),
                self.player,
                self.active_obstacles,
            )

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
