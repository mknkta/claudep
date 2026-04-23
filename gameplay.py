"""
gameplay.py — Cena principal de jogo (GameplayScene).

Gerencia o loop de física, spawn de obstáculos, detecção de colisão
via pygame.sprite.spritecollide e transição entre cenas.
"""

import random
import pygame
import audio, saves, loader, debug
from player import Player
from obstacles import Spike, CeilingSpike, Platform, Portal, GravityPortal, GravityFlipPortal, Wall, SpikeBall, PulseLaser
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_Y, CEILING_Y, COLORS, SPEED_MEDIUM

GRID  = 100
SFX   = "assets/sfx/jump.wav"
BAR_H = 8
BAR_C = (140, 80, 220)
BAR_B = (40,  30,  60)
FREEZE_TIME = 0.5

CEILING_COLOR = (60, 50, 80)


def _collision_check(player_spr: Player, obs_spr) -> bool:
    """Função de colisão customizada para spritecollide.

    Usa collision_rect de ambos os sprites, e para Wall chama
    o método especializado que verifica os dois segmentos do muro.

    Args:
        player_spr: Sprite do jogador.
        obs_spr: Sprite do obstáculo.

    Returns:
        True se há colisão, False caso contrário.
    """
    return obs_spr.collides_with(player_spr.collision_rect)


