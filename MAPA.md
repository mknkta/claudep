# MAPA DO PROJETO — onde cada coisa está

## Arquivos e o que cada um controla

```
claudep/
├── main.py                          ← ponto de entrada; cria a janela, o clock e o loop principal
├── config.py                        ← constantes globais (tamanho da tela, FPS, cores, gravidade, velocidades)
├── DESIGN.md                        ← documento de design do jogo (referência criativa)
├── save.json                        ← salva o contador de tentativas entre sessões
├── levels/
│   └── level1.json                  ← posição/tempo de cada espinho e plataforma da Fase 1
└── src/
    ├── entities/
    │   ├── player.py                ← cubo do jogador (tamanho, cor, física de pulo, rotação)
    │   └── obstacles.py             ← espinhos (3 tamanhos) e plataformas
    ├── scenes/
    │   ├── scene.py                 ← classe base abstrata de cena
    │   ├── scene_manager.py         ← troca de cenas (menu → jogo → game over etc.)
    │   ├── main_menu_scene.py       ← tela inicial (formas flutuantes, botões de fase)
    │   ├── difficulty_select_scene.py ← painel Fácil/Médio/Difícil
    │   ├── gameplay_scene.py        ← cena principal: spawna obstáculos, física, morte, vitória
    │   ├── game_over_scene.py       ← tela de game over (painel com tentativas e progresso)
    │   └── victory_scene.py         ← tela de vitória (flash branco + "LEVEL COMPLETE")
    └── systems/
        ├── audio_manager.py         ← carrega/toca música e efeitos sonoros
        ├── debug_overlay.py         ← overlay F3 (FPS, hitboxes, tempo da música)
        ├── level_loader.py          ← lê level1.json e converte tempos → posições X
        └── save_manager.py          ← lê e grava save.json (tentativas)
```

---

## Para mexer em cada elemento visual

### Cubo do jogador
**Arquivo:** `src/entities/player.py`

| O que mudar | Onde |
|---|---|
| Tamanho do cubo | `PLAYER_SIZE = 60` (linha 27) |
| Cor do cubo (fallback sem sprite) | `.fill((100, 80, 220))` (linha 76) |
| Cor da borda do cubo | `.fill((160, 140, 255))` (linha 80) |
| Força do pulo | `JUMP_IMPULSE = -15` (linha 29) — mais negativo = pulo maior |
| Velocidade de rotação no ar | `ROTATION_SPEED = 6` (linha 32) |
| Sprite externo | coloque uma imagem em `assets/sprites/player.png` |

---

### Espinhos
**Arquivo:** `src/entities/obstacles.py`

| O que mudar | Onde |
|---|---|
| Tamanhos disponíveis (small/medium/large) | dicionário `_SPIKE_SIZES` (linha 20) — `(largura, altura)` |
| Cor laranja do espinho | `_COLOR = (255, 80, 30)` (linha 40) |
| Cor da borda do espinho | `_COLOR_EDGE = (255, 180, 80)` (linha 41) |
| Tamanho da hitbox (quanto menor o inset, maior a hitbox) | `inset_x = int(w * 0.15)` e `inset_y = int(h * 0.20)` (linhas 51–52) |
| Sprite externo | coloque uma imagem em `assets/sprites/spike.png` |

---

### Plataformas
**Arquivo:** `src/entities/obstacles.py`

| O que mudar | Onde |
|---|---|
| Espessura da plataforma | `PLATFORM_HEIGHT = 20` (linha 16) |
| Cor verde da plataforma | `_COLOR = (60, 200, 120)` (linha 91) |
| Cor da borda verde clara | `_COLOR_EDGE = (120, 255, 180)` (linha 92) |
| Largura padrão (se não definida no JSON) | `width: int = 200` (linha 95) |

---

### Fundo e grade
**Arquivo:** `src/scenes/gameplay_scene.py`

| O que mudar | Onde |
|---|---|
| Espaçamento das linhas da grade | `GRID_SPACING = 100` (linha 14) |
| Cor do fundo | `COLORS["background"]` em `config.py` → `(30, 30, 40)` |
| Cor das linhas da grade | `COLORS["grid"]` em `config.py` → `(50, 50, 60)` |
| Cor/espessura do chão | `COLORS["ground"]` e `width=4` no `draw()` |
| Altura do chão (onde o cubo pousa) | `GROUND_Y = 600` em `config.py` |

---

### Barra de progresso (topo da tela)
**Arquivo:** `src/scenes/gameplay_scene.py` → método `_draw_progress_bar()`

