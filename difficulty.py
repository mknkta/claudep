"""
difficulty.py — Tela de seleção de dificuldade (DifficultyScene).

Oferece três níveis: Fácil (velocidade menor, hitbox reduzida), Médio e Difícil (zoom in).
"""

import pygame
import audio
from config import SCREEN_WIDTH, SCREEN_HEIGHT

DIFFS = [
    {"label": "Fácil",   "color": (60,200,80),  "speed": 400, "hscale": 0.7, "zoom": 1.0},
    {"label": "Médio",   "color": (220,180,20),  "speed": 600, "hscale": 1.0, "zoom": 1.0},
    {"label": "Difícil", "color": (220,60,60),   "speed": 900, "hscale": 1.0, "zoom": 1.1},
]


class DifficultyScene:
    """Tela de seleção de dificuldade para a fase escolhida."""

    def __init__(self, manager, clock, phase):
        """
        Inicializa a tela de dificuldade.

        Args:
            manager: Gerenciador de cenas para transições.
            clock: Clock do pygame.
            phase: Número da fase (1, 2 ou 3).
        """
        self._manager = manager
        self._clock   = clock
        self._phase   = phase
        self._hov     = -1

        self._tf = pygame.font.SysFont("consolas", 36, bold=True)
        self._bf = pygame.font.SysFont("consolas", 28, bold=True)
        self._hf = pygame.font.SysFont("consolas", 15)

        pw, ph = 700, 340
        self._panel = pygame.Rect((SCREEN_WIDTH-pw)//2, (SCREEN_HEIGHT-ph)//2, pw, ph)

        bw, bh = 180, 70; gap = 30; total = 3*bw+2*gap
        bx = self._panel.x + (pw-total)//2
        by = self._panel.y + 180
        self._btns = [pygame.Rect(bx+i*(bw+gap), by, bw, bh) for i in range(3)]

        self._ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self._ov.fill((0,0,0,150))

    def handle_events(self, events):
        """Processa ESC (volta ao menu) e clique para iniciar com dificuldade escolhida."""
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                import saves
                saves.reset_attempts()
                from menu import MenuScene
                self._manager.go(MenuScene(self._manager, self._clock))
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for i, r in enumerate(self._btns):
                    if r.collidepoint(pygame.mouse.get_pos()):
                        audio.play_click()
                        d = DIFFS[i]
                        from gameplay import GameplayScene
                        s = GameplayScene(d["speed"], d["hscale"], d["zoom"],
                                          self._phase, self._manager)
                        s.set_clock(self._clock)
                        self._manager.go(s)

    def update(self, dt):
        """Atualiza hover dos botões e toca som ao entrar."""
        mp      = pygame.mouse.get_pos()
        new_hov = next((i for i,r in enumerate(self._btns) if r.collidepoint(mp)), -1)
        if new_hov != self._hov and new_hov != -1:
            audio.play_hover()
        self._hov = new_hov

    def draw(self, screen):
        """Renderiza o painel de seleção de dificuldade."""
        screen.blit(self._ov, (0,0))
        pygame.draw.rect(screen, (25,20,40),   self._panel, border_radius=14)
        pygame.draw.rect(screen, (80,60,120),  self._panel, width=2, border_radius=14)

        t = self._tf.render(f"Fase {self._phase} — Dificuldade", True, (200,180,255))
        screen.blit(t, t.get_rect(centerx=self._panel.centerx, centery=self._panel.y+50))

        h = self._hf.render("ESC para voltar", True, (100,90,130))
        screen.blit(h, h.get_rect(centerx=self._panel.centerx, centery=self._panel.y+95))

        descs = ["400 px/s  •  hitbox menor", "600 px/s  •  ritmo normal", "900 px/s  •  zoom in"]
        for i, (desc, d) in enumerate(zip(descs, DIFFS)):
            s = self._hf.render(desc, True, d["color"])
            screen.blit(s, s.get_rect(centerx=self._btns[i].centerx, centery=self._panel.y+130))

        for i, (r, d) in enumerate(zip(self._btns, DIFFS)):
            hov = (i == self._hov)
            w, h = int(r.w*(1.05 if hov else 1)), int(r.h*(1.05 if hov else 1))
            br = pygame.Rect(r.centerx-w//2, r.centery-h//2, w, h)
            pygame.draw.rect(screen, (30,25,45), br, border_radius=10)
            pygame.draw.rect(screen, d["color"], br, width=3 if hov else 1, border_radius=10)
            l = self._bf.render(d["label"], True, d["color"] if hov else (160,150,180))
            screen.blit(l, l.get_rect(center=br.center))
