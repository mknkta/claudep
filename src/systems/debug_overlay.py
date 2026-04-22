# debug_overlay.py — overlay de depuração ativado por F3
#
# Mostra: FPS, tempo da música, posição do player.
# Desenha: collision_rect do player (verde), de cada obstáculo (vermelho),
#          linha vertical amarela na posição X do player.

import pygame

_font: pygame.font.Font | None = None

# Cores
_GREEN  = (0,   255,  80)
_RED    = (255,  60,  60)
_YELLOW = (255, 220,   0)
_BG     = (0,    0,    0, 160)   # preto semi-transparente para o texto


def _get_font() -> pygame.font.Font:
    global _font
    if _font is None:
        _font = pygame.font.SysFont("consolas", 16)
    return _font


def draw(
    screen:        pygame.Surface,
    clock:         pygame.time.Clock,
    music_time:    float,
    player,                        # src.entities.player.Player
    active_obstacles: list,
):
    """Desenha o overlay completo. Chamar apenas quando F3 estiver ativo."""
    font = _get_font()

    # ------------------------------------------------------------------
    # Hitboxes
    # ------------------------------------------------------------------
    # Linha vertical no centro horizontal do player.
    pygame.draw.line(
        screen, _YELLOW,
        (player.rect.centerx, 0),
        (player.rect.centerx, screen.get_height()),
        width=1,
    )

    # Collision rects dos obstáculos em vermelho.
    for obs in active_obstacles:
        pygame.draw.rect(screen, _RED,    obs.collision_rect, width=1)

    # Collision rect do player em verde.
    col_r = getattr(player, "collision_rect", player.rect)
    pygame.draw.rect(screen, _GREEN, col_r, width=2)

    # ------------------------------------------------------------------
    # Painel de texto (canto superior esquerdo)
    # ------------------------------------------------------------------
    lines = [
        f"FPS:   {clock.get_fps():.1f}",
        f"Music: {music_time:.2f}s",
        f"Player X: {player.rect.x}  Y: {player.rect.y}",
        f"on_ground: {player.on_ground}",
        f"vel_y: {player.velocity_y:.2f}",
    ]

    padding = 6
    line_h  = font.get_linesize()
    panel_w = 220
    panel_h = len(lines) * line_h + padding * 2

    # Superfície semi-transparente de fundo.
    bg = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    bg.fill(_BG)
    screen.blit(bg, (4, 4))

    for i, line in enumerate(lines):
        surf = font.render(line, True, _YELLOW)
        screen.blit(surf, (4 + padding, 4 + padding + i * line_h))
