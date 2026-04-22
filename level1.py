MUSIC    = "assets/music/level1.ogg"
DURATION = 92.0

# Regras do level:
#   - Máximo 3 espinhos juntos (espaçados 0.12s)
#   - Gap mínimo de 0.7s entre grupos de espinhos
#   - Essas regras garantem que NADA é impossível de pular no Fácil (400 px/s)

OBSTACLES = [
    # ── Introdução ───────────────────────────────────────────────────
    {"time":  2.0,  "type": "spike", "size": "small"},
    {"time":  2.12, "type": "spike", "size": "medium"},

    {"time":  3.0,  "type": "spike", "size": "medium"},
    {"time":  3.12, "type": "spike", "size": "large"},
    {"time":  3.24, "type": "spike", "size": "medium"},

    {"time":  4.2,  "type": "spike", "size": "small"},
    {"time":  4.32, "type": "spike", "size": "medium"},
    {"time":  4.44, "type": "spike", "size": "small"},

    # ── Plataforma + espinhos ────────────────────────────────────────
    {"time":  5.5,  "type": "platform", "y": 520, "width": 160},
    {"time":  5.5,  "type": "spike", "size": "large"},
    {"time":  5.62, "type": "spike", "size": "medium"},

    {"time":  6.5,  "type": "spike", "size": "medium"},
    {"time":  6.62, "type": "spike", "size": "large"},
    {"time":  6.74, "type": "spike", "size": "medium"},

    {"time":  7.5,  "type": "spike", "size": "small"},
    {"time":  7.62, "type": "spike", "size": "medium"},
    {"time":  7.74, "type": "spike", "size": "small"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time":  9.0,  "type": "platform", "y": 525, "width": 150},
    {"time":  9.0,  "type": "spike", "size": "large"},
    {"time":  9.12, "type": "spike", "size": "medium"},

    {"time": 10.0,  "type": "spike", "size": "medium"},
    {"time": 10.12, "type": "spike", "size": "small"},
    {"time": 10.24, "type": "spike", "size": "medium"},

    {"time": 11.0,  "type": "spike", "size": "large"},
    {"time": 11.12, "type": "spike", "size": "medium"},
    {"time": 11.24, "type": "spike", "size": "small"},

    {"time": 12.0,  "type": "spike", "size": "small"},
    {"time": 12.12, "type": "spike", "size": "medium"},
    {"time": 12.24, "type": "spike", "size": "large"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time": 13.5,  "type": "platform", "y": 520, "width": 140},
    {"time": 13.5,  "type": "spike", "size": "large"},
    {"time": 13.62, "type": "spike", "size": "medium"},

    {"time": 14.5,  "type": "spike", "size": "medium"},
    {"time": 14.62, "type": "spike", "size": "large"},
    {"time": 14.74, "type": "spike", "size": "medium"},

    {"time": 15.5,  "type": "spike", "size": "small"},
    {"time": 15.62, "type": "spike", "size": "medium"},
    {"time": 15.74, "type": "spike", "size": "small"},

    {"time": 16.5,  "type": "spike", "size": "medium"},
    {"time": 16.62, "type": "spike", "size": "large"},
    {"time": 16.74, "type": "spike", "size": "medium"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time": 17.8,  "type": "platform", "y": 530, "width": 130},
    {"time": 17.8,  "type": "spike", "size": "large"},
    {"time": 17.92, "type": "spike", "size": "medium"},

    {"time": 19.0,  "type": "spike", "size": "small"},
    {"time": 19.12, "type": "spike", "size": "medium"},
    {"time": 19.24, "type": "spike", "size": "small"},

    {"time": 20.0,  "type": "spike", "size": "medium"},
    {"time": 20.12, "type": "spike", "size": "large"},
    {"time": 20.24, "type": "spike", "size": "medium"},

    {"time": 21.0,  "type": "spike", "size": "large"},
    {"time": 21.12, "type": "spike", "size": "medium"},
    {"time": 21.24, "type": "spike", "size": "small"},

    # ── Escadinha de plataformas ─────────────────────────────────────
    {"time": 22.5,  "type": "platform", "y": 530, "width": 130},
    {"time": 22.5,  "type": "spike", "size": "medium"},
    {"time": 22.62, "type": "spike", "size": "large"},

    {"time": 23.3,  "type": "platform", "y": 490, "width": 130},
    {"time": 23.3,  "type": "spike", "size": "large"},
    {"time": 23.42, "type": "spike", "size": "medium"},

    {"time": 24.1,  "type": "platform", "y": 450, "width": 130},
    {"time": 24.1,  "type": "spike", "size": "medium"},
    {"time": 24.22, "type": "spike", "size": "small"},

    {"time": 24.9,  "type": "platform", "y": 415, "width": 130},
    {"time": 24.9,  "type": "spike", "size": "large"},
    {"time": 25.02, "type": "spike", "size": "medium"},

    {"time": 26.0,  "type": "spike", "size": "small"},
    {"time": 26.12, "type": "spike", "size": "medium"},
    {"time": 26.24, "type": "spike", "size": "large"},

    {"time": 27.0,  "type": "spike", "size": "medium"},
    {"time": 27.12, "type": "spike", "size": "large"},
    {"time": 27.24, "type": "spike", "size": "medium"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time": 28.5,  "type": "platform", "y": 520, "width": 150},
    {"time": 28.5,  "type": "spike", "size": "large"},
    {"time": 28.62, "type": "spike", "size": "medium"},

    {"time": 29.5,  "type": "spike", "size": "medium"},
    {"time": 29.62, "type": "spike", "size": "small"},
    {"time": 29.74, "type": "spike", "size": "medium"},

    {"time": 30.5,  "type": "spike", "size": "large"},
    {"time": 30.62, "type": "spike", "size": "medium"},
    {"time": 30.74, "type": "spike", "size": "small"},

    {"time": 31.5,  "type": "spike", "size": "small"},
    {"time": 31.62, "type": "spike", "size": "medium"},
    {"time": 31.74, "type": "spike", "size": "large"},

    # ── Escadinha ────────────────────────────────────────────────────
    {"time": 32.8,  "type": "platform", "y": 525, "width": 120},
    {"time": 32.8,  "type": "spike", "size": "large"},
    {"time": 32.92, "type": "spike", "size": "medium"},

    {"time": 33.6,  "type": "platform", "y": 485, "width": 120},
    {"time": 33.6,  "type": "spike", "size": "medium"},
    {"time": 33.72, "type": "spike", "size": "large"},

    {"time": 34.4,  "type": "platform", "y": 445, "width": 120},
    {"time": 34.4,  "type": "spike", "size": "small"},
    {"time": 34.52, "type": "spike", "size": "medium"},

    {"time": 35.2,  "type": "platform", "y": 410, "width": 120},
    {"time": 35.2,  "type": "spike", "size": "large"},
    {"time": 35.32, "type": "spike", "size": "medium"},

    {"time": 36.2,  "type": "spike", "size": "medium"},
    {"time": 36.32, "type": "spike", "size": "large"},
    {"time": 36.44, "type": "spike", "size": "medium"},

    {"time": 37.2,  "type": "spike", "size": "small"},
    {"time": 37.32, "type": "spike", "size": "medium"},
    {"time": 37.44, "type": "spike", "size": "large"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time": 38.5,  "type": "platform", "y": 520, "width": 140},
    {"time": 38.5,  "type": "spike", "size": "large"},
    {"time": 38.62, "type": "spike", "size": "medium"},

    {"time": 39.5,  "type": "spike", "size": "medium"},
    {"time": 39.62, "type": "spike", "size": "large"},
    {"time": 39.74, "type": "spike", "size": "medium"},

    {"time": 40.5,  "type": "spike", "size": "small"},
    {"time": 40.62, "type": "spike", "size": "medium"},
    {"time": 40.74, "type": "spike", "size": "small"},

    {"time": 41.5,  "type": "spike", "size": "large"},
    {"time": 41.62, "type": "spike", "size": "medium"},
    {"time": 41.74, "type": "spike", "size": "large"},

    # ── Escadinha longa ──────────────────────────────────────────────
    {"time": 42.8,  "type": "platform", "y": 530, "width": 120},
    {"time": 42.8,  "type": "spike", "size": "large"},
    {"time": 42.92, "type": "spike", "size": "medium"},

    {"time": 43.6,  "type": "platform", "y": 490, "width": 120},
    {"time": 43.6,  "type": "spike", "size": "medium"},
    {"time": 43.72, "type": "spike", "size": "small"},

    {"time": 44.4,  "type": "platform", "y": 450, "width": 120},
    {"time": 44.4,  "type": "spike", "size": "large"},
    {"time": 44.52, "type": "spike", "size": "medium"},

    {"time": 45.2,  "type": "platform", "y": 415, "width": 120},
    {"time": 45.2,  "type": "spike", "size": "medium"},
    {"time": 45.32, "type": "spike", "size": "large"},

    {"time": 46.0,  "type": "platform", "y": 380, "width": 120},
    {"time": 46.0,  "type": "spike", "size": "small"},
    {"time": 46.12, "type": "spike", "size": "medium"},

    {"time": 47.0,  "type": "spike", "size": "medium"},
    {"time": 47.12, "type": "spike", "size": "large"},
    {"time": 47.24, "type": "spike", "size": "medium"},

    {"time": 48.0,  "type": "spike", "size": "small"},
    {"time": 48.12, "type": "spike", "size": "medium"},
    {"time": 48.24, "type": "spike", "size": "small"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time": 49.5,  "type": "platform", "y": 520, "width": 130},
    {"time": 49.5,  "type": "spike", "size": "large"},
    {"time": 49.62, "type": "spike", "size": "medium"},

    {"time": 50.5,  "type": "spike", "size": "medium"},
    {"time": 50.62, "type": "spike", "size": "large"},
    {"time": 50.74, "type": "spike", "size": "medium"},

    {"time": 51.5,  "type": "spike", "size": "large"},
    {"time": 51.62, "type": "spike", "size": "medium"},
    {"time": 51.74, "type": "spike", "size": "small"},

    {"time": 52.5,  "type": "spike", "size": "medium"},
    {"time": 52.62, "type": "spike", "size": "small"},
    {"time": 52.74, "type": "spike", "size": "medium"},

    # ── Escadinha ────────────────────────────────────────────────────
    {"time": 54.0,  "type": "platform", "y": 525, "width": 110},
    {"time": 54.0,  "type": "spike", "size": "large"},
    {"time": 54.12, "type": "spike", "size": "medium"},

    {"time": 54.8,  "type": "platform", "y": 485, "width": 110},
    {"time": 54.8,  "type": "spike", "size": "medium"},
    {"time": 54.92, "type": "spike", "size": "large"},

    {"time": 55.6,  "type": "platform", "y": 445, "width": 110},
    {"time": 55.6,  "type": "spike", "size": "small"},
    {"time": 55.72, "type": "spike", "size": "medium"},

    {"time": 56.4,  "type": "platform", "y": 410, "width": 110},
    {"time": 56.4,  "type": "spike", "size": "large"},
    {"time": 56.52, "type": "spike", "size": "medium"},

    {"time": 57.2,  "type": "platform", "y": 375, "width": 110},
    {"time": 57.2,  "type": "spike", "size": "medium"},
    {"time": 57.32, "type": "spike", "size": "small"},

    {"time": 58.2,  "type": "spike", "size": "large"},
    {"time": 58.32, "type": "spike", "size": "medium"},
    {"time": 58.44, "type": "spike", "size": "small"},

    {"time": 59.2,  "type": "spike", "size": "medium"},
    {"time": 59.32, "type": "spike", "size": "large"},
    {"time": 59.44, "type": "spike", "size": "medium"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time": 60.5,  "type": "platform", "y": 520, "width": 130},
    {"time": 60.5,  "type": "spike", "size": "large"},
    {"time": 60.62, "type": "spike", "size": "medium"},

    {"time": 61.5,  "type": "spike", "size": "small"},
    {"time": 61.62, "type": "spike", "size": "medium"},
    {"time": 61.74, "type": "spike", "size": "large"},

    {"time": 62.5,  "type": "spike", "size": "medium"},
    {"time": 62.62, "type": "spike", "size": "large"},
    {"time": 62.74, "type": "spike", "size": "medium"},

    {"time": 63.5,  "type": "spike", "size": "large"},
    {"time": 63.62, "type": "spike", "size": "medium"},
    {"time": 63.74, "type": "spike", "size": "small"},

    # ── Escadinha longa ──────────────────────────────────────────────
    {"time": 65.0,  "type": "platform", "y": 530, "width": 110},
    {"time": 65.0,  "type": "spike", "size": "large"},
    {"time": 65.12, "type": "spike", "size": "medium"},

    {"time": 65.8,  "type": "platform", "y": 490, "width": 110},
    {"time": 65.8,  "type": "spike", "size": "medium"},
    {"time": 65.92, "type": "spike", "size": "large"},

    {"time": 66.6,  "type": "platform", "y": 450, "width": 110},
    {"time": 66.6,  "type": "spike", "size": "small"},
    {"time": 66.72, "type": "spike", "size": "medium"},

    {"time": 67.4,  "type": "platform", "y": 415, "width": 110},
    {"time": 67.4,  "type": "spike", "size": "large"},
    {"time": 67.52, "type": "spike", "size": "medium"},

    {"time": 68.2,  "type": "platform", "y": 380, "width": 110},
    {"time": 68.2,  "type": "spike", "size": "medium"},
    {"time": 68.32, "type": "spike", "size": "small"},

    {"time": 69.0,  "type": "platform", "y": 345, "width": 110},
    {"time": 69.0,  "type": "spike", "size": "large"},
    {"time": 69.12, "type": "spike", "size": "medium"},

    {"time": 70.0,  "type": "spike", "size": "medium"},
    {"time": 70.12, "type": "spike", "size": "large"},
    {"time": 70.24, "type": "spike", "size": "medium"},

    {"time": 71.0,  "type": "spike", "size": "small"},
    {"time": 71.12, "type": "spike", "size": "medium"},
    {"time": 71.24, "type": "spike", "size": "small"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time": 72.5,  "type": "platform", "y": 520, "width": 120},
    {"time": 72.5,  "type": "spike", "size": "large"},
    {"time": 72.62, "type": "spike", "size": "medium"},

    {"time": 73.5,  "type": "spike", "size": "medium"},
    {"time": 73.62, "type": "spike", "size": "large"},
    {"time": 73.74, "type": "spike", "size": "medium"},

    {"time": 74.5,  "type": "spike", "size": "large"},
    {"time": 74.62, "type": "spike", "size": "medium"},
    {"time": 74.74, "type": "spike", "size": "small"},

    {"time": 75.5,  "type": "spike", "size": "small"},
    {"time": 75.62, "type": "spike", "size": "medium"},
    {"time": 75.74, "type": "spike", "size": "large"},

    # ── Escadinha final ──────────────────────────────────────────────
    {"time": 77.0,  "type": "platform", "y": 525, "width": 110},
    {"time": 77.0,  "type": "spike", "size": "large"},
    {"time": 77.12, "type": "spike", "size": "medium"},

    {"time": 77.8,  "type": "platform", "y": 485, "width": 110},
    {"time": 77.8,  "type": "spike", "size": "medium"},
    {"time": 77.92, "type": "spike", "size": "large"},

    {"time": 78.6,  "type": "platform", "y": 445, "width": 110},
    {"time": 78.6,  "type": "spike", "size": "small"},
    {"time": 78.72, "type": "spike", "size": "medium"},

    {"time": 79.4,  "type": "platform", "y": 408, "width": 110},
    {"time": 79.4,  "type": "spike", "size": "large"},
    {"time": 79.52, "type": "spike", "size": "medium"},

    {"time": 80.2,  "type": "platform", "y": 371, "width": 110},
    {"time": 80.2,  "type": "spike", "size": "medium"},
    {"time": 80.32, "type": "spike", "size": "small"},

    {"time": 81.0,  "type": "platform", "y": 334, "width": 110},
    {"time": 81.0,  "type": "spike", "size": "large"},
    {"time": 81.12, "type": "spike", "size": "medium"},

    {"time": 82.0,  "type": "spike", "size": "medium"},
    {"time": 82.12, "type": "spike", "size": "large"},
    {"time": 82.24, "type": "spike", "size": "medium"},

    {"time": 83.0,  "type": "spike", "size": "small"},
    {"time": 83.12, "type": "spike", "size": "medium"},
    {"time": 83.24, "type": "spike", "size": "large"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time": 84.5,  "type": "platform", "y": 520, "width": 120},
    {"time": 84.5,  "type": "spike", "size": "large"},
    {"time": 84.62, "type": "spike", "size": "medium"},

    {"time": 85.5,  "type": "spike", "size": "medium"},
    {"time": 85.62, "type": "spike", "size": "large"},
    {"time": 85.74, "type": "spike", "size": "medium"},

    {"time": 86.5,  "type": "spike", "size": "large"},
    {"time": 86.62, "type": "spike", "size": "medium"},
    {"time": 86.74, "type": "spike", "size": "small"},

    {"time": 87.5,  "type": "spike", "size": "small"},
    {"time": 87.62, "type": "spike", "size": "medium"},
    {"time": 87.74, "type": "spike", "size": "large"},

    {"time": 88.5,  "type": "spike", "size": "medium"},
    {"time": 88.62, "type": "spike", "size": "large"},
    {"time": 88.74, "type": "spike", "size": "medium"},

    {"time": 89.5,  "type": "spike", "size": "large"},
    {"time": 89.62, "type": "spike", "size": "medium"},
    {"time": 89.74, "type": "spike", "size": "small"},
]
