"""
main.py — Ponto de entrada do jogo Developer Life / Geometry Dash.

Inicializa o pygame, cria o gerenciador de cenas (Manager) e mantém
o loop principal de eventos, atualização e renderização.
"""

import sys
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


class Manager:
    """Gerenciador de cenas: mantém a cena ativa e delega eventos, update e draw."""
    def __init__(self, scene):
        """Inicializa o gerenciador com a cena inicial (pode ser None)."""
        self.scene = scene

    def go(self, new_scene):
        """Troca a cena ativa."""
        self.scene = new_scene

    def update(self, dt):
        """Delega update à cena ativa."""
        self.scene.update(dt)

    def draw(self, screen):
        """Delega draw à cena ativa."""
        self.scene.draw(screen)

    def events(self, evts):
        """Delega handle_events à cena ativa."""
        self.scene.handle_events(evts)

def main():
    """Inicializa o pygame e executa o loop principal do jogo."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Meu Jogo")
    clock  = pygame.time.Clock()

    from menu import MenuScene
    manager = Manager(None)
    manager.go(MenuScene(manager, clock))

    while True:
        dt = clock.tick(FPS) / 1000.0
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        manager.events(events)
        manager.update(dt)
        manager.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