| O que mudar | Onde |
|---|---|
| Altura da barra | `_BAR_H = 8` (linha 18) |
| Cor da barra preenchida | `_BAR_COL = (140, 80, 220)` (linha 19) |
| Cor do fundo da barra | `_BAR_BG = (40, 30, 60)` (linha 20) |

---

### Partículas de morte
**Arquivo:** `src/scenes/gameplay_scene.py` → classe `_Particle`

| O que mudar | Onde |
|---|---|
| Quantidade de partículas | `[_Particle(cx, cy) for _ in range(20)]` em `_trigger_death()` |
| Velocidade aleatória | `random.uniform(-300, 300)` para `vx` e `vy` |
| Tamanho das partículas | `random.randint(5, 14)` |
| Tempo de vida | `random.uniform(0.6, 1.0)` em segundos |
| Gravidade das partículas | `self.vy += 600 * dt` |
| Cores das partículas | lista `random.choice([...])` no `__init__` |

---

### Tela inicial (menu principal)
**Arquivo:** `src/scenes/main_menu_scene.py`

| O que mudar | Onde |
|---|---|
| Cor do fundo do menu | `BG_COLOR = (20, 18, 32)` |
| Cor do título | `TITLE_COLOR = (220, 200, 255)` |
| Texto do título | `"GEOMETRY DASH"` no `draw()` |
| Tamanho da fonte do título | `pygame.font.SysFont("consolas", 64, bold=True)` |
| Formas geométricas flutuantes | classe `_FloatingShape` — velocidade (`vx`, `vy`), tamanho, opacidade (`alpha=40`) |
| Cor neon de cada botão de fase | `PHASE_COLORS = {1: ciano, 2: magenta, 3: verde}` |
| Tamanho dos botões | `bw, bh = 260, 90` |

---

### Seleção de dificuldade
**Arquivo:** `src/scenes/difficulty_select_scene.py`

| O que mudar | Onde |
|---|---|
| Velocidades | `"speed": 400 / 600 / 900` no dicionário `DIFFICULTIES` |
| Escala da hitbox no Fácil | `"hitbox": 0.7` |
| Zoom no Difícil | `"zoom": 1.1` |
| Cores dos botões | `"color"` em cada entrada de `DIFFICULTIES` |

---

### Tela de game over
**Arquivo:** `src/scenes/game_over_scene.py`

| O que mudar | Onde |
|---|---|
| Cor do painel | `(20, 16, 35)` e borda `(120, 80, 180)` |
| Cor da barra de progresso no painel | `(140, 80, 220)` |
| Botão "Reiniciar" | cor `(80, 200, 120)` |
| Botão "Menu Principal" | cor `(100, 120, 220)` |

---

### Tela de vitória
**Arquivo:** `src/scenes/victory_scene.py`

| O que mudar | Onde |
|---|---|
| Duração do flash branco | `FLASH_DURATION = 0.3` segundos |
| Duração da animação do texto | `ANIM_DURATION = 0.8` segundos |
| Cor do texto "LEVEL COMPLETE" | `(255, 230, 80)` |
| Escala máxima do texto | `1.2` (cresce até 1.2× e volta para 1.0×) |

---

### Posicionamento dos obstáculos na fase
**Arquivo:** `levels/level1.json`

Cada linha é um obstáculo:
```json
{"time": 2.0, "type": "spike", "size": "medium"}
{"time": 5.5, "type": "platform", "y": 520, "width": 160}
```

| Campo | O que faz |
|---|---|
| `"time"` | segundo da música em que o obstáculo entra na tela |
| `"type"` | `"spike"` ou `"platform"` |
| `"size"` | tamanho do espinho: `"small"`, `"medium"` ou `"large"` |
| `"y"` | altura da plataforma (só para platforms — menor valor = mais alto na tela) |
| `"width"` | largura da plataforma em pixels |
| `"duration"` | duração total da fase em segundos (campo no topo do JSON) |

---

### Física global
**Arquivo:** `config.py`

| O que mudar | Onde |
|---|---|
| Gravidade | `GRAVITY = 0.8` pixels/frame² |
| Altura do chão | `GROUND_Y = 600` |
| FPS | `FPS = 60` |
| Tamanho da janela | `SCREEN_WIDTH = 1280`, `SCREEN_HEIGHT = 720` |

---

### Música e sons
**Arquivo:** `src/systems/audio_manager.py`

| Arquivo de áudio | Caminho |
|---|---|
| Música da Fase 1 | `assets/music/level1.ogg` (definido em `levels/level1.json`) |
| Som de pulo | `assets/sfx/jump.wav` (silencioso se não existir) |

Volume da música: `set_volume(0.7)` em `play_music()` — valor entre 0.0 e 1.0.
