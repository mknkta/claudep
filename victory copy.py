import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

FLASH = 0.3
ANIM  = 0.8


class VictoryScene:
    def __init__(self, manager, clock, attempts, snapshot):
        self._manager  = manager
        self._clock    = clock
        self._attempts = attempts
        self._snap     = snapshot
        self._t        = 0.0
        self._hov      = False

        self._tf = pygame.font.SysFont("consolas", 72, bold=True)
        self._mf = pygame.font.SysFont("consolas", 28)
        self._bf = pygame.font.SysFont("consolas", 22, bold=True)

        self._title = self._tf.render("LEVEL COMPLETE", True, (255,230,80))
        pw, ph = 260, 55
        self._btn = pygame.Rect((SCREEN_WIDTH-pw)//2, SCREEN_HEIGHT//2+140, pw, ph)

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self._t > FLASH and self._btn.collidepoint(pygame.mouse.get_pos()):
                    from menu import MenuScene
                    self._manager.go(MenuScene(self._manager, self._clock))

    def update(self, dt):
        self._t  += dt
        self._hov = self._btn.collidepoint(pygame.mouse.get_pos())

    def draw(self, screen):
        if self._snap: screen.blit(self._snap, (0,0))

        if self._t < FLASH:
            a = int(255 * (1 - self._t / FLASH))
            f = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            f.fill((255,255,255)); f.set_alpha(a)
            screen.blit(f, (0,0)); return

        ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        ov.fill((0,0,0,160)); screen.blit(ov, (0,0))

        t = min((self._t - FLASH) / ANIM, 1.0)
        scale = (0.1 + 1.1*t/0.7) if t < 0.7 else (1.2 - 0.2*(t-0.7)/0.3)
        w, h = int(self._title.get_width()*scale), int(self._title.get_height()*scale)
        if w > 0 and h > 0:
            sc = pygame.transform.scale(self._title, (w, h))
            screen.blit(sc, sc.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-40)))

        if t >= 1.0:
            s = self._attempts
            sub = self._mf.render(
                f"Venceu em {s} tentativa{'s' if s!=1 else ''}!", True, (200,180,255))
            screen.blit(sub, sub.get_rect(centerx=SCREEN_WIDTH//2, centery=SCREEN_HEIGHT//2+60))

            bw = int(self._btn.w*(1.05 if self._hov else 1))
            bh = int(self._btn.h*(1.05 if self._hov else 1))
            br = pygame.Rect(self._btn.centerx-bw//2, self._btn.centery-bh//2, bw, bh)
            pygame.draw.rect(screen, (30,25,45),   br, border_radius=8)
            pygame.draw.rect(screen, (100,120,220), br,
                             width=3 if self._hov else 1, border_radius=8)
            bt = self._bf.render("Menu Principal", True,
                                 (100,120,220) if self._hov else (160,150,180))
            screen.blit(bt, bt.get_rect(center=br.center))
