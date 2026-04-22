import level1
from config import SCREEN_WIDTH, GROUND_Y
from obstacles import Spike, Platform

class Def:
    def __init__(self, spawn_x, obs_type, params):
        self.spawn_x  = spawn_x
        self.obs_type = obs_type
        self.params   = params

    def make(self, screen_x):
        if self.obs_type == "spike":
            s = Spike(x=screen_x, size=self.params.get("size", "medium"))
            s._spawn_x = self.spawn_x
            return s
        if self.obs_type == "platform":
            p = Platform(x=screen_x,
                         y=self.params.get("y", GROUND_Y - 180),
                         width=self.params.get("width", 200))
            p._spawn_x = self.spawn_x
            return p

def load(world_speed: float):
    """Retorna (music_path, defs, duration)."""
    defs = []
    for e in level1.OBSTACLES:
        spawn_x = float(e["time"]) * world_speed + SCREEN_WIDTH
        params  = {k: v for k, v in e.items() if k not in ("time", "type")}
        defs.append(Def(spawn_x, e["type"], params))
    defs.sort(key=lambda d: d.spawn_x)
    return level1.MUSIC, defs, level1.DURATION
