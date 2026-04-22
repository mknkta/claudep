# game_over_scene.py — tela de game over com painel e botões
import pygame
from src.scenes.scene import Scene
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS

BTN_W, BTN_H = 200, 55


class GameOverScene(Scene):
    def __init__(self, manager, clock, phase: int, world_speed: float,
                 hitbox_scale: float, zoom: float,
                 attempts: int, progress_pct: float,
                 snapshot: pygame.Surface):
        self._manager      = manager
        self._clock        = clock
        self._phase        = phase
        self._world_speed  = world_speed
        self._hitbox_scale = hitbox_scale
        self._zoom         = zoom
        self._attempts     = attempts
        self._progress_pct = progress_pct
        self._snapshot     = snapshot   # frame congelado do gameplay

        # Fontes
        self._big_font  = pygame.font.SysFont("consolas", 48, bold=True)
        self._mid_font  = pygame.font.SysFont("consolas", 26)
        self._btn_font  = pygame.font.SysFont("consolas", 22, bold=True)
        self._hint_font = pygame.font.SysFont("consolas", 15)

        # Painel
        pw, ph = 560, 320
        self._panel = pygame.Rect(
            (SCREEN_WIDTH  - pw) // 2,
            (SCREEN_HEIGHT - ph) // 2,
            pw, ph,
        )

        # Botões: Reiniciar e Menu Principal
        gap      = 30
        total_bw = 2 * BTN_W + gap
        bx       = self._panel.centerx - total_bw // 2
        by       = self._panel.bottom  - BTN_H - 30
        self._btn_restart = pygame.Rect(bx,          by, BTN_W, BTN_H)
        self._btn_menu    = pygame.Rect(bx + BTN_W + gap, by, BTN_W, BTN_H)
        self._hovered     = None

        # Overlay escuro
        self._overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self._overlay.fill((0, 0, 0, 170))

    # ------------------------------------------------------------------
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mp = pygame.mouse.get_pos()
                if self._btn_restart.collidepoint(mp):
                    self._restart()
                elif self._btn_menu.collidepoint(mp):
                    self._go_menu()

    def _restart(self):
        from src.scenes.gameplay_scene import GameplayScene
        scene = GameplayScene(
            world_speed  = self._world_speed,
            hitbox_scale = self._hitbox_scale,
            zoom         = self._zoom,
            phase        = self._phase,
            manager      = self._manager,
        )
        scene.set_clock(self._clock)
        self._manager.change_scene(scene)

    def _go_menu(self):
        from src.scenes.main_menu_scene import MainMenuScene
        self._manager.change_scene(MainMenuScene(self._manager, self._clock))

    # ------------------------------------------------------------------
    def update(self, dt: float):
        mp = pygame.mouse.get_pos()
        if self._btn_restart.collidepoint(mp):
            self._hovered = "restart"
        elif self._btn_menu.collidepoint(mp):
            self._hovered = "menu"
        else:
            self._hovered = None

    # ------------------------------------------------------------------
    def draw(self, screen: pygame.Surface):
        # Fundo: frame congelado do gameplay + escurecimento
        screen.blit(self._snapshot, (0, 0))
        screen.blit(self._overlay, (0, 0))

        # Painel
        pygame.draw.rect(screen, (20, 16, 35), self._panel, border_radius=14)
        pygame.draw.rect(screen, (120, 80, 180), self._panel, width=2, border_radius=14)

        # "Tentativa #N"
        attempt_surf = self._big_font.render(f"Tentativa #{self._attempts}", True, (220, 180, 255))
        screen.blit(attempt_surf, attempt_surf.get_rect(
            centerx=self._panel.centerx, centery=self._panel.y + 65))

        # "Você completou X%"
        pct_text = f"Você completou {self._progress_pct:.1f}%"
        pct_surf = self._mid_font.render(pct_text, True, (160, 140, 200))
        screen.blit(pct_surf, pct_surf.get_rect(
            centerx=self._panel.centerx, centery=self._panel.y + 130))

        # Barra de progresso mini dentro do painel
        bar_w, bar_h = 400, 12
        bar_x = self._panel.centerx - bar_w // 2
        bar_y = self._panel.y + 160
        pygame.draw.rect(screen, (50, 40, 70), (bar_x, bar_y, bar_w, bar_h), border_radius=6)
        fill = int(bar_w * self._progress_pct / 100)
        if fill > 0:
            pygame.draw.rect(screen, (140, 80, 220), (bar_x, bar_y, fill, bar_h), border_radius=6)

        # Botões
        self._draw_btn(screen, self._btn_restart, "Reiniciar",     (80, 200, 120), self._hovered == "restart")
        self._draw_btn(screen, self._btn_menu,    "Menu Principal", (100, 120, 220), self._hovered == "menu")

    def _draw_btn(self, screen, rect, label, color, hovered):
        scale = 1.05 if hovered else 1.0
        w = int(rect.width  * scale)
        h = int(rect.height * scale)
        r = pygame.Rect(rect.centerx - w // 2, rect.centery - h // 2, w, h)
        pygame.draw.rect(screen, (30, 25, 45), r, border_radius=8)
        pygame.draw.rect(screen, color, r, width=2 if not hovered else 3, border_radius=8)
        text = self._btn_font.render(label, True, color if hovered else (160, 150, 180))
        screen.blit(text, text.get_rect(center=r.center))
