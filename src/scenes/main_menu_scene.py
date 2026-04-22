# main_menu_scene.py — tela inicial com formas flutuantes e seleção de fase
import math
import random
import pygame
from src.scenes.scene import Scene
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS

# Paleta neon por fase
PHASE_COLORS = {
    1: (0,   255, 255),   # ciano
    2: (255,  0,  255),   # magenta
    3: (0,   255,  80),   # verde neon
}

TITLE_COLOR  = (220, 200, 255)
BG_COLOR     = (20,  18,  32)


# ──────────────────────────────────────────────────────────────────────
class _FloatingShape:
    TYPES = ("rect", "circle", "triangle")

    def __init__(self):
        self._reset(initial=True)

    def _reset(self, initial=False):
        self.x   = random.uniform(0, SCREEN_WIDTH)
        self.y   = random.uniform(0, SCREEN_HEIGHT) if initial else random.choice([-60, SCREEN_HEIGHT + 60])
        self.vx  = random.uniform(-25, 25)
        self.vy  = random.uniform(-20, 20)
        if abs(self.vx) < 5:  self.vx = 5 * (1 if self.vx >= 0 else -1)
        if abs(self.vy) < 5:  self.vy = 5 * (1 if self.vy >= 0 else -1)
        self.size    = random.randint(30, 75)
        self.angle   = random.uniform(0, 360)
        self.rot_spd = random.uniform(-15, 15)
        self.shape   = random.choice(self.TYPES)
        r = random.choice([
            (100, 80, 220), (0, 200, 200), (200, 0, 200),
            (220, 180, 0),  (0, 180, 80),  (180, 80, 255),
        ])
        self.color = (*r, 40)   # RGBA, alpha baixo

    def update(self, dt: float):
        self.x    += self.vx * dt
        self.y    += self.vy * dt
        self.angle = (self.angle + self.rot_spd * dt) % 360
        # Rebote nas bordas
        if self.x < -100 or self.x > SCREEN_WIDTH + 100 or \
           self.y < -100 or self.y > SCREEN_HEIGHT + 100:
            self._reset()

    def draw(self, screen: pygame.Surface):
        s = self.size
        surf = pygame.Surface((s * 2 + 4, s * 2 + 4), pygame.SRCALPHA)

        if self.shape == "rect":
            rect_s = pygame.Surface((s, s), pygame.SRCALPHA)
            rect_s.fill(self.color)
            rotated = pygame.transform.rotate(rect_s, self.angle)
            surf.blit(rotated, rotated.get_rect(center=(s + 2, s + 2)))

        elif self.shape == "circle":
            pygame.draw.circle(surf, self.color, (s + 2, s + 2), s // 2)

        elif self.shape == "triangle":
            cx, cy = s + 2, s + 2
            pts_base = [
                (cx,         cy - s // 2),
                (cx - s // 2, cy + s // 2),
                (cx + s // 2, cy + s // 2),
            ]
            rad = math.radians(self.angle)
            cos_a, sin_a = math.cos(rad), math.sin(rad)
            pts = [
                (cx + cos_a * (px - cx) - sin_a * (py - cy),
                 cy + sin_a * (px - cx) + cos_a * (py - cy))
                for px, py in pts_base
            ]
            pygame.draw.polygon(surf, self.color, pts)

        screen.blit(surf, (int(self.x) - s - 2, int(self.y) - s - 2))


# ──────────────────────────────────────────────────────────────────────
class _Button:
    def __init__(self, rect: pygame.Rect, label: str, neon_color: tuple):
        self.rect       = rect
        self.label      = label
        self.neon_color = neon_color
        self._hovered   = False
        self._font      = None

    def _get_font(self, size=28) -> pygame.font.Font:
        return pygame.font.SysFont("consolas", size, bold=True)

    def handle_mouse(self, mouse_pos) -> bool:
        self._hovered = self.rect.collidepoint(mouse_pos)
        return self._hovered

    def is_clicked(self, mouse_pos, mouse_pressed) -> bool:
        return self.rect.collidepoint(mouse_pos) and mouse_pressed

    def draw(self, screen: pygame.Surface):
        if self._hovered:
            scale   = 1.05
            border_w = 3
            color   = self.neon_color
        else:
            scale   = 1.0
            border_w = 1
            color   = (80, 70, 100)

        w = int(self.rect.width  * scale)
        h = int(self.rect.height * scale)
        cx, cy = self.rect.center
        r = pygame.Rect(cx - w // 2, cy - h // 2, w, h)

        # Fundo
        pygame.draw.rect(screen, (30, 25, 45), r, border_radius=10)
        # Borda
        pygame.draw.rect(screen, color, r, width=border_w, border_radius=10)

        # Texto
        font = self._get_font(30 if self._hovered else 26)
        text = font.render(self.label, True, color if self._hovered else (180, 170, 200))
        screen.blit(text, text.get_rect(center=r.center))


# ──────────────────────────────────────────────────────────────────────
class MainMenuScene(Scene):
    def __init__(self, manager, clock):
        self._manager = manager
        self._clock   = clock
        self._shapes  = [_FloatingShape() for _ in range(8)]

        # Botões das 3 fases, centralizados
        bw, bh = 260, 90
        gap     = 40
        total_w = 3 * bw + 2 * gap
        start_x = (SCREEN_WIDTH - total_w) // 2
        btn_y   = SCREEN_HEIGHT // 2 + 30

        self._buttons = [
            _Button(pygame.Rect(start_x + i * (bw + gap), btn_y, bw, bh),
                    f"Fase {i + 1}", PHASE_COLORS[i + 1])
            for i in range(3)
        ]

        self._title_font = pygame.font.SysFont("consolas", 64, bold=True)
        self._sub_font   = pygame.font.SysFont("consolas", 18)
        self._msg        = ""   # mensagem "Em breve"
        self._msg_timer  = 0.0

    # ------------------------------------------------------------------
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mp = pygame.mouse.get_pos()
                for i, btn in enumerate(self._buttons):
                    if btn.is_clicked(mp, True):
                        phase = i + 1
                        if phase in (2, 3):
                            self._msg       = f"Fase {phase} — Em breve!"
                            self._msg_timer = 2.5
                        else:
                            from src.scenes.difficulty_select_scene import DifficultySelectScene
                            self._manager.change_scene(
                                DifficultySelectScene(self._manager, self._clock, phase)
                            )

    # ------------------------------------------------------------------
    def update(self, dt: float):
        mp = pygame.mouse.get_pos()
        for btn in self._buttons:
            btn.handle_mouse(mp)
        for shape in self._shapes:
            shape.update(dt)
        if self._msg_timer > 0:
            self._msg_timer -= dt

    # ------------------------------------------------------------------
    def draw(self, screen: pygame.Surface):
        screen.fill(BG_COLOR)

        for shape in self._shapes:
            shape.draw(screen)

        # Título
        title = self._title_font.render("GEOMETRY DASH", True, TITLE_COLOR)
        screen.blit(title, title.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2 - 80))

        sub = self._sub_font.render("Escolha uma fase para começar", True, (120, 110, 150))
        screen.blit(sub, sub.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2 - 20))

        for btn in self._buttons:
            btn.draw(screen)

        if self._msg_timer > 0:
            msg_surf = self._sub_font.render(self._msg, True, (255, 200, 80))
            screen.blit(msg_surf, msg_surf.get_rect(centerx=SCREEN_WIDTH // 2,
                                                    centery=SCREEN_HEIGHT // 2 + 160))
