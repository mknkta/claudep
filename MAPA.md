# MAPA DO PROJETO — onde cada coisa está

## Estrutura de arquivos (tudo na raiz)

```
claudep/
├── main.py          ← loop principal do jogo (janela, FPS, troca de cenas)
├── config.py        ← constantes globais (tamanho da tela, gravidade, cores, velocidades)
├── player.py        ← cubo do jogador (tamanho, cor, pulo, rotação)
├── obstacles.py     ← espinhos e plataformas (tamanhos, cores, hitbox)
├── level1.py        ← posição de cada espinho e plataforma da Fase 1
├── loader.py        ← lê o level1.py e converte tempos em posições X
├── audio.py         ← música e efeitos sonoros
├── saves.py         ← contador de tentativas (salvo em save.json)
├── debug.py         ← overlay F3 (FPS, hitboxes, tempo)
├── gameplay.py      ← cena de jogo (física, colisão, morte, vitória)
├── menu.py          ← tela inicial (formas flutuantes, botões de fase)
├── difficulty.py    ← painel Fácil / Médio / Difícil
├── gameover.py      ← tela de game over (partículas, painel, botões)
├── victory.py       ← tela de vitória (flash branco, animação)
└── assets/
    ├── player.jpg   ← imagem do cubo (opcional — usa cor se não existir)
    ├── spike.jpg    ← imagem do espinho (opcional — usa triângulo se não existir)
    ├── music/
    │   └── level1.ogg  ← música da fase 1
    └── sfx/
        └── jump.wav    ← som do pulo (opcional — silencioso se não existir)
```

---

## Para mexer em cada elemento

---

### Cubo do jogador
**Arquivo:** `player.py`

| O que mudar | Onde |
|---|---|
| Tamanho do cubo | `SIZE = 60` |
| Força do pulo | `JUMP_IMPULSE = -15` — mais negativo = pulo maior |
| Velocidade de rotação no ar | `ROT_SPEED = 6` |
| Cor do cubo (sem imagem) | `.fill((100, 80, 220))` no método `_load()` |
| Cor da borda do cubo | `.draw.rect(..., (160, 140, 255), ...)` no método `_load()` |
| Imagem do cubo | coloque `assets/player.jpg` — o código carrega automaticamente |

---

### Espinhos
**Arquivo:** `obstacles.py`

| O que mudar | Onde |
|---|---|
| Tamanho small (largura, altura) | `"small": (22, 18)` no dicionário `SIZES` |
| Tamanho medium | `"medium": (34, 28)` |
| Tamanho large | `"large": (46, 38)` |
| Cor laranja do espinho | `COLOR = (255, 80, 30)` na classe `Spike` |
| Cor da borda | `COLOR_EDGE = (255, 180, 80)` |
| Tamanho da hitbox | `int(w * 0.15)` e `int(h * 0.20)` — quanto maior o valor, menor a hitbox |
| Imagem do espinho | coloque `assets/spike.jpg` — o código carrega automaticamente |

---

### Plataformas
**Arquivo:** `obstacles.py`

| O que mudar | Onde |
|---|---|
| Espessura da plataforma | `PLATFORM_H = 20` (no topo do arquivo) |
| Cor verde | `COLOR = (60, 200, 120)` na classe `Platform` |
| Cor da borda | `COLOR_EDGE = (120, 255, 180)` |
| Largura padrão (quando não definida no level) | `width: int = 200` no `__init__` da `Platform` |

---

### Fundo e grade
**Arquivo:** `gameplay.py`

| O que mudar | Onde |
|---|---|
| Cor do fundo | `COLORS["background"]` em `config.py` → `(30, 30, 40)` |
| Cor das linhas da grade | `COLORS["grid"]` em `config.py` → `(50, 50, 60)` |
| Espaçamento das linhas | `GRID = 100` no topo de `gameplay.py` |
| Cor e espessura do chão | `COLORS["ground"]` em `config.py` e `width=4` no método `draw()` |
| Altura do chão | `GROUND_Y = 600` em `config.py` |

---

### Barra de progresso (topo da tela)
**Arquivo:** `gameplay.py`

| O que mudar | Onde |
|---|---|
| Altura da barra | `BAR_H = 8` |
| Cor da barra preenchida | `BAR_C = (140, 80, 220)` |
| Cor do fundo da barra | `BAR_B = (40, 30, 60)` |

---

### Física global
**Arquivo:** `config.py`

