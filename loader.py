import importlib
from config import SCREEN_WIDTH, GROUND_Y, CEILING_Y
from obstacles import Spike, CeilingSpike, Platform, Portal, Wall, SpikeBall, PulseLaser


class Def:
    def __init__(self, spawn_x, obs_type, params):
        self.spawn_x  = spawn_x
        self.obs_type = obs_type
        self.params   = params

    def make(self, screen_x):
        t = self.obs_type
        o = None
        if t == "spike":
            o = Spike(x=screen_x, size=self.params.get("size", "medium"))
        elif t == "ceiling_spike":
            o = CeilingSpike(x=screen_x, size=self.params.get("size", "medium"))
        elif t == "platform":
            o = Platform(x=screen_x,
                         y=self.params.get("y", GROUND_Y - 180),
                         width=self.params.get("width", 200))
        elif t == "portal":
            o = Portal(x=screen_x, target_mode=self.params.get("target_mode", "ship"))
        elif t == "wall":
            mid_y = (CEILING_Y + GROUND_Y) // 2
            o = Wall(x=screen_x,
                     gap_y=self.params.get("gap_y", mid_y),
                     gap_h=self.params.get("gap_h", 210))
        elif t == "pulse_laser":
            mid_y = (CEILING_Y + GROUND_Y) // 2
            import math
            o = PulseLaser(x=screen_x,
                           y=self.params.get("y", mid_y),
                           freq=self.params.get("freq", 2.0),
                           phase=self.params.get("phase", 0.0),
                           width=self.params.get("width", 900))
        elif t == "spike_ball":
            mid_y = (CEILING_Y + GROUND_Y) // 2
            o = SpikeBall(x=screen_x,
                          base_y=self.params.get("base_y", mid_y),
                          amplitude=self.params.get("amplitude", 120),
                          speed=self.params.get("speed", 1.8))
        if o is not None:
            o._spawn_x = self.spawn_x
        return o


def load(world_speed: float, phase: int = 1):
    """Carrega level<phase>.py e retorna (music_path, defs, duration)."""
    lvl = importlib.import_module(f"level{phase}")
    defs = []
    for e in lvl.OBSTACLES:
        spawn_x = float(e["time"]) * world_speed + SCREEN_WIDTH
        params  = {k: v for k, v in e.items() if k not in ("time", "type")}
        defs.append(Def(spawn_x, e["type"], params))
    defs.sort(key=lambda d: d.spawn_x)
    return lvl.MUSIC, defs, lvl.DURATION
