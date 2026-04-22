import pygame

_font = None
GREEN  = (0,   255,  80)
RED    = (255,  60,  60)
YELLOW = (255, 220,   0)

def draw(screen, clock, music_time, player, obstacles):
    global _font
    if _font is None:
        _font = pygame.font.SysFont("consolas", 16)

    pygame.draw.line(screen, YELLOW,
        (player.rect.centerx, 0), (player.rect.centerx, screen.get_height()), 1)

    for obs in obstacles:
        pygame.draw.rect(screen, RED, obs.collision_rect, 1)

    cr = getattr(player, "collision_rect", player.rect)
    pygame.draw.rect(screen, GREEN, cr, 2)

    lines = [
        f"FPS:   {clock.get_fps():.1f}",
        f"Music: {music_time:.2f}s",
        f"X:{player.rect.x}  Y:{player.rect.y}",
        f"on_ground: {player.on_ground}",
    ]
    lh = _font.get_linesize()
    bg = pygame.Surface((200, len(lines) * lh + 12), pygame.SRCALPHA)
    bg.fill((0, 0, 0, 160))
    screen.blit(bg, (4, 4))
    for i, l in enumerate(lines):
        screen.blit(_font.render(l, True, YELLOW), (10, 4 + 6 + i * lh))
