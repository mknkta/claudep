# level_loader.py — carrega definições de fases a partir de JSON
#
# Formato esperado do JSON:
#   {
#     "music": "assets/music/level1.ogg",
#     "obstacles": [
#       {"time": 1.5, "type": "spike"},
#       {"time": 3.0, "type": "platform", "y": 400, "width": 200}
#     ]
#   }
#
# Cada entrada retornada tem o atributo spawn_x calculado como:
#   spawn_x = time * world_speed + SCREEN_WIDTH
# Isso garante que o obstáculo entre pela direita exatamente quando a
# música (e o mundo) estiver naquele instante de tempo.

import json
from dataclasses import dataclass, field
from typing import Any

from config import SCREEN_WIDTH, GROUND_Y
from src.entities.obstacles import Obstacle, Spike, Platform


@dataclass
class ObstacleDef:
    """Definição "fria" de um obstáculo — ainda não instanciado."""
    spawn_x: float
    type: str
    params: dict = field(default_factory=dict)

    def instantiate(self, screen_x: float) -> Obstacle:
        """Cria o obstáculo na posição de tela screen_x."""
        if self.type == "spike":
            return Spike(x=screen_x)
        if self.type == "platform":
            y     = self.params.get("y", GROUND_Y - 180)
            width = self.params.get("width", 200)
            return Platform(x=screen_x, y=y, width=width)
        raise ValueError(f"Tipo de obstáculo desconhecido: '{self.type}'")


def load_level(path: str, world_speed: float) -> tuple[str, list[ObstacleDef]]:
    """
    Lê o JSON da fase e devolve (music_path, lista_de_ObstacleDef).

    Os ObstacleDefs ficam ordenados por spawn_x crescente para facilitar
    o spawner da GameplayScene.
    """
    with open(path, encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)

    music: str = data.get("music", "")
    defs: list[ObstacleDef] = []

    for entry in data.get("obstacles", []):
        t       = float(entry["time"])
        obs_type = entry["type"]
        # spawn_x: posição onde o obstáculo nasce (fora da tela, à direita).
        spawn_x = t * world_speed + SCREEN_WIDTH
        params  = {k: v for k, v in entry.items() if k not in ("time", "type")}
        defs.append(ObstacleDef(spawn_x=spawn_x, type=obs_type, params=params))

    defs.sort(key=lambda d: d.spawn_x)
    return music, defs
