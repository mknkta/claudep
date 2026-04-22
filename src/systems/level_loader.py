# level_loader.py — carrega definições de fases a partir de JSON
#
# Formato esperado do JSON:
#   {
#     "music": "assets/music/level1.ogg",
#     "duration": 92.0,
#     "obstacles": [
#       {"time": 1.5, "type": "spike"},
#       {"time": 3.0, "type": "platform", "y": 400, "width": 200}
#     ]
#   }

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
        if self.type == "spike":
            return Spike(x=screen_x)
        if self.type == "platform":
            y     = self.params.get("y", GROUND_Y - 180)
            width = self.params.get("width", 200)
            return Platform(x=screen_x, y=y, width=width)
        raise ValueError(f"Tipo de obstáculo desconhecido: '{self.type}'")


def load_level(path: str, world_speed: float) -> tuple[str, list[ObstacleDef], float]:
    """
    Lê o JSON da fase e devolve (music_path, lista_de_ObstacleDef, music_duration).

    music_duration vem do campo "duration" do JSON. Se ausente, é estimado
    a partir do tempo do último obstáculo + 2 segundos de buffer.
    """
    with open(path, encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)

    music: str = data.get("music", "")
    defs: list[ObstacleDef] = []

    for entry in data.get("obstacles", []):
        t        = float(entry["time"])
        obs_type = entry["type"]
        spawn_x  = t * world_speed + SCREEN_WIDTH
        params   = {k: v for k, v in entry.items() if k not in ("time", "type")}
        defs.append(ObstacleDef(spawn_x=spawn_x, type=obs_type, params=params))

    defs.sort(key=lambda d: d.spawn_x)

    # Duração da música
    if "duration" in data:
        duration = float(data["duration"])
    elif defs:
        last_t = max(float(e["time"]) for e in data.get("obstacles", [{}]))
        duration = last_t + 2.0
    else:
        duration = 60.0

    return music, defs, duration
