"""
menu.py — Tela inicial do jogo (MenuScene).

Exibe o título, botões de seleção de fase e botão de ranking.
Botões possuem efeitos visuais (hover/scale) e sonoros (beep).
"""

import math
import random
import pygame
import audio
from config import SCREEN_WIDTH, SCREEN_HEIGHT

PHASE_COLORS = {1: (0,255,255), 2: (255,0,255), 3: (0,255,80)}
BG    = (20, 18, 32)
TITLE = (220, 200, 255)


class _Shape:
    """Forma geométrica decorativa animada no fundo do menu."""

    TYPES = ("rect", "circle", "triangle")

    def __init__(self, initial=True):
        """Inicializa a forma com posição, velocidade e tipo aleatórios."""
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
        """Atualiza posição e ângulo; reinicia quando sai da tela."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.angle = (self.angle + self.rot * dt) % 360
        if not (-100 < self.x < SCREEN_WIDTH+100 and -100 < self.y < SCREEN_HEIGHT+100):
            self.__init__(initial=False)

    def draw(self, screen):
        """Desenha a forma semi-transparente na tela."""
        s = self.sz
        buf = pygame.Surface((s*2+4, s*2+4), pygame.SRCALPHA)
        cx, cy = s+2, s+2
        if self.shape == "rect":
            rs = pygame.Surface((s, s), pygame.SRCALPHA)
            rs.fill(self.color)
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
    """Botão interativo com efeito de escala no hover e som ao clicar/passar."""

    def __init__(self, rect, label, color):
        """
        Inicializa o botão.

        Args:
            rect: pygame.Rect com a posição e tamanho do botão.
            label: Texto exibido no botão.
            color: Cor de destaque do botão.
        """
        self.rect  = rect
        self.label = label
        self.color = color
        self._hov  = False
        self._font = None

    def _f(self, sz):
        """Retorna fonte Consolas em tamanho sz."""
        return pygame.font.SysFont("consolas", sz, bold=True)

    def update(self, mp):
        """Atualiza estado de hover e toca som ao entrar no botão."""
        was_hov = self._hov
        self._hov = self.rect.collidepoint(mp)
        if self._hov and not was_hov:
            audio.play_hover()

    def clicked(self, mp, pressed):
        """Retorna True se o mouse está sobre o botão e pressionado."""
        return self.rect.collidepoint(mp) and pressed

    def draw(self, screen):
        """Desenha o botão com escala maior no hover."""
        sc = 1.05 if self._hov else 1.0
        w  = int(self.rect.w * sc)
        h  = int(self.rect.h * sc)
        cx, cy = self.rect.center
        r = pygame.Rect(cx-w//2, cy-h//2, w, h)
        pygame.draw.rect(screen, (30,25,45), r, border_radius=10)
        pygame.draw.rect(screen, self.color if self._hov else (80,70,100),
                         r, width=3 if self._hov else 1, border_radius=10)
        f = self._f(30 if self._hov else 26)
        t = f.render(self.label, True, self.color if self._hov else (180,170,200))
        screen.blit(t, t.get_rect(center=r.center))


class MenuScene:
    """Tela inicial com seleção de fase e botão Voltar para o ranking."""

    def __init__(self, manager, clock, player_name=""):
        """
        Inicializa o menu principal.

        Args:
            manager: Gerenciador de cenas para transições.
            clock: Clock do pygame.
            player_name: Nome do jogador atual.
        """
        self._manager     = manager
        self._clock       = clock
        self._player_name = player_name
        self._shapes      = [_Shape() for _ in range(8)]
        bw, bh = 260, 90
        gap    = 40
        total  = 3*bw + 2*gap
        sx     = (SCREEN_WIDTH - total) // 2
        by     = SCREEN_HEIGHT // 2 + 20
        self._btns = [
            _Btn(pygame.Rect(sx + i*(bw+gap), by, bw, bh), f"Fase {i+1}", PHASE_COLORS[i+1])
            for i in range(3)
        ]
        # botões inferiores
        self._rank_btn   = _Btn(pygame.Rect(30, SCREEN_HEIGHT - 70, 180, 48),
                                "Ranking", (140, 100, 220))
        self._change_btn = _Btn(pygame.Rect(SCREEN_WIDTH - 210, SCREEN_HEIGHT - 70, 180, 48),
                                "Trocar jogador", (80, 160, 220))

        self._tf = pygame.font.SysFont("consolas", 64, bold=True)
        self._sf = pygame.font.SysFont("consolas", 18)
        self._nf = pygame.font.SysFont("consolas", 20, bold=True)

    def handle_events(self, events):
        """Processa cliques: inicia fase, abre ranking ou troca jogador."""
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mp = pygame.mouse.get_pos()
                for i, btn in enumerate(self._btns):
                    if btn.clicked(mp, True):
                        audio.play_click()
                        from difficulty import DifficultyScene
                        self._manager.go(DifficultyScene(
                            self._manager, self._clock, i+1, self._player_name))
                if self._rank_btn.clicked(mp, True):
                    audio.play_click()
                    from ranking import RankingScene
                    self._manager.go(RankingScene(
                        self._manager, self._clock, self._player_name))
                if self._change_btn.clicked(mp, True):
                    audio.play_click()
                    import saves
                    saves.reset_attempts()
                    from name_input import NameInputScene
                    self._manager.go(NameInputScene(self._manager, self._clock))

    def update(self, dt):
        """Atualiza hover dos botões e animação das formas decorativas."""
        mp = pygame.mouse.get_pos()
        for b in self._btns:
            b.update(mp)
        self._rank_btn.update(mp)
        self._change_btn.update(mp)
        for s in self._shapes:
            s.update(dt)

    def draw(self, screen):
        """Renderiza o fundo, formas, título e botões."""
        screen.fill(BG)
        for s in self._shapes:
            s.draw(screen)

        t = self._tf.render("GEOMETRY DASH", True, TITLE)
        screen.blit(t, t.get_rect(centerx=SCREEN_WIDTH//2, centery=SCREEN_HEIGHT//2-90))

        sub = self._sf.render("Escolha uma fase para começar", True, (120,110,150))
        screen.blit(sub, sub.get_rect(centerx=SCREEN_WIDTH//2, centery=SCREEN_HEIGHT//2-30))

        for b in self._btns:
            b.draw(screen)

        # nome do jogador atual (centro inferior)
        if self._player_name:
            nt = self._nf.render(f"Jogador: {self._player_name}", True, (160, 140, 200))
            screen.blit(nt, nt.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 20))

        self._rank_btn.draw(screen)
        self._change_btn.draw(screen)
