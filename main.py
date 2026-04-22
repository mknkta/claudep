import sys
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Manager:
    def __init__(self, scene):
        self.scene = scene
    def go(self, new_scene):
        self.scene = new_scene
    def update(self, dt):   self.scene.update(dt)
    def draw(self, screen): self.scene.draw(screen)
    def events(self, evts): self.scene.handle_events(evts)

def main():
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
