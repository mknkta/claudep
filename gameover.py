import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

BW, BH = 200, 55


class GameOverScene:
    def __init__(self, manager, clock, phase, speed, hscale, zoom,
                 attempts, progress_pct, snapshot):
        self._manager  = manager
        self._clock    = clock
        self._phase    = phase
        self._speed    = speed
        self._hscale   = hscale
        self._zoom     = zoom
        self._attempts = attempts
        self._pct      = progress_pct
        self._snap     = snapshot

        self._bf = pygame.font.SysFont("consolas", 48, bold=True)
        self._mf = pygame.font.SysFont("consolas", 26)
        self._sf = pygame.font.SysFont("consolas", 22, bold=True)

        pw, ph = 560, 320
        self._panel = pygame.Rect((SCREEN_WIDTH-pw)//2, (SCREEN_HEIGHT-ph)//2, pw, ph)
        gap = 30; bx = self._panel.centerx - (2*BW+gap)//2; by = self._panel.bottom-BH-30
        self._br = pygame.Rect(bx,       by, BW, BH)
        self._bm = pygame.Rect(bx+BW+gap, by, BW, BH)
        self._hov = None

        self._ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self._ov.fill((0,0,0,170))

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mp = pygame.mouse.get_pos()
                if self._br.collidepoint(mp): self._restart()
                elif self._bm.collidepoint(mp): self._menu()

    def _restart(self):
        from gameplay import GameplayScene
        s = GameplayScene(self._speed, self._hscale, self._zoom, self._phase, self._manager)
        s.set_clock(self._clock)
        self._manager.go(s)

    def _menu(self):
        from menu import MenuScene
        self._manager.go(MenuScene(self._manager, self._clock))

    def update(self, dt):
        mp = pygame.mouse.get_pos()
        self._hov = "r" if self._br.collidepoint(mp) else "m" if self._bm.collidepoint(mp) else None

    def draw(self, screen):
        if self._snap: screen.blit(self._snap, (0,0))
        screen.blit(self._ov, (0,0))

        pygame.draw.rect(screen, (20,16,35),   self._panel, border_radius=14)
        pygame.draw.rect(screen, (120,80,180), self._panel, width=2, border_radius=14)

        t = self._bf.render(f"Tentativa #{self._attempts}", True, (220,180,255))
        screen.blit(t, t.get_rect(centerx=self._panel.centerx, centery=self._panel.y+65))

        p = self._mf.render(f"Você completou {self._pct:.1f}%", True, (160,140,200))
        screen.blit(p, p.get_rect(centerx=self._panel.centerx, centery=self._panel.y+130))

        bw, bh, bx, by = 400, 12, self._panel.centerx-200, self._panel.y+160
        pygame.draw.rect(screen, (50,40,70), (bx,by,bw,bh), border_radius=6)
        fill = int(bw * self._pct / 100)
        if fill: pygame.draw.rect(screen, (140,80,220), (bx,by,fill,bh), border_radius=6)

        self._btn(screen, self._br, "Reiniciar",      (80,200,120),  self._hov=="r")
        self._btn(screen, self._bm, "Menu Principal", (100,120,220), self._hov=="m")

    def _btn(self, screen, rect, label, color, hov):
        w, h = int(rect.w*(1.05 if hov else 1)), int(rect.h*(1.05 if hov else 1))
        r = pygame.Rect(rect.centerx-w//2, rect.centery-h//2, w, h)
        pygame.draw.rect(screen, (30,25,45), r, border_radius=8)
        pygame.draw.rect(screen, color, r, width=3 if hov else 2, border_radius=8)
        t = self._sf.render(label, True, color if hov else (160,150,180))
        screen.blit(t, t.get_rect(center=r.center))
