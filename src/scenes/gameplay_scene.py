# gameplay_scene.py — cena principal de jogo
#
# Fonte da verdade do tempo: get_music_time() — não acumula dt.
# Posição X dos obstáculos: spawn_x_original - music_time * world_speed.

import random
import pygame
from src.scenes.scene import Scene
from src.entities.player import Player
from src.entities.obstacles import Platform, Spike
from src.systems.level_loader import load_level
from src.systems import audio_manager as audio
from src.systems import debug_overlay
from src.systems import save_manager
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    GROUND_Y, COLORS, SPEED_MEDIUM,
)

GRID_SPACING = 100
LEVEL_PATH   = "levels/level1.json"
SFX_JUMP     = "assets/sfx/jump.wav"

# Morte: tempo de congelamento antes de mostrar o painel de game over
FREEZE_DURATION = 0.5

# Barra de progresso
_BAR_H   = 8
_BAR_COL = (140, 80, 220)
_BAR_BG  = (40, 30, 60)


# ──────────────────────────────────────────────────────────────────────
class _Particle:
    """Pequeno quadrado colorido que explode na morte do player."""

    def __init__(self, x: float, y: float):
        self.x  = x + random.uniform(-5, 5)
        self.y  = y + random.uniform(-5, 5)
        self.vx = random.uniform(-300, 300)
        self.vy = random.uniform(-300, 300)
        self.size     = random.randint(5, 14)
        self.life     = random.uniform(0.6, 1.0)   # segundos até desaparecer
        self.max_life = self.life
        r = random.choice([
            (100, 80, 220), (160, 100, 255), (80, 200, 255),
            (255, 200, 80), (255, 255, 255),
        ])
        self.color = r

    def update(self, dt: float):
        self.vy += 600 * dt   # gravidade
        self.x  += self.vx * dt
        self.y  += self.vy * dt
        self.life -= dt

    @property
    def alive(self) -> bool:
        return self.life > 0

    def draw(self, screen: pygame.Surface):
        alpha = max(0, int(255 * self.life / self.max_life))
        s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        s.fill((*self.color, alpha))
        screen.blit(s, (int(self.x - self.size // 2), int(self.y - self.size // 2)))


# ──────────────────────────────────────────────────────────────────────
class GameplayScene(Scene):
    def __init__(self, world_speed: float = SPEED_MEDIUM,
                 hitbox_scale: float = 1.0,
                 zoom: float = 1.0,
                 phase: int = 1,
                 manager=None):
        self._manager      = manager
        self._phase        = phase
        self._world_speed  = world_speed
        self._hitbox_scale = hitbox_scale
        self._zoom         = zoom

        self.player = Player()

        # Ajusta o collision rect do player de acordo com hitbox_scale.
        # hitbox_scale < 1.0 → hitbox menor que o visual (mais fácil).
        # Guardamos o rect original para recalcular se necessário.
        self._apply_hitbox_scale()

        # Carrega a fase.
        music_path, self._all_defs, self._music_duration = load_level(LEVEL_PATH, world_speed)
        self._next_def_idx: int = 0
        self.active_obstacles: list = []

        # Attempts
        self._attempts = save_manager.get_attempts()

        # Inicia a música.
        audio.play_music(music_path)

        # Estado de morte
        self._dead:           bool  = False
        self._freeze_timer:   float = 0.0
        self._particles:      list  = []
        self._death_snapshot: pygame.Surface | None = None

        # Estado geral
        self._paused: bool = False
        self._debug:  bool = False
        self._won:    bool = False

        # Clock (injetado pelo main loop)
        self._clock: pygame.time.Clock | None = None

        # Surface para zoom (reutilizada a cada frame)
        self._render_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    # ------------------------------------------------------------------
    def _apply_hitbox_scale(self):
        """Cria player.collision_rect escalado por hitbox_scale."""
        r = self.player.rect
        if self._hitbox_scale == 1.0:
            self.player.collision_rect = r
        else:
            sw = int(r.width  * self._hitbox_scale)
            sh = int(r.height * self._hitbox_scale)
            self.player.collision_rect = pygame.Rect(
                r.centerx - sw // 2,
                r.centery - sh // 2,
                sw, sh,
            )

    def _sync_player_collision(self):
        """Mantém collision_rect centrado no player.rect após movimentos."""
        if self._hitbox_scale == 1.0:
            self.player.collision_rect = self.player.rect
            return
        r = self.player.rect
        sw = int(r.width  * self._hitbox_scale)
        sh = int(r.height * self._hitbox_scale)
        self.player.collision_rect.width  = sw
        self.player.collision_rect.height = sh
        self.player.collision_rect.center = r.center

    # ------------------------------------------------------------------
    def set_clock(self, clock: pygame.time.Clock):
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

        # ── Partículas (correm mesmo durante o freeze) ─────────────────
        for p in self._particles:
            p.update(dt)
        self._particles = [p for p in self._particles if p.alive]

        # ── Fase de congelamento pós-morte ─────────────────────────────
        if self._dead:
            if self._freeze_timer < FREEZE_DURATION:
                self._freeze_timer += dt
            else:
                # Após o freeze, abre o GameOverScene.
                self._open_game_over()
            return

        # ── Jogo normal ────────────────────────────────────────────────
        music_t = audio.get_music_time()

        # Vitória: música acabou
        if music_t >= self._music_duration and not self._won:
            self._trigger_victory(music_t)
            return

        self._camera_x = music_t * self._world_speed

        # Pulo contínuo
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if self.player.jump():
                audio.play_sfx(SFX_JUMP)

        self.player.update(dt)
        self._sync_player_collision()

        # Spawnar obstáculos
        while (self._next_def_idx < len(self._all_defs) and
               music_t >= (self._all_defs[self._next_def_idx].spawn_x - SCREEN_WIDTH) / self._world_speed):
            defn = self._all_defs[self._next_def_idx]
            self._next_def_idx += 1
            screen_x = defn.spawn_x - self._camera_x
            obs = defn.instantiate(screen_x)
            obs._spawn_x = defn.spawn_x
            self.active_obstacles.append(obs)

        # Reposicionar obstáculos
        for obs in self.active_obstacles:
            new_x = int(obs._spawn_x - self._camera_x)
            dx = new_x - obs.rect.x
            obs.rect.x = new_x
            obs.collision_rect.x += dx

        # Remover fora da tela
        self.active_obstacles = [o for o in self.active_obstacles if o.rect.right > 0]

        self._check_collisions()

    # ------------------------------------------------------------------
    def _check_collisions(self):
        pr = self.player.collision_rect

        for obs in self.active_obstacles:
            if not pr.colliderect(obs.collision_rect):
                continue

            if isinstance(obs, Platform):
                if self.player.velocity_y >= 0 and pr.bottom <= obs.collision_rect.top + 15:
                    self.player.rect.bottom = obs.collision_rect.top
                    self._sync_player_collision()
                    self.player.velocity_y = 0.0
                    self.player.on_ground = True
            elif isinstance(obs, Spike):
                self._trigger_death()
                return

    # ------------------------------------------------------------------
    def _trigger_death(self):
        """Inicia a sequência de morte."""
        if self._dead:
            return
        self._dead         = True
        self._freeze_timer = 0.0

        # Incrementa e guarda tentativas
        self._attempts = save_manager.increment_attempts()

        # Captura snapshot da tela atual
        self._death_snapshot = self._render_surf.copy()

        # Explode o player em 20 partículas
        cx = self.player.rect.centerx
        cy = self.player.rect.centery
        self._particles = [_Particle(cx, cy) for _ in range(20)]

        audio.stop_music()

    def _open_game_over(self):
        if self._manager is None:
            return
        progress = min(audio.get_music_time() / self._music_duration * 100, 100.0)

        from src.scenes.game_over_scene import GameOverScene
        scene = GameOverScene(
            manager      = self._manager,
            clock        = self._clock,
            phase        = self._phase,
            world_speed  = self._world_speed,
            hitbox_scale = self._hitbox_scale,
            zoom         = self._zoom,
            attempts     = self._attempts,
            progress_pct = progress,
            snapshot     = self._death_snapshot,
        )
        self._manager.change_scene(scene)

    # ------------------------------------------------------------------
    def _trigger_victory(self, music_t: float):
        self._won = True
        audio.stop_music()

        snapshot = self._render_surf.copy()

        from src.scenes.victory_scene import VictoryScene
        scene = VictoryScene(
            manager  = self._manager,
            clock    = self._clock,
            attempts = self._attempts,
            snapshot = snapshot,
        )
        self._manager.change_scene(scene)

    # ------------------------------------------------------------------
    def draw(self, screen: pygame.Surface):
        # Renderiza num surface intermediário (para suportar zoom).
        target = self._render_surf
        target.fill(COLORS["background"])
        self._draw_grid(target)

        pygame.draw.line(
            target, COLORS["ground"],
            (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y),
            width=4,
        )

        for obs in self.active_obstacles:
            obs.draw(target)

        # Não desenha o player durante o freeze (partículas tomam o lugar)
        if not self._dead:
            self.player.draw(target)

        # Partículas
        for p in self._particles:
            p.draw(target)

        # Barra de progresso no topo
        self._draw_progress_bar(target)

        # Overlay de debug
        if self._debug and self._clock:
            debug_overlay.draw(
                target,
                self._clock,
                audio.get_music_time(),
                self.player,
                self.active_obstacles,
            )

        # Aplica zoom e blit na tela real
        if self._zoom != 1.0:
            zw = int(SCREEN_WIDTH  * self._zoom)
            zh = int(SCREEN_HEIGHT * self._zoom)
            zoomed = pygame.transform.scale(target, (zw, zh))
            ox = (SCREEN_WIDTH  - zw) // 2
            oy = (SCREEN_HEIGHT - zh) // 2
            screen.fill((0, 0, 0))
            screen.blit(zoomed, (ox, oy))
        else:
            screen.blit(target, (0, 0))

    # ------------------------------------------------------------------
    def _draw_progress_bar(self, surface: pygame.Surface):
        music_t  = audio.get_music_time()
        ratio    = min(music_t / self._music_duration, 1.0) if self._music_duration > 0 else 0
        fill_w   = int(SCREEN_WIDTH * ratio)

        pygame.draw.rect(surface, _BAR_BG,  (0, 0, SCREEN_WIDTH, _BAR_H))
        if fill_w > 0:
            pygame.draw.rect(surface, _BAR_COL, (0, 0, fill_w, _BAR_H))

    # ------------------------------------------------------------------
    def _draw_grid(self, surface: pygame.Surface):
        offset = self._camera_x % GRID_SPACING if hasattr(self, '_camera_x') else 0

        x = -offset
        while x < SCREEN_WIDTH:
            pygame.draw.line(surface, COLORS["grid"], (int(x), 0), (int(x), SCREEN_HEIGHT))
            x += GRID_SPACING

        y = 0
        while y < GROUND_Y:
            pygame.draw.line(surface, COLORS["grid"], (0, y), (SCREEN_WIDTH, y))
            y += GRID_SPACING
