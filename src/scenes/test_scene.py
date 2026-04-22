# test_scene.py — cena placeholder para validar o pipeline de renderização
#
# Objetivo: provar que fundo, linha do chão e um retângulo aparecem na tela.
# Quando o jogo real começar, esta cena pode ser removida ou virar um sandbox.

import pygame
from src.scenes.scene import Scene
from config import COLORS, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT


class TestScene(Scene):
    def __init__(self):
        # Retângulo estático no centro da tela — só para confirmar que draw() funciona.
        # pygame.Rect(x, y, largura, altura); centralizamos manualmente.
        rect_w, rect_h = 100, 100
        self.test_rect = pygame.Rect(
            (SCREEN_WIDTH  - rect_w) // 2,
            (SCREEN_HEIGHT - rect_h) // 2,
            rect_w,
            rect_h,
        )

    def handle_events(self, events):
        # Nesta cena de teste não há interação além de fechar a janela,
        # que já é tratada no loop principal em main.py.
        pass

    def update(self, dt):
        # Nada se move aqui — dt está disponível quando precisarmos animar.
        pass

    def draw(self, screen):
        # 1. Pinta o fundo inteiro com a cor "background".
        screen.fill(COLORS["background"])

        # 2. Desenha a linha do chão: vai da borda esquerda à direita em GROUND_Y.
        pygame.draw.line(
            screen,
            COLORS["ground"],
            (0, GROUND_Y),
            (SCREEN_WIDTH, GROUND_Y),
            width=4,  # espessura da linha em pixels
        )

        # 3. Desenha o retângulo de teste em branco no centro.
        pygame.draw.rect(screen, (220, 220, 220), self.test_rect)
