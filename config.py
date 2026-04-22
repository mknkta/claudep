# config.py — constantes globais do jogo
# Centralizar aqui facilita ajustar valores sem precisar caçar no código.

# --- Janela ---
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
FPS           = 60

# --- Física ---
# GROUND_Y é o Y do topo do chão (pygame conta Y de cima pra baixo).
GROUND_Y = 600
GRAVITY      = 0.8   # pixels/frame²
SHIP_THRUST  = 0.9   # força de subida da nave por frame (segurar espaço)
CEILING_Y    = 40    # Y mínimo antes de matar no modo nave

# --- Velocidades por dificuldade (pixels/segundo) ---
SPEED_EASY   = 400
SPEED_MEDIUM = 600
SPEED_HARD   = 900

# --- Paleta de cores base (R, G, B) ---
COLORS = {
    "background": (30, 30, 40),   # cinza-azulado escuro
    "ground":     (80, 60, 40),   # marrom terra
    "grid":       (50, 50, 60),   # linhas de grade sutis
}
