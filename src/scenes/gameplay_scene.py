# gameplay_scene.py — cena principal da Fase 1 (modo Cubo)
#
# Esta cena orquestra:
#   - O Player (cubo com pulo único e rotação).
#   - A grade de fundo que rola para criar ilusão de movimento.
#   - O chão sólido.
#   - Leitura de input (Espaço → pular, ESC → sair).

import pygame
from src.scenes.scene import Scene
from src.entities.player import Player
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    GROUND_Y, COLORS, SPEED_MEDIUM,
)

# Espaçamento entre as linhas verticais da grade de fundo (pixels).
GRID_SPACING = 100


class GameplayScene(Scene):
    def __init__(self):
        self.player = Player()

        # Velocidade com que o mundo se move para a esquerda (pixels/segundo).
        # Representamos a corrida do personagem movendo o cenário — o player
        # fica sempre na mesma posição horizontal na tela.
        self.world_speed: float = SPEED_MEDIUM

        # camera_x acumula quantos pixels o mundo já "rolou" desde o início.
        # Usamos ele para calcular onde cada linha da grade deve ser desenhada,
        # criando o efeito de rolagem contínua.
        self._camera_x: float = 0.0

    # ------------------------------------------------------------------
    # HANDLE EVENTS
    # ------------------------------------------------------------------
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Espaço aciona o pulo. O método jump() decide se é possível.
                    self.player.jump()

                elif event.key == pygame.K_ESCAPE:
                    # ESC encerra o jogo. Futuramente voltará ao menu principal.
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    def update(self, dt: float):
        # Avança a "câmera" proporcionalmente à velocidade e ao delta time.
        # dt em segundos garante que a velocidade seja igual independente do FPS.
        # Ex: world_speed=600, dt=1/60 → câmera avança 10px por frame.
        self._camera_x += self.world_speed * dt

        # Atualiza a física e a animação do player.
        self.player.update(dt)

    # ------------------------------------------------------------------
    # DRAW
    # ------------------------------------------------------------------
    def draw(self, screen: pygame.Surface):
        # 1. Fundo sólido.
        screen.fill(COLORS["background"])

        # 2. Grade de fundo rolante — cria ilusão de profundidade e movimento.
        self._draw_grid(screen)

        # 3. Linha do chão.
        pygame.draw.line(
            screen,
            COLORS["ground"],
            (0, GROUND_Y),
            (SCREEN_WIDTH, GROUND_Y),
            width=4,
        )

        # 4. Player por cima de tudo.
        self.player.draw(screen)

    # ------------------------------------------------------------------
    # HELPER — grade rolante
    # ------------------------------------------------------------------
    def _draw_grid(self, screen: pygame.Surface):
        # camera_x % GRID_SPACING dá o offset atual dentro de um "bloco" da grade.
        # Ao subtrair esse offset de cada linha, elas parecem deslizar para a
        # esquerda de forma contínua e cíclica, sem saltos.
        offset = self._camera_x % GRID_SPACING

        x = -offset
        while x < SCREEN_WIDTH:
            pygame.draw.line(
                screen,
                COLORS["grid"],
                (int(x), 0),
                (int(x), SCREEN_HEIGHT),
            )
            x += GRID_SPACING

        # Linhas horizontais (estáticas) completam a grade.
        y = 0
        while y < GROUND_Y:
            pygame.draw.line(
                screen,
                COLORS["grid"],
                (0, y),
                (SCREEN_WIDTH, y),
            )
            y += GRID_SPACING
