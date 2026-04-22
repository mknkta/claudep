# main.py — ponto de entrada do jogo

import sys
import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.scenes.scene_manager import SceneManager
from src.scenes.main_menu_scene import MainMenuScene


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Meu Jogo — Fase 1")

    clock = pygame.time.Clock()

    manager = SceneManager(MainMenuScene(None, clock))
    # Injeta o manager na cena depois de criá-lo para evitar referência circular.
    manager.current_scene._manager = manager

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if not running:
            break

        manager.handle_events(events)
        manager.update(dt)
        manager.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
