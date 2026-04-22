# main.py — ponto de entrada do jogo
#
# Responsabilidades:
#   1. Inicializar o Pygame e criar a janela.
#   2. Montar o SceneManager com a cena inicial.
#   3. Rodar o loop principal: eventos → update → draw → flip.

import sys
import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.scenes.scene_manager import SceneManager
from src.scenes.test_scene import TestScene


def main():
    # --- Inicialização ---
    pygame.init()

    # display.set_mode devolve a Surface principal (a "tela").
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Meu Jogo")

    # Clock controla o FPS e fornece o delta time entre frames.
    clock = pygame.time.Clock()

    # Cria o gerenciador de cenas já apontando para a cena de teste.
    manager = SceneManager(TestScene())

    # --- Loop principal ---
    running = True
    while running:
        # clock.tick(FPS) dorme o tempo necessário para não ultrapassar 60 FPS
        # e retorna quantos milissegundos passaram desde o frame anterior.
        dt = clock.tick(FPS) / 1000.0  # converte ms → segundos

        # Coleta todos os eventos gerados neste frame (teclado, mouse, fechar janela…)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                # Usuário clicou no X da janela.
                running = False

        if not running:
            break  # sai antes de update/draw para evitar frame extra

        # Delega eventos e atualização para a cena ativa.
        manager.handle_events(events)
        manager.update(dt)

        # Delega o desenho; draw() deve cobrir a tela inteira antes do flip.
        manager.draw(screen)

        # Envia o frame renderizado para o monitor (double buffering).
        pygame.display.flip()

    # --- Encerramento ---
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
