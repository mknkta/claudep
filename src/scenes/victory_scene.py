# victory_scene.py — tela de vitória com flash branco e animação de escala
import math
import pygame
from src.scenes.scene import Scene
from config import SCREEN_WIDTH, SCREEN_HEIGHT

FLASH_DURATION = 0.3   # segundos do flash branco
ANIM_DURATION  = 0.8   # segundos da animação do texto


class VictoryScene(Scene):
    def __init__(self, manager, clock, attempts: int, snapshot: pygame.Surface):
        self._manager  = manager
        self._clock    = clock
        self._attempts = attempts
        self._snapshot = snapshot

        self._elapsed  = 0.0

        self._big_font  = pygame.font.SysFont("consolas", 72, bold=True)
        self._mid_font  = pygame.font.SysFont("consolas", 28)
        self._btn_font  = pygame.font.SysFont("consolas", 22, bold=True)

        # Pré-renderiza o texto "LEVEL COMPLETE" grande.
        self._title_surf = self._big_font.render("LEVEL COMPLETE", True, (255, 230, 80))

        pw, ph  = 260, 55
        self._btn_menu = pygame.Rect(
            (SCREEN_WIDTH  - pw) // 2,
            SCREEN_HEIGHT // 2 + 140,
            pw, ph,
        )
        self._hovered = False

    # ------------------------------------------------------------------
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._elapsed > FLASH_DURATION and self._btn_menu.collidepoint(pygame.mouse.get_pos()):
                    from src.scenes.main_menu_scene import MainMenuScene
                    self._manager.change_scene(MainMenuScene(self._manager, self._clock))

    # ------------------------------------------------------------------
    def update(self, dt: float):
        self._elapsed += dt
        self._hovered = self._btn_menu.collidepoint(pygame.mouse.get_pos())

    # ------------------------------------------------------------------
    def draw(self, screen: pygame.Surface):
        screen.blit(self._snapshot, (0, 0))

        # ── Flash branco ──────────────────────────────────────────────
        if self._elapsed < FLASH_DURATION:
            alpha = int(255 * (1 - self._elapsed / FLASH_DURATION))
            flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash.fill((255, 255, 255))
            flash.set_alpha(alpha)
            screen.blit(flash, (0, 0))
            return   # só mostra o flash durante os primeiros 0.3s

        # ── Overlay escuro após o flash ───────────────────────────────
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # ── Animação de escala do título ──────────────────────────────
        # t vai de 0→1 durante ANIM_DURATION após o flash.
        t = min((self._elapsed - FLASH_DURATION) / ANIM_DURATION, 1.0)

        # Easing: cresce até 1.2x nos primeiros 70%, volta a 1.0x nos 30% finais.
        if t < 0.7:
            scale = 0.1 + (1.2 - 0.1) * (t / 0.7)
        else:
            scale = 1.2 - (1.2 - 1.0) * ((t - 0.7) / 0.3)

        w = int(self._title_surf.get_width()  * scale)
        h = int(self._title_surf.get_height() * scale)
        if w > 0 and h > 0:
            scaled = pygame.transform.scale(self._title_surf, (w, h))
            screen.blit(scaled, scaled.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))

        # ── Subtítulo e botão (só após animação) ─────────────────────
        if t >= 1.0:
            sub = self._mid_font.render(
                f"Venceu em {self._attempts} tentativa{'s' if self._attempts != 1 else ''}!",
                True, (200, 180, 255),
            )
            screen.blit(sub, sub.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2 + 60))

            # Botão Menu Principal
            scale_b = 1.05 if self._hovered else 1.0
            bw = int(self._btn_menu.width  * scale_b)
            bh = int(self._btn_menu.height * scale_b)
            br = pygame.Rect(self._btn_menu.centerx - bw // 2,
                             self._btn_menu.centery - bh // 2, bw, bh)
            pygame.draw.rect(screen, (30, 25, 45), br, border_radius=8)
            pygame.draw.rect(screen, (100, 120, 220), br,
                             width=3 if self._hovered else 1, border_radius=8)
            btn_text = self._btn_font.render("Menu Principal", True,
                                             (100, 120, 220) if self._hovered else (160, 150, 180))
            screen.blit(btn_text, btn_text.get_rect(center=br.center))
