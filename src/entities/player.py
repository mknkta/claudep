# player.py — entidade principal do jogador no modo Cubo (Fase 1)
#
# CONCEITOS DE FÍSICA PARA INICIANTES
# ------------------------------------
# Velocidade (velocity_y): o quanto o cubo se move verticalmente a cada frame.
#   - Valor negativo → sobe (em pygame, Y=0 é o topo da tela).
#   - Valor positivo → desce.
#
# Gravidade: somamos um valor positivo pequeno (GRAVITY) à velocity_y todo frame.
#   Isso simula a aceleração gravitacional: o cubo sobe mais devagar,
#   para, e então cai cada vez mais rápido — exatamente como na vida real.
#
# Impulso de pulo: atribuímos um velocity_y muito negativo de uma vez só.
#   O cubo dispara pra cima. A gravidade vai desacelerando esse impulso até
#   velocity_y virar positivo e o cubo começar a cair.

import os
import pygame
from config import GRAVITY, GROUND_Y

# Tamanho do cubo em pixels (largura × altura).
PLAYER_SIZE = 60

# Força do impulso de pulo. Valor negativo porque "cima" é Y decrescente.
# Quanto mais negativo, mais alto o pulo.
JUMP_IMPULSE = -15

# Velocidade de rotação enquanto o cubo está no ar (graus por frame).
ROTATION_SPEED = 6


class Player:
    def __init__(self):
        # --- Posição e física ---
        # Posicionamos o cubo apoiado no chão: o bottom do rect deve ser GROUND_Y.
        start_x = 150
        self.rect = pygame.Rect(
            start_x,
            GROUND_Y - PLAYER_SIZE,  # topo do cubo = chão − altura
            PLAYER_SIZE,
            PLAYER_SIZE,
        )

        # Velocidade vertical. Começa em 0 (cubo parado).
        self.velocity_y: float = 0.0

        # True enquanto o cubo está tocando o chão — impede double-jump.
        self.on_ground: bool = True

        # --- Rotação visual ---
        # Ângulo atual de rotação em graus. Afeta apenas o desenho.
        self._angle: float = 0.0

        # --- Sprite ---
        # Tentamos carregar o arquivo de imagem. Se não existir, usamos um
        # fallback colorido para não quebrar o jogo durante o desenvolvimento.
        sprite_path = os.path.join("assets", "sprites", "player.jpg")
        self._sprite_original: pygame.Surface | None = None

        if os.path.isfile(sprite_path):
            try:
                # convert_alpha() otimiza a surface para desenhar com transparência.
                self._sprite_original = pygame.image.load(sprite_path).convert_alpha()
                # Escala o sprite para o tamanho do cubo, caso seja diferente.
                self._sprite_original = pygame.transform.scale(
                    self._sprite_original, (PLAYER_SIZE, PLAYER_SIZE)
                )
            except pygame.error:
                # pygame.error é lançado se o arquivo existir mas não for uma imagem válida.
                self._sprite_original = None

        # Cria a surface de fallback (retângulo colorido) uma única vez.
        if self._sprite_original is None:
            self._sprite_original = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
            # Azul-roxo, seguindo a estética da Fase 1 descrita no DESIGN.md.
            self._sprite_original.fill((100, 80, 220))
            # Borda mais clara para dar profundidade ao cubo.
            pygame.draw.rect(
                self._sprite_original,
                (160, 140, 255),
                self._sprite_original.get_rect(),
                width=3,
            )

    # ------------------------------------------------------------------
    # UPDATE — chamado todo frame com o delta time em segundos
    # ------------------------------------------------------------------
    def update(self, dt: float):
        # GRAVIDADE: acumulamos GRAVITY à velocidade vertical todo frame.
        # Isso faz o cubo acelerar pra baixo continuamente (como na física real).
        # Nota: usamos GRAVITY diretamente (pixels/frame), não escalado por dt,
        # para que o "feel" do pulo seja consistente independente de pequenas
        # variações de framerate — common em jogos de plataforma arcade.
        self.velocity_y += GRAVITY

        # Aplica a velocidade à posição vertical do rect.
        self.rect.y += int(self.velocity_y)

        # --- Detecção de colisão com o chão ---
        if self.rect.bottom >= GROUND_Y:
            # Cubo ultrapassou o chão: reposiciona exatamente sobre ele.
            self.rect.bottom = GROUND_Y
            self.velocity_y = 0.0
            self.on_ground = True

            # ROTAÇÃO — ao pousar, trava no múltiplo de 90° mais próximo.
            # Isso dá a ilusão de que o cubo "encaixa" na grade do chão.
            self._angle = round(self._angle / 90) * 90
        else:
            self.on_ground = False
            # ROTAÇÃO — acumula graus enquanto está no ar.
            self._angle += ROTATION_SPEED

    # ------------------------------------------------------------------
    # JUMP — chamado pelo input handler quando o jogador pressiona Espaço
    # ------------------------------------------------------------------
    def jump(self) -> bool:
        """Pula se estiver no chão. Retorna True se o pulo foi executado."""
        if self.on_ground:
            self.velocity_y = JUMP_IMPULSE
            self.on_ground = False
            return True
        return False

    # ------------------------------------------------------------------
    # DRAW — renderiza o cubo (rotacionado) na tela
    # ------------------------------------------------------------------
    def draw(self, screen: pygame.Surface):
        # pygame.transform.rotate() cria uma NOVA surface rotacionada.
        # O tamanho dela muda (bounding box cresce nas diagonais), por isso
        # precisamos recalcular onde centralizá-la para não "escorregar".
        rotated = pygame.transform.rotate(self._sprite_original, -self._angle)
        # Mantemos o centro visual no mesmo ponto que o rect de colisão.
        draw_rect = rotated.get_rect(center=self.rect.center)
        screen.blit(rotated, draw_rect)
