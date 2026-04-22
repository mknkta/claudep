import random
import pygame
import audio, saves, loader, debug
from player import Player
from obstacles import Spike, CeilingSpike, Platform, Portal
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_Y, CEILING_Y, COLORS, SPEED_MEDIUM

GRID  = 100
SFX   = "assets/sfx/jump.wav"
BAR_H = 8
BAR_C = (140, 80, 220)
BAR_B = (40,  30,  60)
FREEZE_TIME = 0.5

# Cor do teto no modo nave
CEILING_COLOR = (60, 50, 80)


class Particle:
    COLORS = [(100,80,220),(160,100,255),(80,200,255),(255,200,80),(255,255,255)]
    def __init__(self, x, y):
        self.x, self.y   = x + random.uniform(-5,5), y + random.uniform(-5,5)
        self.vx, self.vy = random.uniform(-300,300), random.uniform(-300,300)
        self.size = random.randint(5, 14)
        self.life = self.max_life = random.uniform(0.6, 1.0)
        self.color = random.choice(self.COLORS)
    def update(self, dt):
        self.vy += 600 * dt
        self.x  += self.vx * dt
        self.y  += self.vy * dt
        self.life -= dt
    @property
    def alive(self): return self.life > 0
    def draw(self, screen):
        a = max(0, int(255 * self.life / self.max_life))
        s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        s.fill((*self.color, a))
        screen.blit(s, (int(self.x - self.size//2), int(self.y - self.size//2)))


class GameplayScene:
    def __init__(self, world_speed=SPEED_MEDIUM, hitbox_scale=1.0,
                 zoom=1.0, phase=1, manager=None):
        self._manager = manager
        self._phase   = phase
        self._speed   = world_speed
        self._hscale  = hitbox_scale
        self._zoom    = zoom

        self.player = Player()
        self._apply_hscale()

        music_path, self._defs, self._duration = loader.load(world_speed, phase)
        self._idx = 0
        self._obs = []

        self._attempts = saves.get_attempts()
        audio.play_music(music_path)

        self._dead     = False
        self._freeze   = 0.0
        self._parts    = []
        self._snapshot = None
        self._paused   = False
        self._debug    = False
        self._camera_x = 0.0
        self._clock    = None
        self._surf     = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def set_clock(self, c): self._clock = c

    # ── hitbox scale ──────────────────────────────────────────────────
    def _apply_hscale(self):
        r = self.player.rect
        if self._hscale == 1.0:
            self.player.collision_rect = r; return
        sw, sh = int(r.w * self._hscale), int(r.h * self._hscale)
        self.player.collision_rect = pygame.Rect(
            r.centerx - sw//2, r.centery - sh//2, sw, sh)

    def _sync_hscale(self):
        if self._hscale == 1.0:
            self.player.collision_rect = self.player.rect; return
        r = self.player.rect
        sw, sh = int(r.w * self._hscale), int(r.h * self._hscale)
        self.player.collision_rect.size   = (sw, sh)
        self.player.collision_rect.center = r.center

    # ── events ────────────────────────────────────────────────────────
    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE: self._paused = not self._paused
                if e.key == pygame.K_F3:     self._debug  = not self._debug
                # cubo: pulo no press (não hold)
                if e.key == pygame.K_SPACE and self.player.mode == "cube":
                    if self.player.jump():
                        audio.play_sfx(SFX)

    # ── update ────────────────────────────────────────────────────────
    def update(self, dt):
        if self._paused: return

        for p in self._parts: p.update(dt)
        self._parts = [p for p in self._parts if p.alive]

        if self._dead:
            self._freeze += dt
            if self._freeze >= FREEZE_TIME:
                self._open_gameover()
            return

        t = audio.get_time()
        if t >= self._duration:
            self._win(); return

        self._camera_x = t * self._speed

        # nave: thrust ao segurar espaço
        space_held = pygame.key.get_pressed()[pygame.K_SPACE]

        self.player.update(dt, space_held=(self.player.mode == "ship" and space_held))
        self._sync_hscale()

        # colisão com teto (modo nave)
        if self.player.mode == "ship" and self.player.rect.top <= CEILING_Y:
            self._die(); return

        # spawn
        while (self._idx < len(self._defs) and
               t >= (self._defs[self._idx].spawn_x - SCREEN_WIDTH) / self._speed):
            d = self._defs[self._idx]; self._idx += 1
            obj = d.make(d.spawn_x - self._camera_x)
            if obj is not None:
                self._obs.append(obj)

        # reposicionar
        for o in self._obs:
            nx = int(o._spawn_x - self._camera_x)
            dx = nx - o.rect.x
            o.rect.x = nx
            o.collision_rect.x += dx

        self._obs = [o for o in self._obs if o.rect.right > 0]
        self._collide()

    def _collide(self):
        pr = self.player.collision_rect
        for o in self._obs:
            if not pr.colliderect(o.collision_rect): continue

            if isinstance(o, Portal):
                if not o.triggered:
                    o.triggered = True
                    self.player.set_mode(o.target_mode)

            elif isinstance(o, Platform):
                if self.player.velocity_y >= 0 and pr.bottom <= o.collision_rect.top + 15:
                    self.player.rect.bottom = o.collision_rect.top
                    self._sync_hscale()
                    self.player.velocity_y = 0.0
                    self.player.on_ground  = True

            elif isinstance(o, (Spike, CeilingSpike)):
                self._die(); return

    def _die(self):
        if self._dead: return
        self._dead     = True
        self._freeze   = 0.0
        self._attempts = saves.increment()
        self._snapshot = self._surf.copy()
        cx, cy = self.player.rect.center
        self._parts = [Particle(cx, cy) for _ in range(20)]
        audio.stop()

    def _open_gameover(self):
        if not self._manager: return
        pct = min(audio.get_time() / self._duration * 100, 100.0)
        from gameover import GameOverScene
        self._manager.go(GameOverScene(
            self._manager, self._clock, self._phase,
            self._speed, self._hscale, self._zoom,
            self._attempts, pct, self._snapshot))

    def _win(self):
        snap = self._surf.copy()
        audio.stop()
        from victory import VictoryScene
        self._manager.go(VictoryScene(self._manager, self._clock, self._attempts, snap))

    # ── draw ──────────────────────────────────────────────────────────
    def draw(self, screen):
        s = self._surf
        s.fill(COLORS["background"])
        self._grid(s)

        # teto (visível no modo nave)
        if self.player.mode == "ship":
            pygame.draw.rect(s, CEILING_COLOR, (0, 0, SCREEN_WIDTH, CEILING_Y))
            pygame.draw.line(s, (120, 100, 160), (0, CEILING_Y), (SCREEN_WIDTH, CEILING_Y), 3)

        pygame.draw.line(s, COLORS["ground"], (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 4)

        for o in self._obs: o.draw(s)
        if not self._dead: self.player.draw(s)
        for p in self._parts: p.draw(s)

        # barra de progresso
        t    = audio.get_time()
        fill = int(SCREEN_WIDTH * min(t / self._duration, 1.0)) if self._duration else 0
        pygame.draw.rect(s, BAR_B, (0, 0, SCREEN_WIDTH, BAR_H))
        if fill: pygame.draw.rect(s, BAR_C, (0, 0, fill, BAR_H))

        if self._debug and self._clock:
            debug.draw(s, self._clock, audio.get_time(), self.player, self._obs)

        if self._zoom != 1.0:
            zw, zh = int(SCREEN_WIDTH * self._zoom), int(SCREEN_HEIGHT * self._zoom)
            zoomed = pygame.transform.scale(s, (zw, zh))
            screen.fill((0,0,0))
            screen.blit(zoomed, ((SCREEN_WIDTH-zw)//2, (SCREEN_HEIGHT-zh)//2))
        else:
            screen.blit(s, (0, 0))

    def _grid(self, surface):
        off = self._camera_x % GRID
        x = -off
        while x < SCREEN_WIDTH:
            pygame.draw.line(surface, COLORS["grid"], (int(x), 0), (int(x), SCREEN_HEIGHT))
            x += GRID
        y = 0
        while y < GROUND_Y:
            pygame.draw.line(surface, COLORS["grid"], (0, y), (SCREEN_WIDTH, y))
            y += GRID