| O que mudar | Onde |
|---|---|
| Gravidade | `GRAVITY = 0.8` pixels/frame² — maior = cai mais rápido |
| Altura do chão | `GROUND_Y = 600` |
| FPS | `FPS = 60` |
| Tamanho da janela | `SCREEN_WIDTH = 1280`, `SCREEN_HEIGHT = 720` |
| Cores do fundo, grade e chão | dicionário `COLORS` |
| Velocidades das dificuldades | `SPEED_EASY = 400`, `SPEED_MEDIUM = 600`, `SPEED_HARD = 900` |

---

### Partículas de morte
**Arquivo:** `gameplay.py` → classe `Particle`

| O que mudar | Onde |
|---|---|
| Quantidade de partículas | `range(20)` em `_die()` |
| Velocidade aleatória | `random.uniform(-300, 300)` para `vx` e `vy` |
| Tamanho | `random.randint(5, 14)` |
| Tempo de vida | `random.uniform(0.6, 1.0)` segundos |
| Gravidade das partículas | `self.vy += 600 * dt` |
| Cores | lista `COLORS` dentro da classe `Particle` |
| Tempo de congelamento antes do game over | `FREEZE_TIME = 0.5` segundos |

---

### Mapa (posição dos obstáculos)
**Arquivo:** `level1.py`

Cada linha é um obstáculo. Exemplos:
```python
{"time": 2.0, "type": "spike", "size": "medium"}
{"time": 5.5, "type": "platform", "y": 520, "width": 160}
```

| Campo | O que faz |
|---|---|
| `"time"` | segundo da música em que o obstáculo entra pela direita |
| `"type"` | `"spike"` ou `"platform"` |
| `"size"` | tamanho do espinho: `"small"`, `"medium"` ou `"large"` |
| `"y"` | altura da plataforma — menor valor = mais alto na tela |
| `"width"` | largura da plataforma em pixels |
| `DURATION` | duração total da fase em segundos (variável no topo) |
| `MUSIC` | caminho do arquivo de música |

**Regra importante:** máximo 3 espinhos juntos (espaçados 0.12s), gap mínimo de 0.7s entre grupos. Isso garante que tudo é possível de pular no Fácil.

---

### Tela inicial (menu)
**Arquivo:** `menu.py`

| O que mudar | Onde |
|---|---|
| Cor do fundo | `BG = (20, 18, 32)` |
| Cor do título | `TITLE = (220, 200, 255)` |
| Texto do título | `"GEOMETRY DASH"` no método `draw()` |
| Quantidade de formas flutuantes | `range(8)` no `__init__` |
| Cores neon dos botões por fase | `PHASE_COLORS = {1: ciano, 2: magenta, 3: verde}` |
| Tamanho dos botões | `bw, bh = 260, 90` |

---

### Seleção de dificuldade
**Arquivo:** `difficulty.py`

| O que mudar | Onde |
|---|---|
| Velocidade de cada dificuldade | `"speed": 400 / 600 / 900` no dicionário `DIFFS` |
| Hitbox no Fácil | `"hscale": 0.7` — 0.7 = 70% do tamanho visual |
| Zoom no Difícil | `"zoom": 1.1` — 1.1 = 10% de zoom in |
| Cores dos botões | `"color"` em cada entrada de `DIFFS` |

---

### Tela de game over
**Arquivo:** `gameover.py`

| O que mudar | Onde |
|---|---|
| Cor do painel | `(20, 16, 35)` fundo e `(120, 80, 180)` borda |
| Botão "Reiniciar" | cor `(80, 200, 120)` |
| Botão "Menu Principal" | cor `(100, 120, 220)` |
| Escurecimento do fundo | `(0, 0, 0, 170)` — último número é a opacidade (0–255) |

---

### Tela de vitória
**Arquivo:** `victory.py`

| O que mudar | Onde |
|---|---|
| Duração do flash branco | `FLASH = 0.3` segundos |
| Duração da animação do texto | `ANIM = 0.8` segundos |
| Cor do "LEVEL COMPLETE" | `(255, 230, 80)` |
| Escala máxima do texto | `1.2` no cálculo de `scale` |

---

### Música e sons
**Arquivo:** `audio.py`

| O que mudar | Onde |
|---|---|
| Volume da música | `set_volume(0.7)` em `play_music()` — 0.0 a 1.0 |
| Arquivo de música | definido em `level1.py` → `MUSIC = "assets/music/level1.ogg"` |
| Som de pulo | `SFX = "assets/sfx/jump.wav"` em `gameplay.py` |

---

### Contador de tentativas
**Arquivo:** `saves.py`

Salvo automaticamente em `save.json` na raiz. Para zerar as tentativas, delete o arquivo `save.json`.
