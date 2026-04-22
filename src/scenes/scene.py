# scene.py — classe base abstrata para todas as cenas do jogo
#
# Por que usar uma classe abstrata?
# Garante que toda cena nova implemente os três métodos obrigatórios.
# O SceneManager pode chamar esses métodos sem saber qual cena está ativa.

from abc import ABC, abstractmethod


class Scene(ABC):
    """Interface que toda cena deve seguir."""

    @abstractmethod
    def handle_events(self, events):
        """Recebe a lista de eventos pygame do frame atual.

        Parâmetros:
            events: lista retornada por pygame.event.get()
        """
        pass

    @abstractmethod
    def update(self, dt):
        """Atualiza a lógica da cena.

        Parâmetros:
            dt: delta time em segundos desde o último frame.
                Multiplicar velocidades por dt torna o jogo
                independente do FPS (ex: vel * dt = pixels/frame).
        """
        pass

    @abstractmethod
    def draw(self, screen):
        """Desenha tudo na superfície recebida.

        Parâmetros:
            screen: pygame.Surface da janela principal.
        """
        pass
