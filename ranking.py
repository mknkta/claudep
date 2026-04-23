"""
ranking.py — Tela de ranking (RankingScene).

Exibe o top 10 de pontuações salvas em arquivo, ordenado de forma
decrescente. Jogadores com maior pontuação aparecem no topo.
"""

import pygame
import audio
import saves
from config import SCREEN_WIDTH, SCREEN_HEIGHT

BG     = (20, 18, 32)
GOLD   = (255, 215,   0)
SILVER = (192, 192, 192)
BRONZE = (205, 127,  50)
PURPLE = (140,  80, 220)
WHITE  = (220, 210, 255)
DIM    = (100,  90, 130)

MEDAL_COLORS = [GOLD, SILVER, BRONZE]


class RankingScene:
    """Tela de ranking com top 10 pontuações ordenadas de forma decrescente."""

    def __init__(self, manager, clock, highlight: str = ""):
        """
        Inicializa a tela de ranking.

        Args:
            manager: Gerenciador de cenas.
            clock: Clock do pygame.
            highlight: Nome do jogador a destacar (recém-salvo).
        """
        self._manager   = manager
        self._clock     = clock
        self._highlight = highlight
        self._ranking   = saves.get_ranking()

        self._tf = pygame.font.SysFont("consolas", 48, bold=True)
        self._rf = pygame.font.SysFont("consolas", 24, bold=True)
        self._sf = pygame.font.SysFont("consolas", 20)
        self._bf = pygame.font.SysFont("consolas", 22, bold=True)

        bw, bh = 220, 50
        self._btn = pygame.Rect(
            SCREEN_WIDTH // 2 - bw // 2,
            SCREEN_HEIGHT - 70, bw, bh)
        self._hov = False

    def handle_events(self, events):
        """Processa clique no botão de menu e tecla ESC."""
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self._btn.collidepoint(pygame.mouse.get_pos()):
                    audio.play_click()
                    self._go_menu()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self._go_menu()

    def _go_menu(self):
        """Reseta tentativas e volta ao menu principal."""
        saves.reset_attempts()
        from menu import MenuScene
        self._manager.go(MenuScene(self._manager, self._clock))

    def update(self, dt):
        """Atualiza estado de hover do botão e toca som ao entrar."""
        was_hov   = self._hov
        self._hov = self._btn.collidepoint(pygame.mouse.get_pos())
        if self._hov and not was_hov:
            audio.play_hover()

    def draw(self, screen):
        """Renderiza o painel de ranking com posições, nomes e pontuações."""
        screen.fill(BG)

        # título
        title = self._tf.render("RANKING", True, PURPLE)
        screen.blit(title, title.get_rect(centerx=SCREEN_WIDTH // 2, y=28))

        # painel central
        pw, ph = 640, 440
        panel = pygame.Rect((SCREEN_WIDTH - pw) // 2, 100, pw, ph)
        pygame.draw.rect(screen, (25, 20, 40), panel, border_radius=12)
        pygame.draw.rect(screen, (80, 60, 120), panel, width=2, border_radius=12)

        if not self._ranking:
            empty = self._sf.render("Nenhuma pontuação ainda!", True, DIM)
            screen.blit(empty, empty.get_rect(center=panel.center))
        else:
            row_h = 40
            for i, entry in enumerate(self._ranking):
                y = panel.y + 16 + i * row_h
                is_hl = entry["name"] == self._highlight

                # fundo highlight
                if is_hl:
                    hl = pygame.Rect(panel.x + 8, y + 2, panel.w - 16, row_h - 4)
                    pygame.draw.rect(screen, (50, 35, 80), hl, border_radius=6)

                # cor da posição
                if i < 3:
                    pos_col = MEDAL_COLORS[i]
                else:
                    pos_col = WHITE if is_hl else DIM

                # posição
                pos_t = self._rf.render(f"#{i+1:02d}", True, pos_col)
                screen.blit(pos_t, (panel.x + 20, y + 8))

                # nome
                name_col = (255, 220, 80) if is_hl else WHITE
                name_t = self._rf.render(entry["name"][:16], True, name_col)
                screen.blit(name_t, (panel.x + 90, y + 8))

                # pontuação alinhada à direita
                score_t = self._rf.render(f"{entry['score']:,}", True, pos_col)
                screen.blit(score_t, score_t.get_rect(
                    right=panel.right - 20, y=y + 8))

                # separador
                if i < len(self._ranking) - 1:
                    pygame.draw.line(screen, (50, 40, 70),
                                     (panel.x + 12, y + row_h),
                                     (panel.right - 12, y + row_h))

        # botão menu
        bw = int(self._btn.w * (1.05 if self._hov else 1))
        bh = int(self._btn.h * (1.05 if self._hov else 1))
        br = pygame.Rect(
            self._btn.centerx - bw // 2,
            self._btn.centery - bh // 2, bw, bh)
        pygame.draw.rect(screen, (30, 25, 45), br, border_radius=8)
        pygame.draw.rect(screen, (100, 120, 220), br,
                         width=3 if self._hov else 2, border_radius=8)
        bt = self._bf.render("Menu Principal", True,
                             (100, 120, 220) if self._hov else (160, 150, 180))
        screen.blit(bt, bt.get_rect(center=br.center))
