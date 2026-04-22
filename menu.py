import math, random
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

PHASE_COLORS = {1: (0,255,255), 2: (255,0,255), 3: (0,255,80)}
BG    = (20, 18, 32)
TITLE = (220, 200, 255)


class _Shape:
    TYPES = ("rect", "circle", "triangle")
    def __init__(self, initial=True):
        self.x  = random.uniform(0, SCREEN_WIDTH)
        self.y  = random.uniform(0, SCREEN_HEIGHT) if initial else random.choice([-60, SCREEN_HEIGHT+60])
        self.vx = random.choice([-1,1]) * random.uniform(15, 35)
        self.vy = random.choice([-1,1]) * random.uniform(15, 35)
        self.sz = random.randint(30, 75)
        self.angle = random.uniform(0, 360)
        self.rot   = random.uniform(-15, 15)
        self.shape = random.choice(self.TYPES)
        r = random.choice([(100,80,220),(0,200,200),(200,0,200),(220,180,0),(0,180,80)])
        self.color = (*r, 40)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.angle = (self.angle + self.rot * dt) % 360
        if not (-100 < self.x < SCREEN_WIDTH+100 and -100 < self.y < SCREEN_HEIGHT+100):
            self.__init__(initial=False)

    def draw(self, screen):
        s = self.sz
        buf = pygame.Surface((s*2+4, s*2+4), pygame.SRCALPHA)
        cx, cy = s+2, s+2
        if self.shape == "rect":
            rs = pygame.Surface((s, s), pygame.SRCALPHA); rs.fill(self.color)
            rot = pygame.transform.rotate(rs, self.angle)
            buf.blit(rot, rot.get_rect(center=(cx, cy)))
        elif self.shape == "circle":
            pygame.draw.circle(buf, self.color, (cx, cy), s//2)
        else:
            rad = math.radians(self.angle)
            ca, sa = math.cos(rad), math.sin(rad)
            base = [(cx, cy-s//2), (cx-s//2, cy+s//2), (cx+s//2, cy+s//2)]
            pts  = [(cx+ca*(px-cx)-sa*(py-cy), cy+sa*(px-cx)+ca*(py-cy)) for px,py in base]
            pygame.draw.polygon(buf, self.color, pts)
        screen.blit(buf, (int(self.x)-s-2, int(self.y)-s-2))


class _Btn:
    def __init__(self, rect, label, color):
        self.rect  = rect
        self.label = label
        self.color = color
        self._hov  = False
        self._font = None

    def _f(self, sz): return pygame.font.SysFont("consolas", sz, bold=True)

    def update(self, mp): self._hov = self.rect.collidepoint(mp)

    def clicked(self, mp, pressed): return self.rect.collidepoint(mp) and pressed

    def draw(self, screen):
        sc = 1.05 if self._hov else 1.0
        w  = int(self.rect.w * sc); h = int(self.rect.h * sc)
        cx, cy = self.rect.center
        r = pygame.Rect(cx-w//2, cy-h//2, w, h)
        pygame.draw.rect(screen, (30,25,45), r, border_radius=10)
        pygame.draw.rect(screen, self.color if self._hov else (80,70,100),
                         r, width=3 if self._hov else 1, border_radius=10)
        f = self._f(30 if self._hov else 26)
        t = f.render(self.label, True, self.color if self._hov else (180,170,200))
        screen.blit(t, t.get_rect(center=r.center))


class MenuScene:
    def __init__(self, manager, clock):
        self._manager = manager
        self._clock   = clock
        self._shapes  = [_Shape() for _ in range(8)]
        self._msg     = ""
        self._msg_t   = 0.0

        bw, bh = 260, 90; gap = 40
        total  = 3*bw + 2*gap
        sx     = (SCREEN_WIDTH - total) // 2
        by     = SCREEN_HEIGHT // 2 + 30
        self._btns = [
            _Btn(pygame.Rect(sx + i*(bw+gap), by, bw, bh), f"Fase {i+1}", PHASE_COLORS[i+1])
            for i in range(3)
        ]
        self._tf = pygame.font.SysFont("consolas", 64, bold=True)
        self._sf = pygame.font.SysFont("consolas", 18)

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mp = pygame.mouse.get_pos()
                for i, btn in enumerate(self._btns):
                    if btn.clicked(mp, True):
                        if i+1 in (2, 3):
                            self._msg = f"Fase {i+1} — Em breve!"; self._msg_t = 2.5
                        else:
                            from difficulty import DifficultyScene
                            self._manager.go(DifficultyScene(self._manager, self._clock, i+1))

    def update(self, dt):
        mp = pygame.mouse.get_pos()
        for b in self._btns: b.update(mp)
        for s in self._shapes: s.update(dt)
        if self._msg_t > 0: self._msg_t -= dt

    def draw(self, screen):
        screen.fill(BG)
        for s in self._shapes: s.draw(screen)

        t = self._tf.render("GEOMETRY DASH", True, TITLE)
        screen.blit(t, t.get_rect(centerx=SCREEN_WIDTH//2, centery=SCREEN_HEIGHT//2-80))

        sub = self._sf.render("Escolha uma fase para começar", True, (120,110,150))
        screen.blit(sub, sub.get_rect(centerx=SCREEN_WIDTH//2, centery=SCREEN_HEIGHT//2-20))

        for b in self._btns: b.draw(screen)

        if self._msg_t > 0:
            m = self._sf.render(self._msg, True, (255,200,80))
            screen.blit(m, m.get_rect(centerx=SCREEN_WIDTH//2, centery=SCREEN_HEIGHT//2+160))
