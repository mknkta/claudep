MUSIC    = "assets/music/level1.ogg"
DURATION = 75.0

# Fase 3: cubo normal (0-35s) → portal → gravity_flip (35-75s).
# Na seção gravity_flip o espaço inverte a gravidade sem delay.

OBSTACLES = [

    # ── SEÇÃO 1: Cubo normal (0–35s) ─────────────────────────────────

    {"time":  2.0,  "type": "spike", "size": "small"},
    {"time":  2.12, "type": "spike", "size": "medium"},

    {"time":  4.0,  "type": "spike", "size": "medium"},
    {"time":  4.12, "type": "spike", "size": "large"},

    {"time":  6.0,  "type": "spike", "size": "large"},
    {"time":  6.12, "type": "spike", "size": "medium"},
    {"time":  6.24, "type": "spike", "size": "small"},

    {"time":  8.0,  "type": "platform", "y": 520, "width": 160},
    {"time":  8.0,  "type": "spike", "size": "large"},

    {"time": 10.0,  "type": "spike", "size": "small"},
    {"time": 10.12, "type": "spike", "size": "medium"},
    {"time": 10.24, "type": "spike", "size": "large"},

    {"time": 12.0,  "type": "spike", "size": "medium"},
    {"time": 12.12, "type": "spike", "size": "large"},

    {"time": 14.0,  "type": "spike", "size": "large"},
    {"time": 14.12, "type": "spike", "size": "medium"},
    {"time": 14.24, "type": "spike", "size": "small"},
    {"time": 14.36, "type": "spike", "size": "medium"},

    {"time": 16.0,  "type": "spike", "size": "small"},
    {"time": 16.12, "type": "spike", "size": "medium"},

    {"time": 18.0,  "type": "platform", "y": 510, "width": 150},
    {"time": 18.0,  "type": "spike", "size": "medium"},
    {"time": 18.12, "type": "spike", "size": "large"},

    {"time": 20.0,  "type": "spike", "size": "large"},
    {"time": 20.12, "type": "spike", "size": "medium"},
    {"time": 20.24, "type": "spike", "size": "large"},

    {"time": 22.0,  "type": "spike", "size": "medium"},
    {"time": 22.12, "type": "spike", "size": "large"},

    {"time": 24.0,  "type": "spike", "size": "small"},
    {"time": 24.12, "type": "spike", "size": "medium"},
    {"time": 24.24, "type": "spike", "size": "large"},
    {"time": 24.36, "type": "spike", "size": "medium"},

    {"time": 26.0,  "type": "spike", "size": "large"},
    {"time": 26.12, "type": "spike", "size": "medium"},
    {"time": 26.24, "type": "spike", "size": "small"},

    {"time": 28.0,  "type": "spike", "size": "medium"},
    {"time": 28.12, "type": "spike", "size": "large"},

    {"time": 30.0,  "type": "spike", "size": "large"},
    {"time": 30.12, "type": "spike", "size": "medium"},
    {"time": 30.24, "type": "spike", "size": "large"},

    {"time": 32.0,  "type": "spike", "size": "small"},
    {"time": 32.12, "type": "spike", "size": "medium"},
    {"time": 32.24, "type": "spike", "size": "large"},

    {"time": 34.0,  "type": "spike", "size": "medium"},
    {"time": 34.12, "type": "spike", "size": "large"},

    # ── PORTAL: transição para gravity_flip (35s) ─────────────────────
    {"time": 35.0,  "type": "gravity_flip_portal"},

    # ── SEÇÃO 2: Gravity flip — difícil (35–75s) ──────────────────────
    # Espaço inverte a gravidade. Espinhos + SpikeBalls oscilantes.

    # bolas moveis logo após o portal
    {"time": 36.0,  "type": "spike_ball", "base_y": 320, "amplitude": 200, "speed": 2.0},
    {"time": 37.5,  "type": "spike_ball", "base_y": 280, "amplitude": 170, "speed": 2.5},
    {"time": 39.0,  "type": "spike_ball", "base_y": 360, "amplitude": 190, "speed": 1.8},

    {"time": 36.5,  "type": "spike",         "size": "large"},
    {"time": 36.62, "type": "ceiling_spike", "size": "large"},

    {"time": 37.5,  "type": "ceiling_spike", "size": "large"},
    {"time": 37.62, "type": "ceiling_spike", "size": "medium"},

    {"time": 38.5,  "type": "spike",         "size": "medium"},
    {"time": 38.62, "type": "spike",         "size": "large"},

    {"time": 39.5,  "type": "ceiling_spike", "size": "large"},
    {"time": 39.62, "type": "spike",         "size": "medium"},

    {"time": 40.5,  "type": "spike",         "size": "large"},
    {"time": 40.62, "type": "ceiling_spike", "size": "large"},
    {"time": 40.74, "type": "spike",         "size": "medium"},

    {"time": 41.0,  "type": "spike_ball", "base_y": 320, "amplitude": 210, "speed": 2.2},

    {"time": 41.5,  "type": "ceiling_spike", "size": "medium"},
    {"time": 41.62, "type": "ceiling_spike", "size": "large"},
    {"time": 41.74, "type": "spike",         "size": "large"},

    {"time": 42.5,  "type": "spike",         "size": "large"},
    {"time": 42.62, "type": "ceiling_spike", "size": "medium"},

    {"time": 43.0,  "type": "spike_ball", "base_y": 300, "amplitude": 190, "speed": 2.8},

    {"time": 43.5,  "type": "ceiling_spike", "size": "large"},
    {"time": 43.62, "type": "spike",         "size": "large"},
    {"time": 43.74, "type": "ceiling_spike", "size": "medium"},

    {"time": 44.5,  "type": "spike",         "size": "medium"},
    {"time": 44.62, "type": "spike",         "size": "large"},
    {"time": 44.74, "type": "ceiling_spike", "size": "large"},

    {"time": 45.0,  "type": "spike_ball", "base_y": 340, "amplitude": 200, "speed": 2.0},

    {"time": 45.5,  "type": "ceiling_spike", "size": "large"},
    {"time": 45.62, "type": "ceiling_spike", "size": "medium"},
    {"time": 45.74, "type": "spike",         "size": "large"},

    {"time": 46.5,  "type": "spike",         "size": "large"},
    {"time": 46.62, "type": "ceiling_spike", "size": "large"},

    {"time": 47.0,  "type": "spike_ball", "base_y": 320, "amplitude": 215, "speed": 2.5},

    {"time": 47.5,  "type": "ceiling_spike", "size": "medium"},
    {"time": 47.62, "type": "spike",         "size": "large"},
    {"time": 47.74, "type": "ceiling_spike", "size": "large"},

    {"time": 48.5,  "type": "spike",         "size": "large"},
    {"time": 48.62, "type": "spike",         "size": "medium"},
    {"time": 48.74, "type": "ceiling_spike", "size": "large"},

    {"time": 49.0,  "type": "spike_ball", "base_y": 290, "amplitude": 180, "speed": 3.0},

    {"time": 49.5,  "type": "ceiling_spike", "size": "large"},
    {"time": 49.62, "type": "ceiling_spike", "size": "medium"},
    {"time": 49.74, "type": "ceiling_spike", "size": "small"},

    {"time": 50.5,  "type": "spike",         "size": "large"},
    {"time": 50.62, "type": "ceiling_spike", "size": "large"},
    {"time": 50.74, "type": "spike",         "size": "medium"},

    {"time": 51.0,  "type": "spike_ball", "base_y": 350, "amplitude": 200, "speed": 2.3},

    {"time": 51.5,  "type": "ceiling_spike", "size": "large"},
    {"time": 51.62, "type": "spike",         "size": "large"},
    {"time": 51.74, "type": "ceiling_spike", "size": "medium"},

    {"time": 52.5,  "type": "spike",         "size": "medium"},
    {"time": 52.62, "type": "spike",         "size": "large"},
    {"time": 52.74, "type": "ceiling_spike", "size": "large"},

    {"time": 53.0,  "type": "spike_ball", "base_y": 310, "amplitude": 210, "speed": 2.7},

    {"time": 53.5,  "type": "ceiling_spike", "size": "large"},
    {"time": 53.62, "type": "ceiling_spike", "size": "medium"},
    {"time": 53.74, "type": "spike",         "size": "large"},
    {"time": 53.86, "type": "ceiling_spike", "size": "large"},

    {"time": 54.5,  "type": "spike",         "size": "large"},
    {"time": 54.62, "type": "ceiling_spike", "size": "large"},
    {"time": 54.74, "type": "spike",         "size": "medium"},
    {"time": 54.86, "type": "spike",         "size": "large"},

    {"time": 55.0,  "type": "spike_ball", "base_y": 330, "amplitude": 195, "speed": 2.4},

    {"time": 55.5,  "type": "ceiling_spike", "size": "large"},
    {"time": 55.62, "type": "spike",         "size": "large"},
    {"time": 55.74, "type": "ceiling_spike", "size": "large"},

    {"time": 56.5,  "type": "spike",         "size": "large"},
    {"time": 56.62, "type": "ceiling_spike", "size": "medium"},
    {"time": 56.74, "type": "spike",         "size": "large"},
    {"time": 56.86, "type": "ceiling_spike", "size": "large"},

    {"time": 57.0,  "type": "spike_ball", "base_y": 300, "amplitude": 205, "speed": 3.2},

    {"time": 57.5,  "type": "ceiling_spike", "size": "large"},
    {"time": 57.62, "type": "spike",         "size": "large"},
    {"time": 57.74, "type": "ceiling_spike", "size": "medium"},
    {"time": 57.86, "type": "spike",         "size": "large"},

    # ── SEÇÃO FINAL: máxima densidade (60–75s) ───────────────────────

    {"time": 59.5,  "type": "spike_ball", "base_y": 320, "amplitude": 220, "speed": 3.5},

    {"time": 60.0,  "type": "spike",         "size": "large"},
    {"time": 60.12, "type": "ceiling_spike", "size": "large"},
    {"time": 60.24, "type": "spike",         "size": "medium"},

    {"time": 61.0,  "type": "ceiling_spike", "size": "large"},
    {"time": 61.12, "type": "spike",         "size": "large"},
    {"time": 61.24, "type": "ceiling_spike", "size": "medium"},

    {"time": 62.0,  "type": "spike",         "size": "large"},
    {"time": 62.12, "type": "ceiling_spike", "size": "large"},
    {"time": 62.24, "type": "spike",         "size": "large"},

    {"time": 62.5,  "type": "spike_ball", "base_y": 300, "amplitude": 200, "speed": 3.0},

    {"time": 63.0,  "type": "ceiling_spike", "size": "large"},
    {"time": 63.12, "type": "spike",         "size": "medium"},
    {"time": 63.24, "type": "ceiling_spike", "size": "large"},

    {"time": 64.0,  "type": "spike",         "size": "large"},
    {"time": 64.12, "type": "ceiling_spike", "size": "large"},
    {"time": 64.24, "type": "spike",         "size": "medium"},
    {"time": 64.36, "type": "ceiling_spike", "size": "large"},

    {"time": 65.0,  "type": "ceiling_spike", "size": "large"},
    {"time": 65.12, "type": "spike",         "size": "large"},
    {"time": 65.24, "type": "ceiling_spike", "size": "medium"},
    {"time": 65.36, "type": "spike",         "size": "large"},

    {"time": 66.0,  "type": "spike",         "size": "large"},
    {"time": 66.12, "type": "ceiling_spike", "size": "large"},
    {"time": 66.24, "type": "spike",         "size": "large"},
    {"time": 66.36, "type": "ceiling_spike", "size": "medium"},

    {"time": 66.5,  "type": "spike_ball", "base_y": 340, "amplitude": 210, "speed": 3.3},

    {"time": 67.0,  "type": "ceiling_spike", "size": "large"},
    {"time": 67.12, "type": "spike",         "size": "large"},
    {"time": 67.24, "type": "ceiling_spike", "size": "large"},

    {"time": 68.0,  "type": "spike",         "size": "large"},
    {"time": 68.12, "type": "ceiling_spike", "size": "large"},
    {"time": 68.24, "type": "spike",         "size": "medium"},
    {"time": 68.36, "type": "ceiling_spike", "size": "large"},

    {"time": 69.0,  "type": "ceiling_spike", "size": "large"},
    {"time": 69.12, "type": "spike",         "size": "large"},
    {"time": 69.24, "type": "ceiling_spike", "size": "large"},
    {"time": 69.36, "type": "spike",         "size": "medium"},

    {"time": 70.0,  "type": "spike",         "size": "large"},
    {"time": 70.12, "type": "ceiling_spike", "size": "large"},
    {"time": 70.24, "type": "spike",         "size": "large"},

    {"time": 70.5,  "type": "spike_ball", "base_y": 310, "amplitude": 215, "speed": 3.8},

    {"time": 71.0,  "type": "ceiling_spike", "size": "large"},
    {"time": 71.12, "type": "spike",         "size": "large"},
    {"time": 71.24, "type": "ceiling_spike", "size": "medium"},
    {"time": 71.36, "type": "spike",         "size": "large"},

    {"time": 72.0,  "type": "spike",         "size": "large"},
    {"time": 72.12, "type": "ceiling_spike", "size": "large"},
    {"time": 72.24, "type": "spike",         "size": "medium"},
    {"time": 72.36, "type": "ceiling_spike", "size": "large"},

    {"time": 73.0,  "type": "ceiling_spike", "size": "large"},
    {"time": 73.12, "type": "spike",         "size": "large"},
    {"time": 73.24, "type": "ceiling_spike", "size": "large"},

    {"time": 74.0,  "type": "spike",         "size": "large"},
    {"time": 74.12, "type": "ceiling_spike", "size": "large"},
    {"time": 74.24, "type": "spike",         "size": "large"},
    {"time": 74.36, "type": "ceiling_spike", "size": "medium"},
]