class Particle:
    """Partícula de explosão emitida ao morrer."""

    COLORS = [(100,80,220),(160,100,255),(80,200,255),(255,200,80),(255,255,255)]

    def __init__(self, x, y):
        """Inicializa partícula com posição, velocidade e cor aleatórias."""
        self.x, self.y   = x + random.uniform(-5,5), y + random.uniform(-5,5)
        self.vx, self.vy = random.uniform(-300,300), random.uniform(-300,300)
        self.size = random.randint(5, 14)
        self.life = self.max_life = random.uniform(0.6, 1.0)
        self.color = random.choice(self.COLORS)

    def update(self, dt):
        """Atualiza posição e tempo de vida da partícula."""
        self.vy += 600 * dt
        self.x  += self.vx * dt
        self.y  += self.vy * dt
        self.life -= dt

    @property
    def alive(self):
        """Retorna True enquanto a partícula ainda está visível."""
        return self.life > 0

    def draw(self, screen):
        """Desenha a partícula com alpha proporcional ao tempo de vida."""
        a = max(0, int(255 * self.life / self.max_life))
        s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        s.fill((*self.color, a))
        screen.blit(s, (int(self.x - self.size//2), int(self.y - self.size//2)))


class GameplayScene:
    """Cena principal do jogo.

    Controla o spawn de obstáculos sincronizado com a música, a física
    do player, a detecção de colisão e a transição para game over ou vitória.
    """

    def __init__(self, world_speed=SPEED_MEDIUM, hitbox_scale=1.0,
                 zoom=1.0, phase=1, manager=None):
        """
        Inicializa a cena de gameplay.

        Args:
            world_speed: Velocidade de rolagem do mundo em pixels/segundo.
            hitbox_scale: Fator de escala da hitbox do player (0.7 = mais fácil).
            zoom: Fator de zoom da câmera (>1 aproxima).
            phase: Número da fase (1, 2 ou 3).
            manager: Gerenciador de cenas para transições.
        """
        self._manager = manager
        self._phase   = phase
        self._speed   = world_speed
        self._hscale  = hitbox_scale
        self._zoom    = zoom

        self.player = Player()
        self._apply_hscale()

        music_path, self._defs, self._duration = loader.load(world_speed, phase)
        self._idx = 0
        self._obs_group = pygame.sprite.Group()   # grupo de obstáculos ativos

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

    def set_clock(self, c):
        """Define o clock do pygame para exibição de debug."""
        self._clock = c

    # ── hitbox scale ──────────────────────────────────────────────────
    def _apply_hscale(self):
        """Aplica o fator de escala à hitbox do player na inicialização."""
        r = self.player.rect
        if self._hscale == 1.0:
            self.player.collision_rect = r
            return
        sw, sh = int(r.w * self._hscale), int(r.h * self._hscale)
        self.player.collision_rect = pygame.Rect(
            r.centerx - sw//2, r.centery - sh//2, sw, sh)

    def _sync_hscale(self):
        """Mantém o collision_rect centrado no player após cada movimento."""
        if self._hscale == 1.0:
            self.player.collision_rect = self.player.rect
            return
        r = self.player.rect
        sw, sh = int(r.w * self._hscale), int(r.h * self._hscale)
        self.player.collision_rect.size   = (sw, sh)
        self.player.collision_rect.center = r.center

    # ── events ────────────────────────────────────────────────────────
    def handle_events(self, events):
        """Processa eventos de teclado: pausa, debug e controle do player."""
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self._paused = not self._paused
                if e.key == pygame.K_F3:
                    self._debug  = not self._debug
                if e.key == pygame.K_SPACE and self.player.mode == "cube":
                    if self.player.jump():
                        audio.play_sfx(SFX)
                elif e.key == pygame.K_SPACE and self.player.mode == "gravity_flip":
                    self.player.flip_gravity()
                    audio.play_sfx(SFX)

    # ── update ────────────────────────────────────────────────────────
    def update(self, dt):
        """Atualiza física, obstáculos e verifica colisões a cada frame."""
        if self._paused:
            return

        for p in self._parts:
            p.update(dt)
        self._parts = [p for p in self._parts if p.alive]

        if self._dead:
            self._freeze += dt
            if self._freeze >= FREEZE_TIME:
                self._open_gameover()
            return

        t = audio.get_time()
        if t >= self._duration:
            self._win()
            return

        self._camera_x = t * self._speed

        space_held = pygame.key.get_pressed()[pygame.K_SPACE]
        self.player.update(dt, space_held=space_held)
        self._sync_hscale()

        # spawn de novos obstáculos sincronizado com a música
        while (self._idx < len(self._defs) and
               t >= (self._defs[self._idx].spawn_x - SCREEN_WIDTH) / self._speed):
            d = self._defs[self._idx]
            self._idx += 1
            obj = d.make(d.spawn_x - self._camera_x)
            if obj is not None:
                self._obs_group.add(obj)

        # reposicionar obstáculos conforme câmera avança
        for o in self._obs_group.sprites():
            nx = int(o._spawn_x - self._camera_x)
            dx = nx - o.rect.x
            o.rect.x = nx
            if isinstance(o, SpikeBall):
                o.update_y(t)
                o._sync()
            elif isinstance(o, Wall):
                o._sync()
            elif isinstance(o, PulseLaser):
                o.update(t)
                o._sync()
            else:
                o.collision_rect.x += dx

        # remover obstáculos que saíram da tela pela esquerda
        for o in list(self._obs_group):
            if o.rect.right <= 0:
                o.kill()

        self._collide()

    def _collide(self):
        """Detecta colisões via spritecollide e aplica efeitos por tipo de obstáculo."""
        hits = pygame.sprite.spritecollide(
            self.player, self._obs_group, False, _collision_check)

        for o in hits:
            if isinstance(o, Wall):
                # colisão com muro verificada internamente em collides_with
                # self._die(); return
                continue

            if isinstance(o, GravityPortal):
                if not o.triggered and self.player._grav_cooldown <= 0:
                    o.triggered = True
                    self.player.invert_gravity()

            elif isinstance(o, GravityFlipPortal):
                if not o.triggered:
                    o.triggered = True
                    self.player.set_mode("gravity_flip")
                    self.player.gravity_direction = 1
                    self.player.velocity_y = 0.0

            elif isinstance(o, Portal):
                if not o.triggered:
                    o.triggered = True
                    self.player.set_mode(o.target_mode)

            elif isinstance(o, Platform):
                if (self.player.velocity_y >= 0 and
                        self.player.collision_rect.bottom <= o.collision_rect.top + 15):
                    self.player.rect.bottom = o.collision_rect.top
                    self._sync_hscale()
                    self.player.velocity_y = 0.0
                    self.player.on_ground  = True

            elif isinstance(o, PulseLaser):
                if o.active:
                    self._die()
                    return

            elif isinstance(o, (Spike, CeilingSpike, SpikeBall)):
                self._die()
                return

    def _die(self):
        """Inicia a sequência de morte: partículas, snapshot e para a música."""
        if self._dead:
            return
        self._dead     = True
        self._freeze   = 0.0
        self._attempts = saves.increment()
        self._snapshot = self._surf.copy()
        cx, cy = self.player.rect.center
        self._parts = [Particle(cx, cy) for _ in range(20)]
        audio.stop()

    def _open_gameover(self):
        """Transiciona para a tela de game over."""
        if not self._manager:
            return
        pct = min(audio.get_time() / self._duration * 100, 100.0)
        from gameover import GameOverScene
        self._manager.go(GameOverScene(
            self._manager, self._clock, self._phase,
            self._speed, self._hscale, self._zoom,
            self._attempts, pct, self._snapshot))

    def _win(self):
        """Transiciona para a tela de vitória."""
        snap = self._surf.copy()
        audio.stop()
        from victory import VictoryScene
        self._manager.go(VictoryScene(
            self._manager, self._clock, self._attempts, self._phase, snap))

    # ── draw ──────────────────────────────────────────────────────────
    def draw(self, screen):
        """Renderiza o cenário, obstáculos, player, partículas e HUD."""
        s = self._surf
        s.fill(COLORS["background"])
        self._grid(s)

        if self.player.mode == "ship":
            pygame.draw.rect(s, CEILING_COLOR, (0, 0, SCREEN_WIDTH, CEILING_Y))
            pygame.draw.line(s, (120, 100, 160), (0, CEILING_Y), (SCREEN_WIDTH, CEILING_Y), 3)
            SCOL = (255, 80, 30)
            sh, sw = 18, 24
            for i in range(SCREEN_WIDTH // sw + 2):
                cx = i * sw - int(self._camera_x % sw)
                pts = [(cx, CEILING_Y), (cx + sw, CEILING_Y), (cx + sw // 2, CEILING_Y + sh)]
                pygame.draw.polygon(s, SCOL, pts)
            for i in range(SCREEN_WIDTH // sw + 2):
                cx = i * sw - int(self._camera_x % sw)
                pts = [(cx, GROUND_Y), (cx + sw, GROUND_Y), (cx + sw // 2, GROUND_Y - sh)]
                pygame.draw.polygon(s, SCOL, pts)

        pygame.draw.line(s, COLORS["ground"], (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 4)

        for o in self._obs_group.sprites():
            o.draw(s)
        if not self._dead:
            self.player.draw(s)
        for p in self._parts:
            p.draw(s)

        # barra de progresso da fase
        t    = audio.get_time()
        fill = int(SCREEN_WIDTH * min(t / self._duration, 1.0)) if self._duration else 0
        pygame.draw.rect(s, BAR_B, (0, 0, SCREEN_WIDTH, BAR_H))
        if fill:
            pygame.draw.rect(s, BAR_C, (0, 0, fill, BAR_H))

        if self._debug and self._clock:
            debug.draw(s, self._clock, audio.get_time(), self.player, self._obs_group.sprites())

        if self._zoom != 1.0:
            zw, zh = int(SCREEN_WIDTH * self._zoom), int(SCREEN_HEIGHT * self._zoom)
            zoomed = pygame.transform.scale(s, (zw, zh))
            screen.fill((0,0,0))
            screen.blit(zoomed, ((SCREEN_WIDTH-zw)//2, (SCREEN_HEIGHT-zh)//2))
        else:
            screen.blit(s, (0, 0))

    def _grid(self, surface):
        """Desenha a grade de fundo sincronizada com a câmera."""
        off = self._camera_x % GRID
        x = -off
        while x < SCREEN_WIDTH:
            pygame.draw.line(surface, COLORS["grid"], (int(x), 0), (int(x), SCREEN_HEIGHT))
            x += GRID
        y = 0
        while y < GROUND_Y:
            pygame.draw.line(surface, COLORS["grid"], (0, y), (SCREEN_WIDTH, y))
            y += GRID
