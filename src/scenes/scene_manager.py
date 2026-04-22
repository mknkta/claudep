# scene_manager.py — gerencia qual cena está ativa e delega chamadas a ela
#
# O padrão "manager" desacopla o loop principal das cenas concretas:
# main.py não precisa saber nada sobre TestScene, MenuScene etc.

class SceneManager:
    def __init__(self, initial_scene):
        # Guarda a cena ativa. Sempre deve ser uma instância de Scene.
        self.current_scene = initial_scene

    def change_scene(self, new_scene):
        """Troca a cena ativa imediatamente.

        Chame isto de dentro de qualquer cena quando quiser navegar
        (ex: menu → jogo, jogo → game over).
        """
        self.current_scene = new_scene

    # Os três métodos abaixo simplesmente repassam a chamada
    # para a cena atual — o loop principal não precisa mudar nunca.

    def handle_events(self, events):
        self.current_scene.handle_events(events)

    def update(self, dt):
        self.current_scene.update(dt)

    def draw(self, screen):
        self.current_scene.draw(screen)
