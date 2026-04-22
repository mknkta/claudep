# difficulty_select_scene.py — painel de seleção de dificuldade
import pygame
from src.scenes.scene import Scene
from config import SCREEN_WIDTH, SCREEN_HEIGHT

DIFFICULTIES = [
    {"label": "Fácil",  "color": (60,  200,  80), "speed": 400, "hitbox": 0.7, "zoom": 1.0},
    {"label": "Médio",  "color": (220, 180,  20), "speed": 600, "hitbox": 1.0, "zoom": 1.0},
    {"label": "Difícil","color": (220,  60,  60), "speed": 900, "hitbox": 1.0, "zoom": 1.1},
]


class DifficultySelectScene(Scene):
    def __init__(self, manager, clock, phase: int):
        self._manager = manager
        self._clock   = clock
        self._phase   = phase

        self._title_font = pygame.font.SysFont("consolas", 36, bold=True)
        self._btn_font   = pygame.font.SysFont("consolas", 28, bold=True)
        self._hint_font  = pygame.font.SysFont("consolas", 15)

        # Painel central
        pw, ph  = 700, 340
        self._panel = pygame.Rect(
            (SCREEN_WIDTH  - pw) // 2,
            (SCREEN_HEIGHT - ph) // 2,
            pw, ph,
        )

        # Botões de dificuldade
        bw, bh = 180, 70
        gap     = 30
        total_w = 3 * bw + 2 * gap
        bx      = self._panel.x + (pw - total_w) // 2
        by      = self._panel.y + 180
        self._btns = [
            pygame.Rect(bx + i * (bw + gap), by, bw, bh)
            for i in range(3)
        ]
        self._hovered = -1

        # Sobreposição escura.
        self._overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self._overlay.fill((0, 0, 0, 150))

    # ------------------------------------------------------------------
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from src.scenes.main_menu_scene import MainMenuScene
                self._manager.change_scene(MainMenuScene(self._manager, self._clock))

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mp = pygame.mouse.get_pos()
                for i, rect in enumerate(self._btns):
                    if rect.collidepoint(mp):
                        diff = DIFFICULTIES[i]
                        self._start_game(diff)

    def _start_game(self, diff: dict):
        from src.scenes.gameplay_scene import GameplayScene
        scene = GameplayScene(
            world_speed    = diff["speed"],
            hitbox_scale   = diff["hitbox"],
            zoom           = diff["zoom"],
            phase          = self._phase,
            manager        = self._manager,
        )
        scene.set_clock(self._clock)
        self._manager.change_scene(scene)

    # ------------------------------------------------------------------
    def update(self, dt: float):
        mp = pygame.mouse.get_pos()
        self._hovered = -1
        for i, rect in enumerate(self._btns):
            if rect.collidepoint(mp):
                self._hovered = i

    # ------------------------------------------------------------------
    def draw(self, screen: pygame.Surface):
        # Fundo escurecido
        screen.blit(self._overlay, (0, 0))

        # Painel
        pygame.draw.rect(screen, (25, 20, 40), self._panel, border_radius=14)
        pygame.draw.rect(screen, (80, 60, 120), self._panel, width=2, border_radius=14)

        # Título do painel
        title = self._title_font.render(f"Fase {self._phase} — Dificuldade", True, (200, 180, 255))
        screen.blit(title, title.get_rect(centerx=self._panel.centerx,
                                          centery=self._panel.y + 50))

        hint = self._hint_font.render("ESC para voltar", True, (100, 90, 130))
        screen.blit(hint, hint.get_rect(centerx=self._panel.centerx,
                                        centery=self._panel.y + 95))

        # Descrições de velocidade
        desc_y = self._panel.y + 130
        descs  = ["400 px/s  •  hitbox menor", "600 px/s  •  ritmo normal", "900 px/s  •  zoom in"]
        for i, (desc, diff) in enumerate(zip(descs, DIFFICULTIES)):
            cx = self._btns[i].centerx
            d  = self._hint_font.render(desc, True, diff["color"])
            screen.blit(d, d.get_rect(centerx=cx, centery=desc_y))

        # Botões
        for i, (rect, diff) in enumerate(zip(self._btns, DIFFICULTIES)):
            hov   = (i == self._hovered)
            scale = 1.05 if hov else 1.0
            w     = int(rect.width  * scale)
            h     = int(rect.height * scale)
            r     = pygame.Rect(rect.centerx - w // 2, rect.centery - h // 2, w, h)

            pygame.draw.rect(screen, (30, 25, 45), r, border_radius=10)
            pygame.draw.rect(screen, diff["color"], r,
                             width=3 if hov else 1, border_radius=10)

            label = self._btn_font.render(diff["label"], True,
                                          diff["color"] if hov else (160, 150, 180))
            screen.blit(label, label.get_rect(center=r.center))
