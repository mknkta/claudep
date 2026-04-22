MUSIC    = "assets/music/level2.ogg"
DURATION = 90.0

# Fase 2: cubo (0-36s), portal em 36s (40%), nave (36-90s)
# Espinhos de teto (ceiling_spike) formam corredor estreito com espinhos do chão.
# Nave: segurar ESPAÇO sobe, soltar desce.

OBSTACLES = [
    # ── PARTE 1: CUBO (0–40s) ────────────────────────────────────────

    {"time":  2.0,  "type": "spike", "size": "small"},
    {"time":  2.12, "type": "spike", "size": "medium"},

    {"time":  3.2,  "type": "spike", "size": "medium"},
    {"time":  3.32, "type": "spike", "size": "large"},
    {"time":  3.44, "type": "spike", "size": "medium"},

    {"time":  4.5,  "type": "platform", "y": 520, "width": 160},
    {"time":  4.5,  "type": "spike", "size": "large"},
    {"time":  4.62, "type": "spike", "size": "medium"},

    {"time":  5.8,  "type": "spike", "size": "medium"},
    {"time":  5.92, "type": "spike", "size": "small"},
    {"time":  6.04, "type": "spike", "size": "medium"},

    {"time":  7.0,  "type": "spike", "size": "large"},
    {"time":  7.12, "type": "spike", "size": "medium"},
    {"time":  7.24, "type": "spike", "size": "small"},

    {"time":  8.5,  "type": "platform", "y": 510, "width": 150},
    {"time":  8.5,  "type": "spike", "size": "large"},
    {"time":  8.62, "type": "spike", "size": "medium"},

    {"time":  9.8,  "type": "spike", "size": "small"},
    {"time":  9.92, "type": "spike", "size": "medium"},
    {"time": 10.04, "type": "spike", "size": "large"},

    {"time": 11.2,  "type": "spike", "size": "medium"},
    {"time": 11.32, "type": "spike", "size": "large"},
    {"time": 11.44, "type": "spike", "size": "medium"},

    {"time": 12.5,  "type": "platform", "y": 505, "width": 140},
    {"time": 12.5,  "type": "spike", "size": "large"},
    {"time": 12.62, "type": "spike", "size": "medium"},

    {"time": 13.8,  "type": "spike", "size": "medium"},
    {"time": 13.92, "type": "spike", "size": "small"},
    {"time": 14.04, "type": "spike", "size": "medium"},

    {"time": 15.0,  "type": "spike", "size": "large"},
    {"time": 15.12, "type": "spike", "size": "medium"},
    {"time": 15.24, "type": "spike", "size": "small"},

    {"time": 16.5,  "type": "platform", "y": 500, "width": 140},
    {"time": 16.5,  "type": "spike", "size": "medium"},
    {"time": 16.62, "type": "spike", "size": "large"},

    {"time": 17.8,  "type": "spike", "size": "small"},
    {"time": 17.92, "type": "spike", "size": "medium"},
    {"time": 18.04, "type": "spike", "size": "large"},

    {"time": 19.0,  "type": "spike", "size": "medium"},
    {"time": 19.12, "type": "spike", "size": "large"},
    {"time": 19.24, "type": "spike", "size": "medium"},

    # escadinha
    {"time": 20.5,  "type": "platform", "y": 520, "width": 130},
    {"time": 20.5,  "type": "spike", "size": "large"},
    {"time": 20.62, "type": "spike", "size": "medium"},

    {"time": 21.3,  "type": "platform", "y": 480, "width": 130},
    {"time": 21.3,  "type": "spike", "size": "medium"},
    {"time": 21.42, "type": "spike", "size": "large"},

    {"time": 22.1,  "type": "platform", "y": 440, "width": 130},
    {"time": 22.1,  "type": "spike", "size": "large"},
    {"time": 22.22, "type": "spike", "size": "medium"},

    {"time": 23.0,  "type": "spike", "size": "small"},
    {"time": 23.12, "type": "spike", "size": "medium"},
    {"time": 23.24, "type": "spike", "size": "large"},

    {"time": 24.2,  "type": "spike", "size": "large"},
    {"time": 24.32, "type": "spike", "size": "medium"},
    {"time": 24.44, "type": "spike", "size": "small"},

    {"time": 25.5,  "type": "platform", "y": 515, "width": 130},
    {"time": 25.5,  "type": "spike", "size": "medium"},
    {"time": 25.62, "type": "spike", "size": "large"},

    {"time": 26.8,  "type": "spike", "size": "medium"},
    {"time": 26.92, "type": "spike", "size": "large"},
    {"time": 27.04, "type": "spike", "size": "medium"},

    {"time": 28.0,  "type": "spike", "size": "large"},
    {"time": 28.12, "type": "spike", "size": "medium"},
    {"time": 28.24, "type": "spike", "size": "small"},

    {"time": 29.5,  "type": "platform", "y": 510, "width": 120},
    {"time": 29.5,  "type": "spike", "size": "large"},
    {"time": 29.62, "type": "spike", "size": "medium"},

    {"time": 30.8,  "type": "spike", "size": "small"},
    {"time": 30.92, "type": "spike", "size": "medium"},
    {"time": 31.04, "type": "spike", "size": "large"},

    {"time": 32.0,  "type": "spike", "size": "medium"},
    {"time": 32.12, "type": "spike", "size": "large"},
    {"time": 32.24, "type": "spike", "size": "medium"},

    # escadinha final cubo
    {"time": 33.5,  "type": "platform", "y": 520, "width": 120},
    {"time": 33.5,  "type": "spike", "size": "large"},
    {"time": 33.62, "type": "spike", "size": "medium"},

    {"time": 34.3,  "type": "platform", "y": 480, "width": 120},
    {"time": 34.3,  "type": "spike", "size": "medium"},
    {"time": 34.42, "type": "spike", "size": "large"},

    {"time": 35.1,  "type": "platform", "y": 440, "width": 120},
    {"time": 35.1,  "type": "spike", "size": "large"},
    {"time": 35.22, "type": "spike", "size": "medium"},

    {"time": 36.2,  "type": "spike", "size": "medium"},
    {"time": 36.32, "type": "spike", "size": "large"},
    {"time": 36.44, "type": "spike", "size": "medium"},

    {"time": 37.5,  "type": "spike", "size": "large"},
    {"time": 37.62, "type": "spike", "size": "medium"},
    {"time": 37.74, "type": "spike", "size": "small"},

    {"time": 38.8,  "type": "spike", "size": "medium"},
    {"time": 38.92, "type": "spike", "size": "large"},
    {"time": 39.04, "type": "spike", "size": "medium"},

    # ── PORTAL (40s) — troca pra modo nave ───────────────────────────
    {"time": 36.0,  "type": "portal", "target_mode": "ship"},

    # ── PARTE 2: NAVE (36–90s) ───────────────────────────────────────────
    # HARD MODE: muros estreitos, bolas duplas/triplas, alta velocidade.
    # GROUND_Y=600, CEILING_Y=40 → meio=320.

    # --- intro rápida ---
    {"time": 38.0, "type": "spike",        "size": "large"},
    {"time": 38.6, "type": "ceiling_spike","size": "large"},

    # --- primeiro muro + bola imediata ---
    {"time": 40.0, "type": "wall",       "gap_y": 320, "gap_h": 200},
    {"time": 40.8, "type": "spike_ball", "base_y": 200, "amplitude": 110, "speed": 2.2},
    {"time": 40.8, "type": "spike_ball", "base_y": 440, "amplitude": 110, "speed": 2.2},

    # --- muro alto + dupla bola em velocidades diferentes ---
    {"time": 43.0, "type": "wall",       "gap_y": 240, "gap_h": 185},
    {"time": 43.8, "type": "spike_ball", "base_y": 180, "amplitude": 90, "speed": 3.0},
    {"time": 43.8, "type": "spike_ball", "base_y": 460, "amplitude": 90, "speed": 2.5},

    # --- três bolas em sequência rápida ---
    {"time": 46.0, "type": "spike_ball", "base_y": 320, "amplitude": 130, "speed": 2.8},
    {"time": 47.2, "type": "spike_ball", "base_y": 200, "amplitude": 100, "speed": 3.2},
    {"time": 48.4, "type": "spike_ball", "base_y": 440, "amplitude": 100, "speed": 2.6},

    # --- muro baixo ---
    {"time": 49.5, "type": "wall",       "gap_y": 400, "gap_h": 180},
    {"time": 50.3, "type": "spike_ball", "base_y": 320, "amplitude": 120, "speed": 3.0},
    {"time": 50.3, "type": "spike_ball", "base_y": 160, "amplitude":  80, "speed": 2.4},

    # --- dois muros seguidos, gaps alternados ---
    {"time": 52.5, "type": "wall",       "gap_y": 220, "gap_h": 175},
    {"time": 54.0, "type": "wall",       "gap_y": 420, "gap_h": 175},

    # --- corredor de bolas ---
    {"time": 55.5, "type": "spike_ball", "base_y": 180, "amplitude": 110, "speed": 3.5},
    {"time": 55.5, "type": "spike_ball", "base_y": 460, "amplitude": 110, "speed": 3.5},
    {"time": 57.0, "type": "spike_ball", "base_y": 320, "amplitude": 140, "speed": 2.0},

    # --- muro central estreito + bola dentro do gap ---
    {"time": 59.0, "type": "wall",       "gap_y": 320, "gap_h": 170},
    {"time": 59.5, "type": "spike_ball", "base_y": 320, "amplitude": 100, "speed": 4.0},

    # --- três muros seguidos, gaps alternados ---
    {"time": 61.5, "type": "wall",       "gap_y": 240, "gap_h": 170},
    {"time": 63.0, "type": "wall",       "gap_y": 400, "gap_h": 170},
    {"time": 64.5, "type": "wall",       "gap_y": 280, "gap_h": 170},

    # --- quatro bolas simultâneas ---
    {"time": 66.0, "type": "spike_ball", "base_y": 160, "amplitude":  70, "speed": 2.5},
    {"time": 66.0, "type": "spike_ball", "base_y": 280, "amplitude":  70, "speed": 3.5},
    {"time": 66.0, "type": "spike_ball", "base_y": 370, "amplitude":  70, "speed": 3.0},
    {"time": 66.0, "type": "spike_ball", "base_y": 480, "amplitude":  70, "speed": 2.8},

    # --- muro + duas bolas ---
    {"time": 68.5, "type": "wall",       "gap_y": 320, "gap_h": 165},
    {"time": 69.0, "type": "spike_ball", "base_y": 200, "amplitude": 100, "speed": 3.8},
    {"time": 69.0, "type": "spike_ball", "base_y": 440, "amplitude": 100, "speed": 3.8},

    # --- quatro muros consecutivos (inferno) ---
    {"time": 71.5, "type": "wall",       "gap_y": 220, "gap_h": 160},
    {"time": 73.0, "type": "wall",       "gap_y": 420, "gap_h": 160},
    {"time": 74.5, "type": "wall",       "gap_y": 260, "gap_h": 160},
    {"time": 76.0, "type": "wall",       "gap_y": 380, "gap_h": 160},

    # --- tripla bola pós-muros ---
    {"time": 77.5, "type": "spike_ball", "base_y": 180, "amplitude": 100, "speed": 4.0},
    {"time": 77.5, "type": "spike_ball", "base_y": 320, "amplitude": 140, "speed": 3.5},
    {"time": 77.5, "type": "spike_ball", "base_y": 460, "amplitude": 100, "speed": 4.0},

    # --- muro estreito + bola rápida ---
    {"time": 80.0, "type": "wall",       "gap_y": 320, "gap_h": 155},
    {"time": 80.5, "type": "spike_ball", "base_y": 320, "amplitude": 130, "speed": 5.0},

    # --- CLÍMAX FINAL ---
    {"time": 82.5, "type": "wall",       "gap_y": 240, "gap_h": 150},
    {"time": 82.5, "type": "spike_ball", "base_y": 420, "amplitude":  90, "speed": 4.5},
    {"time": 84.0, "type": "wall",       "gap_y": 400, "gap_h": 150},
    {"time": 84.0, "type": "spike_ball", "base_y": 200, "amplitude":  90, "speed": 4.5},
    {"time": 85.5, "type": "spike_ball", "base_y": 160, "amplitude":  80, "speed": 5.0},
    {"time": 85.5, "type": "spike_ball", "base_y": 320, "amplitude": 120, "speed": 5.0},
    {"time": 85.5, "type": "spike_ball", "base_y": 480, "amplitude":  80, "speed": 5.0},
    {"time": 87.0, "type": "wall",       "gap_y": 320, "gap_h": 145},
    {"time": 87.5, "type": "spike_ball", "base_y": 220, "amplitude": 110, "speed": 5.5},
    {"time": 87.5, "type": "spike_ball", "base_y": 420, "amplitude": 110, "speed": 5.5},
]
