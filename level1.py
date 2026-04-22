MUSIC    = "assets/music/level1.ogg"
DURATION = 92.0

# Harder version: gaps reduzidos de 1.0s → 0.45s, laser pulsante adicionado

OBSTACLES = [
    # ── Introdução ───────────────────────────────────────────────────
    {"time":  2.0,  "type": "spike", "size": "small"},
    {"time":  2.12, "type": "spike", "size": "medium"},

    {"time":  2.6,  "type": "spike", "size": "medium"},
    {"time":  2.72, "type": "spike", "size": "large"},
    {"time":  2.84, "type": "spike", "size": "medium"},

    {"time":  3.4,  "type": "spike", "size": "small"},
    {"time":  3.52, "type": "spike", "size": "medium"},
    {"time":  3.64, "type": "spike", "size": "small"},

    {"time":  4.2,  "type": "spike", "size": "large"},
    {"time":  4.32, "type": "spike", "size": "medium"},
    {"time":  4.44, "type": "spike", "size": "large"},

    # ── Plataforma + espinhos ────────────────────────────────────────
    {"time":  5.0,  "type": "platform", "y": 520, "width": 150},
    {"time":  5.0,  "type": "spike", "size": "large"},
    {"time":  5.12, "type": "spike", "size": "medium"},

    {"time":  5.6,  "type": "spike", "size": "medium"},
    {"time":  5.72, "type": "spike", "size": "large"},
    {"time":  5.84, "type": "spike", "size": "medium"},

    {"time":  6.4,  "type": "spike", "size": "small"},
    {"time":  6.52, "type": "spike", "size": "medium"},
    {"time":  6.64, "type": "spike", "size": "large"},

    {"time":  7.1,  "type": "spike", "size": "medium"},
    {"time":  7.22, "type": "spike", "size": "large"},
    {"time":  7.34, "type": "spike", "size": "medium"},

    # ── Laser pulsante (intro) ────────────────────────────────────────
    {"time":  8.0,  "type": "pulse_laser", "y": 420, "freq": 2.5, "phase": 0.0},

    {"time":  8.6,  "type": "spike", "size": "large"},
    {"time":  8.72, "type": "spike", "size": "medium"},
    {"time":  8.84, "type": "spike", "size": "small"},

    {"time":  9.3,  "type": "spike", "size": "medium"},
    {"time":  9.42, "type": "spike", "size": "large"},
    {"time":  9.54, "type": "spike", "size": "medium"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time": 10.2,  "type": "platform", "y": 520, "width": 140},
    {"time": 10.2,  "type": "spike", "size": "large"},
    {"time": 10.32, "type": "spike", "size": "medium"},

    {"time": 10.8,  "type": "spike", "size": "small"},
    {"time": 10.92, "type": "spike", "size": "medium"},
    {"time": 11.04, "type": "spike", "size": "large"},

    {"time": 11.5,  "type": "spike", "size": "medium"},
    {"time": 11.62, "type": "spike", "size": "large"},
    {"time": 11.74, "type": "spike", "size": "medium"},

    {"time": 12.2,  "type": "spike", "size": "large"},
    {"time": 12.32, "type": "spike", "size": "medium"},
    {"time": 12.44, "type": "spike", "size": "small"},

    # ── Laser + espinhos ─────────────────────────────────────────────
    {"time": 13.0,  "type": "pulse_laser", "y": 380, "freq": 3.0, "phase": 1.0},

    {"time": 13.6,  "type": "spike", "size": "medium"},
    {"time": 13.72, "type": "spike", "size": "large"},
    {"time": 13.84, "type": "spike", "size": "medium"},

    {"time": 14.3,  "type": "spike", "size": "large"},
    {"time": 14.42, "type": "spike", "size": "medium"},
    {"time": 14.54, "type": "spike", "size": "large"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time": 15.2,  "type": "platform", "y": 520, "width": 130},
    {"time": 15.2,  "type": "spike", "size": "large"},
    {"time": 15.32, "type": "spike", "size": "medium"},

    {"time": 15.8,  "type": "spike", "size": "small"},
    {"time": 15.92, "type": "spike", "size": "medium"},
    {"time": 16.04, "type": "spike", "size": "large"},

    {"time": 16.5,  "type": "spike", "size": "medium"},
    {"time": 16.62, "type": "spike", "size": "large"},
    {"time": 16.74, "type": "spike", "size": "medium"},

    {"time": 17.2,  "type": "spike", "size": "large"},
    {"time": 17.32, "type": "spike", "size": "small"},
    {"time": 17.44, "type": "spike", "size": "large"},

    # ── Escadinha de plataformas ─────────────────────────────────────
    {"time": 18.2,  "type": "platform", "y": 530, "width": 120},
    {"time": 18.2,  "type": "spike", "size": "medium"},
    {"time": 18.32, "type": "spike", "size": "large"},

    {"time": 18.9,  "type": "platform", "y": 490, "width": 120},
    {"time": 18.9,  "type": "spike", "size": "large"},
    {"time": 19.02, "type": "spike", "size": "medium"},

    {"time": 19.6,  "type": "platform", "y": 450, "width": 120},
    {"time": 19.6,  "type": "spike", "size": "medium"},
    {"time": 19.72, "type": "spike", "size": "small"},

    {"time": 20.3,  "type": "platform", "y": 415, "width": 120},
    {"time": 20.3,  "type": "spike", "size": "large"},
    {"time": 20.42, "type": "spike", "size": "medium"},

    # ── Laser duplo ──────────────────────────────────────────────────
    {"time": 21.2,  "type": "pulse_laser", "y": 350, "freq": 2.8, "phase": 0.0},
    {"time": 21.2,  "type": "pulse_laser", "y": 480, "freq": 2.8, "phase": 3.14},

    {"time": 22.0,  "type": "spike", "size": "small"},
    {"time": 22.12, "type": "spike", "size": "medium"},
    {"time": 22.24, "type": "spike", "size": "large"},

    {"time": 22.7,  "type": "spike", "size": "medium"},
    {"time": 22.82, "type": "spike", "size": "large"},
    {"time": 22.94, "type": "spike", "size": "medium"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time": 23.6,  "type": "platform", "y": 520, "width": 130},
    {"time": 23.6,  "type": "spike", "size": "large"},
    {"time": 23.72, "type": "spike", "size": "medium"},

    {"time": 24.2,  "type": "spike", "size": "medium"},
    {"time": 24.32, "type": "spike", "size": "small"},
    {"time": 24.44, "type": "spike", "size": "medium"},

    {"time": 24.9,  "type": "spike", "size": "large"},
    {"time": 25.02, "type": "spike", "size": "medium"},
    {"time": 25.14, "type": "spike", "size": "small"},

    {"time": 25.6,  "type": "spike", "size": "medium"},
    {"time": 25.72, "type": "spike", "size": "large"},
    {"time": 25.84, "type": "spike", "size": "medium"},

    # ── Laser rápido ─────────────────────────────────────────────────
    {"time": 26.5,  "type": "pulse_laser", "y": 400, "freq": 4.0, "phase": 0.5},

    {"time": 27.1,  "type": "spike", "size": "large"},
    {"time": 27.22, "type": "spike", "size": "medium"},
    {"time": 27.34, "type": "spike", "size": "large"},

    {"time": 27.8,  "type": "spike", "size": "medium"},
    {"time": 27.92, "type": "spike", "size": "large"},
    {"time": 28.04, "type": "spike", "size": "medium"},

    # ── Escadinha ────────────────────────────────────────────────────
    {"time": 28.8,  "type": "platform", "y": 525, "width": 110},
    {"time": 28.8,  "type": "spike", "size": "large"},
    {"time": 28.92, "type": "spike", "size": "medium"},

    {"time": 29.5,  "type": "platform", "y": 485, "width": 110},
    {"time": 29.5,  "type": "spike", "size": "medium"},
    {"time": 29.62, "type": "spike", "size": "large"},

    {"time": 30.2,  "type": "platform", "y": 445, "width": 110},
    {"time": 30.2,  "type": "spike", "size": "small"},
    {"time": 30.32, "type": "spike", "size": "medium"},

    {"time": 30.9,  "type": "platform", "y": 408, "width": 110},
    {"time": 30.9,  "type": "spike", "size": "large"},
    {"time": 31.02, "type": "spike", "size": "medium"},

    {"time": 31.6,  "type": "spike", "size": "medium"},
    {"time": 31.72, "type": "spike", "size": "large"},
    {"time": 31.84, "type": "spike", "size": "medium"},

    {"time": 32.3,  "type": "spike", "size": "small"},
    {"time": 32.42, "type": "spike", "size": "medium"},
    {"time": 32.54, "type": "spike", "size": "large"},

    # ── Laser + espinhos densos ──────────────────────────────────────
    {"time": 33.2,  "type": "pulse_laser", "y": 370, "freq": 3.5, "phase": 0.0},
    {"time": 33.2,  "type": "pulse_laser", "y": 500, "freq": 3.5, "phase": 3.14},

    {"time": 34.0,  "type": "spike", "size": "large"},
    {"time": 34.12, "type": "spike", "size": "medium"},
    {"time": 34.24, "type": "spike", "size": "large"},

    {"time": 34.7,  "type": "spike", "size": "medium"},
    {"time": 34.82, "type": "spike", "size": "small"},
    {"time": 34.94, "type": "spike", "size": "medium"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time": 35.7,  "type": "platform", "y": 520, "width": 120},
    {"time": 35.7,  "type": "spike", "size": "large"},
    {"time": 35.82, "type": "spike", "size": "medium"},

    {"time": 36.4,  "type": "spike", "size": "medium"},
    {"time": 36.52, "type": "spike", "size": "large"},
    {"time": 36.64, "type": "spike", "size": "medium"},

    {"time": 37.1,  "type": "spike", "size": "large"},
    {"time": 37.22, "type": "spike", "size": "medium"},
    {"time": 37.34, "type": "spike", "size": "small"},

    {"time": 37.8,  "type": "spike", "size": "small"},
    {"time": 37.92, "type": "spike", "size": "medium"},
    {"time": 38.04, "type": "spike", "size": "large"},

    # ── Escadinha longa ──────────────────────────────────────────────
    {"time": 38.8,  "type": "platform", "y": 530, "width": 110},
    {"time": 38.8,  "type": "spike", "size": "large"},
    {"time": 38.92, "type": "spike", "size": "medium"},

    {"time": 39.5,  "type": "platform", "y": 490, "width": 110},
    {"time": 39.5,  "type": "spike", "size": "medium"},
    {"time": 39.62, "type": "spike", "size": "small"},

    {"time": 40.2,  "type": "platform", "y": 450, "width": 110},
    {"time": 40.2,  "type": "spike", "size": "large"},
    {"time": 40.32, "type": "spike", "size": "medium"},

    {"time": 40.9,  "type": "platform", "y": 415, "width": 110},
    {"time": 40.9,  "type": "spike", "size": "medium"},
    {"time": 41.02, "type": "spike", "size": "large"},

    {"time": 41.6,  "type": "platform", "y": 380, "width": 110},
    {"time": 41.6,  "type": "spike", "size": "small"},
    {"time": 41.72, "type": "spike", "size": "medium"},

    # ── Laser rápido pós-escadinha ────────────────────────────────────
    {"time": 42.5,  "type": "pulse_laser", "y": 410, "freq": 4.5, "phase": 1.0},

    {"time": 43.1,  "type": "spike", "size": "medium"},
    {"time": 43.22, "type": "spike", "size": "large"},
    {"time": 43.34, "type": "spike", "size": "medium"},

    {"time": 43.8,  "type": "spike", "size": "large"},
    {"time": 43.92, "type": "spike", "size": "medium"},
    {"time": 44.04, "type": "spike", "size": "large"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time": 44.8,  "type": "platform", "y": 520, "width": 120},
    {"time": 44.8,  "type": "spike", "size": "large"},
    {"time": 44.92, "type": "spike", "size": "medium"},

    {"time": 45.5,  "type": "spike", "size": "medium"},
    {"time": 45.62, "type": "spike", "size": "large"},
    {"time": 45.74, "type": "spike", "size": "medium"},

    {"time": 46.2,  "type": "spike", "size": "large"},
    {"time": 46.32, "type": "spike", "size": "medium"},
    {"time": 46.44, "type": "spike", "size": "small"},

    {"time": 46.9,  "type": "spike", "size": "medium"},
    {"time": 47.02, "type": "spike", "size": "small"},
    {"time": 47.14, "type": "spike", "size": "medium"},

    # ── Escadinha ────────────────────────────────────────────────────
    {"time": 47.9,  "type": "platform", "y": 525, "width": 105},
    {"time": 47.9,  "type": "spike", "size": "large"},
    {"time": 48.02, "type": "spike", "size": "medium"},

    {"time": 48.6,  "type": "platform", "y": 485, "width": 105},
    {"time": 48.6,  "type": "spike", "size": "medium"},
    {"time": 48.72, "type": "spike", "size": "large"},

    {"time": 49.3,  "type": "platform", "y": 445, "width": 105},
    {"time": 49.3,  "type": "spike", "size": "small"},
    {"time": 49.42, "type": "spike", "size": "medium"},

    {"time": 50.0,  "type": "platform", "y": 410, "width": 105},
    {"time": 50.0,  "type": "spike", "size": "large"},
    {"time": 50.12, "type": "spike", "size": "medium"},

    {"time": 50.7,  "type": "platform", "y": 375, "width": 105},
    {"time": 50.7,  "type": "spike", "size": "medium"},
    {"time": 50.82, "type": "spike", "size": "small"},

    # ── Lasers triplos ────────────────────────────────────────────────
    {"time": 51.7,  "type": "pulse_laser", "y": 330, "freq": 3.0, "phase": 0.0},
    {"time": 51.7,  "type": "pulse_laser", "y": 430, "freq": 3.0, "phase": 2.09},
    {"time": 51.7,  "type": "pulse_laser", "y": 520, "freq": 3.0, "phase": 4.18},

    {"time": 52.5,  "type": "spike", "size": "large"},
    {"time": 52.62, "type": "spike", "size": "medium"},
    {"time": 52.74, "type": "spike", "size": "large"},

    {"time": 53.2,  "type": "spike", "size": "medium"},
    {"time": 53.32, "type": "spike", "size": "large"},
    {"time": 53.44, "type": "spike", "size": "medium"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time": 54.1,  "type": "platform", "y": 520, "width": 120},
    {"time": 54.1,  "type": "spike", "size": "large"},
    {"time": 54.22, "type": "spike", "size": "medium"},

    {"time": 54.8,  "type": "spike", "size": "small"},
    {"time": 54.92, "type": "spike", "size": "medium"},
    {"time": 55.04, "type": "spike", "size": "large"},

    {"time": 55.5,  "type": "spike", "size": "medium"},
    {"time": 55.62, "type": "spike", "size": "large"},
    {"time": 55.74, "type": "spike", "size": "medium"},

    {"time": 56.2,  "type": "spike", "size": "large"},
    {"time": 56.32, "type": "spike", "size": "small"},
    {"time": 56.44, "type": "spike", "size": "large"},

    # ── Escadinha longa com laser ─────────────────────────────────────
    {"time": 57.2,  "type": "platform", "y": 530, "width": 105},
    {"time": 57.2,  "type": "spike", "size": "large"},
    {"time": 57.32, "type": "spike", "size": "medium"},

    {"time": 57.9,  "type": "platform", "y": 490, "width": 105},
    {"time": 57.9,  "type": "spike", "size": "medium"},
    {"time": 58.02, "type": "spike", "size": "large"},

    {"time": 58.6,  "type": "platform", "y": 450, "width": 105},
    {"time": 58.6,  "type": "spike", "size": "small"},
    {"time": 58.72, "type": "spike", "size": "medium"},

    {"time": 59.3,  "type": "platform", "y": 415, "width": 105},
    {"time": 59.3,  "type": "spike", "size": "large"},
    {"time": 59.42, "type": "spike", "size": "medium"},

    {"time": 60.0,  "type": "platform", "y": 380, "width": 105},
    {"time": 60.0,  "type": "spike", "size": "medium"},
    {"time": 60.12, "type": "spike", "size": "small"},

    {"time": 60.7,  "type": "platform", "y": 345, "width": 105},
    {"time": 60.7,  "type": "spike", "size": "large"},
    {"time": 60.82, "type": "spike", "size": "medium"},

    {"time": 61.5,  "type": "pulse_laser", "y": 390, "freq": 5.0, "phase": 0.0},

    {"time": 62.1,  "type": "spike", "size": "medium"},
    {"time": 62.22, "type": "spike", "size": "large"},
    {"time": 62.34, "type": "spike", "size": "medium"},

    {"time": 62.8,  "type": "spike", "size": "large"},
    {"time": 62.92, "type": "spike", "size": "medium"},
    {"time": 63.04, "type": "spike", "size": "large"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time": 63.8,  "type": "platform", "y": 520, "width": 115},
    {"time": 63.8,  "type": "spike", "size": "large"},
    {"time": 63.92, "type": "spike", "size": "medium"},

    {"time": 64.4,  "type": "spike", "size": "medium"},
    {"time": 64.52, "type": "spike", "size": "large"},
    {"time": 64.64, "type": "spike", "size": "medium"},

    {"time": 65.1,  "type": "spike", "size": "large"},
    {"time": 65.22, "type": "spike", "size": "medium"},
    {"time": 65.34, "type": "spike", "size": "small"},

    {"time": 65.8,  "type": "spike", "size": "small"},
    {"time": 65.92, "type": "spike", "size": "medium"},
    {"time": 66.04, "type": "spike", "size": "large"},

    # ── Lasers duplos rápidos ─────────────────────────────────────────
    {"time": 66.8,  "type": "pulse_laser", "y": 360, "freq": 4.0, "phase": 0.0},
    {"time": 66.8,  "type": "pulse_laser", "y": 510, "freq": 4.0, "phase": 3.14},

    {"time": 67.5,  "type": "spike", "size": "medium"},
    {"time": 67.62, "type": "spike", "size": "large"},
    {"time": 67.74, "type": "spike", "size": "medium"},

    {"time": 68.2,  "type": "spike", "size": "large"},
    {"time": 68.32, "type": "spike", "size": "medium"},
    {"time": 68.44, "type": "spike", "size": "large"},

    # ── Escadinha final ──────────────────────────────────────────────
    {"time": 69.2,  "type": "platform", "y": 525, "width": 105},
    {"time": 69.2,  "type": "spike", "size": "large"},
    {"time": 69.32, "type": "spike", "size": "medium"},

    {"time": 69.9,  "type": "platform", "y": 485, "width": 105},
    {"time": 69.9,  "type": "spike", "size": "medium"},
    {"time": 70.02, "type": "spike", "size": "large"},

    {"time": 70.6,  "type": "platform", "y": 445, "width": 105},
    {"time": 70.6,  "type": "spike", "size": "small"},
    {"time": 70.72, "type": "spike", "size": "medium"},

    {"time": 71.3,  "type": "platform", "y": 408, "width": 105},
    {"time": 71.3,  "type": "spike", "size": "large"},
    {"time": 71.42, "type": "spike", "size": "medium"},

    {"time": 72.0,  "type": "platform", "y": 371, "width": 105},
    {"time": 72.0,  "type": "spike", "size": "medium"},
    {"time": 72.12, "type": "spike", "size": "small"},

    {"time": 72.7,  "type": "platform", "y": 334, "width": 105},
    {"time": 72.7,  "type": "spike", "size": "large"},
    {"time": 72.82, "type": "spike", "size": "medium"},

    # ── Laser intenso ─────────────────────────────────────────────────
    {"time": 73.6,  "type": "pulse_laser", "y": 340, "freq": 5.5, "phase": 0.0},
    {"time": 73.6,  "type": "pulse_laser", "y": 470, "freq": 5.5, "phase": 1.57},

    {"time": 74.3,  "type": "spike", "size": "large"},
    {"time": 74.42, "type": "spike", "size": "medium"},
    {"time": 74.54, "type": "spike", "size": "large"},

    {"time": 74.9,  "type": "spike", "size": "medium"},
    {"time": 75.02, "type": "spike", "size": "large"},
    {"time": 75.14, "type": "spike", "size": "medium"},

    # ── Plataforma ───────────────────────────────────────────────────
    {"time": 75.9,  "type": "platform", "y": 520, "width": 115},
    {"time": 75.9,  "type": "spike", "size": "large"},
    {"time": 76.02, "type": "spike", "size": "medium"},

    {"time": 76.5,  "type": "spike", "size": "medium"},
    {"time": 76.62, "type": "spike", "size": "large"},
    {"time": 76.74, "type": "spike", "size": "medium"},

    {"time": 77.2,  "type": "spike", "size": "large"},
    {"time": 77.32, "type": "spike", "size": "medium"},
    {"time": 77.44, "type": "spike", "size": "small"},

    {"time": 77.9,  "type": "spike", "size": "small"},
    {"time": 78.02, "type": "spike", "size": "medium"},
    {"time": 78.14, "type": "spike", "size": "large"},

    {"time": 78.6,  "type": "spike", "size": "medium"},
    {"time": 78.72, "type": "spike", "size": "large"},
    {"time": 78.84, "type": "spike", "size": "medium"},

    # ── Clímax: lasers + espinhos densos ─────────────────────────────
    {"time": 79.6,  "type": "pulse_laser", "y": 350, "freq": 6.0, "phase": 0.0},
    {"time": 79.6,  "type": "pulse_laser", "y": 490, "freq": 6.0, "phase": 3.14},

    {"time": 80.3,  "type": "spike", "size": "large"},
    {"time": 80.42, "type": "spike", "size": "medium"},
    {"time": 80.54, "type": "spike", "size": "large"},

    {"time": 81.0,  "type": "spike", "size": "medium"},
    {"time": 81.12, "type": "spike", "size": "large"},
    {"time": 81.24, "type": "spike", "size": "medium"},

    {"time": 81.7,  "type": "spike", "size": "large"},
    {"time": 81.82, "type": "spike", "size": "medium"},
    {"time": 81.94, "type": "spike", "size": "small"},

    {"time": 82.5,  "type": "spike", "size": "small"},
    {"time": 82.62, "type": "spike", "size": "medium"},
    {"time": 82.74, "type": "spike", "size": "large"},

    {"time": 83.2,  "type": "spike", "size": "medium"},
    {"time": 83.32, "type": "spike", "size": "large"},
    {"time": 83.44, "type": "spike", "size": "medium"},

    {"time": 83.9,  "type": "pulse_laser", "y": 400, "freq": 7.0, "phase": 0.8},

    {"time": 84.5,  "type": "spike", "size": "large"},
    {"time": 84.62, "type": "spike", "size": "medium"},
    {"time": 84.74, "type": "spike", "size": "large"},

    {"time": 85.2,  "type": "spike", "size": "medium"},
    {"time": 85.32, "type": "spike", "size": "large"},
    {"time": 85.44, "type": "spike", "size": "medium"},

    {"time": 85.9,  "type": "spike", "size": "large"},
    {"time": 86.02, "type": "spike", "size": "medium"},
    {"time": 86.14, "type": "spike", "size": "small"},

    {"time": 86.6,  "type": "spike", "size": "small"},
    {"time": 86.72, "type": "spike", "size": "medium"},
    {"time": 86.84, "type": "spike", "size": "large"},

    {"time": 87.3,  "type": "spike", "size": "medium"},
    {"time": 87.42, "type": "spike", "size": "large"},
    {"time": 87.54, "type": "spike", "size": "medium"},

    {"time": 88.0,  "type": "spike", "size": "large"},
    {"time": 88.12, "type": "spike", "size": "medium"},
    {"time": 88.24, "type": "spike", "size": "large"},

    {"time": 88.7,  "type": "spike", "size": "medium"},
    {"time": 88.82, "type": "spike", "size": "large"},
    {"time": 88.94, "type": "spike", "size": "medium"},

    {"time": 89.4,  "type": "spike", "size": "large"},
    {"time": 89.52, "type": "spike", "size": "medium"},
    {"time": 89.64, "type": "spike", "size": "small"},
]
