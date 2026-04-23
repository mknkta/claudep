"""
name_input.py — Tela de entrada de nome (NameInputScene).

Exibida após game over ou vitória para que o jogador informe seu nome
antes de salvar a pontuação no ranking.
"""

import pygame
import audio
import saves
from config import SCREEN_WIDTH, SCREEN_HEIGHT

MAX_LEN = 16
BG_OV   = (0, 0, 0, 180)


class NameInputScene:
    """Tela de entrada de nome exibida após game over ou vitória.

    O jogador digita seu nome e confirma para salvar a pontuação
    no ranking persistido em arquivo JSON.
    """

    def __init__(self, manager, clock, score: int, snapshot):
        """
        Inicializa a tela de entrada de nome.

        Args:
            manager: Gerenciador de cenas.
            clock: Clock do pygame.
            score: Pontuação obtida na partida.
            snapshot: Surface com o último frame (exibida ao fundo).
        """
        self._manager  = manager
        self._clock    = clock
        self._score    = score
        self._snap     = snapshot
        self._name     = ""
        self._cursor   = True
        self._blink    = 0.0

        self._tf = pygame.font.SysFont("consolas", 42, bold=True)
        self._mf = pygame.font.SysFont("consolas", 28)
        self._sf = pygame.font.SysFont("consolas", 22)

        pw, ph = 520, 300
        self._panel = pygame.Rect(
            (SCREEN_WIDTH - pw) // 2, (SCREEN_HEIGHT - ph) // 2, pw, ph)

        bw, bh = 200, 50
        self._btn = pygame.Rect(
            SCREEN_WIDTH // 2 - bw // 2,
            self._panel.bottom - bh - 24,
            bw, bh)

        self._hov = False
        self._ov  = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self._ov.fill(BG_OV)

    def handle_events(self, events):
        """Processa digitação do nome, backspace, Enter e clique no botão."""
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    self._confirm()
                elif e.key == pygame.K_BACKSPACE:
                    self._name = self._name[:-1]
                elif len(self._name) < MAX_LEN:
                    ch = e.unicode
                    if ch.isprintable() and ch.strip():
                        self._name += ch

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self._btn.collidepoint(pygame.mouse.get_pos()):
                    audio.play_click()
                    self._confirm()

    def _confirm(self):
        """Salva o nome e pontuação no ranking e vai para a tela de ranking."""
        name = self._name.strip() or "Anônimo"
        saves.add_to_ranking(name, self._score)
        from ranking import RankingScene
        self._manager.go(RankingScene(self._manager, self._clock, highlight=name))

    def update(self, dt):
        """Atualiza piscar do cursor e hover do botão."""
        was_hov      = self._hov
        self._blink  = (self._blink + dt) % 1.0
        self._cursor = self._blink < 0.5
        self._hov    = self._btn.collidepoint(pygame.mouse.get_pos())
        if self._hov and not was_hov:
            audio.play_hover()

    def draw(self, screen):
        """Renderiza o painel de entrada de nome com caixa de texto e botão."""
        if self._snap:
            screen.blit(self._snap, (0, 0))
        screen.blit(self._ov, (0, 0))

        pygame.draw.rect(screen, (20, 16, 35),   self._panel, border_radius=14)
        pygame.draw.rect(screen, (140, 80, 220), self._panel, width=2, border_radius=14)

        title = self._tf.render("Salvar pontuação", True, (220, 180, 255))
        screen.blit(title, title.get_rect(
            centerx=self._panel.centerx, centery=self._panel.y + 45))

        score_t = self._mf.render(f"Pontuação: {self._score:,}", True, (255, 220, 80))
        screen.blit(score_t, score_t.get_rect(
            centerx=self._panel.centerx, centery=self._panel.y + 105))

        # caixa de texto
        box = pygame.Rect(self._panel.x + 40, self._panel.y + 148, self._panel.w - 80, 46)
        pygame.draw.rect(screen, (35, 28, 55), box, border_radius=8)
        pygame.draw.rect(screen, (100, 80, 160), box, width=2, border_radius=8)

        display = self._name + ("|" if self._cursor else " ")
        name_t  = self._mf.render(display, True, (230, 220, 255))
        screen.blit(name_t, name_t.get_rect(midleft=(box.x + 12, box.centery)))

        hint = self._sf.render("Digite seu nome e pressione Enter", True, (100, 90, 130))
        screen.blit(hint, hint.get_rect(
            centerx=self._panel.centerx, centery=self._panel.y + 215))

        # botão confirmar
        bw = int(self._btn.w * (1.05 if self._hov else 1))
        bh = int(self._btn.h * (1.05 if self._hov else 1))
        br = pygame.Rect(
            self._btn.centerx - bw // 2,
            self._btn.centery - bh // 2, bw, bh)
        col = (80, 200, 120)
        pygame.draw.rect(screen, (30, 25, 45), br, border_radius=8)
        pygame.draw.rect(screen, col, br, width=3 if self._hov else 2, border_radius=8)
        bt = self._sf.render("Confirmar", True, col if self._hov else (160, 150, 180))
        screen.blit(bt, bt.get_rect(center=br.center))
