MUSIC    = "assets/music/level2.ogg"
DURATION = 90.0

# Fase 2: primeira metade cubo (0-40s), portal em 40s, segunda metade nave (40-90s)
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
    {"time": 40.0,  "type": "portal", "target_mode": "ship"},

    # ── PARTE 2: NAVE (40–90s) ────────────────────────────────────────
    # Padrão: espinho no chão (Spike) + espinho no teto (CeilingSpike)
    # não alinhados, forçando o player a "vibrar" no meio do corredor.
    # Regra: gap de pelo menos 1.0s entre obstáculos do mesmo lado.

    # bloco 1 — espinho chão, depois espinho teto
    {"time": 42.0,  "type": "spike",         "size": "large"},
    {"time": 43.2,  "type": "ceiling_spike",  "size": "large"},

    {"time": 44.4,  "type": "spike",         "size": "medium"},
    {"time": 45.6,  "type": "ceiling_spike",  "size": "medium"},

    {"time": 46.8,  "type": "spike",         "size": "large"},
    {"time": 47.2,  "type": "spike",         "size": "medium"},
    {"time": 48.0,  "type": "ceiling_spike",  "size": "large"},

    {"time": 49.0,  "type": "ceiling_spike",  "size": "medium"},
    {"time": 50.0,  "type": "spike",         "size": "large"},

    {"time": 51.0,  "type": "spike",         "size": "medium"},
    {"time": 51.4,  "type": "spike",         "size": "large"},
    {"time": 52.0,  "type": "ceiling_spike",  "size": "large"},
    {"time": 52.4,  "type": "ceiling_spike",  "size": "medium"},

    {"time": 53.5,  "type": "spike",         "size": "large"},
    {"time": 54.5,  "type": "ceiling_spike",  "size": "large"},

    {"time": 55.5,  "type": "spike",         "size": "medium"},
    {"time": 55.9,  "type": "spike",         "size": "large"},
    {"time": 56.5,  "type": "ceiling_spike",  "size": "medium"},
    {"time": 57.0,  "type": "ceiling_spike",  "size": "large"},

    {"time": 58.0,  "type": "spike",         "size": "large"},
    {"time": 58.8,  "type": "ceiling_spike",  "size": "large"},
    {"time": 59.6,  "type": "spike",         "size": "medium"},

    {"time": 60.4,  "type": "ceiling_spike",  "size": "large"},
    {"time": 61.0,  "type": "spike",         "size": "large"},
    {"time": 61.4,  "type": "spike",         "size": "medium"},

    {"time": 62.0,  "type": "ceiling_spike",  "size": "medium"},
    {"time": 62.4,  "type": "ceiling_spike",  "size": "large"},
    {"time": 63.0,  "type": "spike",         "size": "large"},

    {"time": 64.0,  "type": "spike",         "size": "medium"},
    {"time": 64.4,  "type": "spike",         "size": "large"},
    {"time": 65.0,  "type": "ceiling_spike",  "size": "large"},
    {"time": 65.4,  "type": "ceiling_spike",  "size": "medium"},

    {"time": 66.5,  "type": "spike",         "size": "large"},
    {"time": 67.3,  "type": "ceiling_spike",  "size": "large"},
    {"time": 68.1,  "type": "spike",         "size": "large"},
    {"time": 68.5,  "type": "spike",         "size": "medium"},

    {"time": 69.0,  "type": "ceiling_spike",  "size": "large"},
    {"time": 69.4,  "type": "ceiling_spike",  "size": "medium"},
    {"time": 70.0,  "type": "spike",         "size": "large"},

    {"time": 71.0,  "type": "spike",         "size": "medium"},
    {"time": 71.5,  "type": "spike",         "size": "large"},
    {"time": 72.0,  "type": "ceiling_spike",  "size": "large"},
    {"time": 72.5,  "type": "ceiling_spike",  "size": "large"},

    {"time": 73.5,  "type": "spike",         "size": "large"},
    {"time": 74.0,  "type": "ceiling_spike",  "size": "large"},
    {"time": 74.5,  "type": "spike",         "size": "medium"},
    {"time": 75.0,  "type": "ceiling_spike",  "size": "medium"},

    {"time": 76.0,  "type": "spike",         "size": "large"},
    {"time": 76.5,  "type": "ceiling_spike",  "size": "large"},
    {"time": 77.0,  "type": "spike",         "size": "large"},
    {"time": 77.5,  "type": "ceiling_spike",  "size": "large"},

    {"time": 78.5,  "type": "spike",         "size": "medium"},
    {"time": 79.0,  "type": "ceiling_spike",  "size": "large"},
    {"time": 79.5,  "type": "spike",         "size": "large"},
    {"time": 80.0,  "type": "ceiling_spike",  "size": "medium"},

    {"time": 81.0,  "type": "spike",         "size": "large"},
    {"time": 81.5,  "type": "ceiling_spike",  "size": "large"},
    {"time": 82.0,  "type": "spike",         "size": "medium"},
    {"time": 82.5,  "type": "ceiling_spike",  "size": "large"},

    {"time": 83.5,  "type": "spike",         "size": "large"},
    {"time": 84.0,  "type": "ceiling_spike",  "size": "large"},
    {"time": 84.5,  "type": "spike",         "size": "large"},
    {"time": 85.0,  "type": "ceiling_spike",  "size": "medium"},

    {"time": 86.0,  "type": "spike",         "size": "large"},
    {"time": 86.5,  "type": "ceiling_spike",  "size": "large"},
    {"time": 87.0,  "type": "spike",         "size": "medium"},
    {"time": 87.5,  "type": "ceiling_spike",  "size": "large"},

    {"time": 88.5,  "type": "spike",         "size": "large"},
    {"time": 89.0,  "type": "ceiling_spike",  "size": "large"},
    {"time": 89.5,  "type": "spike",         "size": "medium"},
]
