
Este é o Documento de Design Técnico e Criativo do seu jogo. Imagine que este é o roteiro que você vai seguir para não se perder durante a programação. Vamos detalhar cada engrenagem desse projeto para que ele não seja apenas um "clone", mas um jogo com personalidade.

🏗️ 1. A Estrutura Central (O "Motor")
O jogo funcionará sob um sistema de Scroller Lateral Infinito, onde o jogador parece correr, mas o mundo é que se move.
Taxa de Quadros (FPS): Cravado em 60 FPS para garantir que os pulos sejam precisos.
Sistema de Coordenadas: O chão será uma linha constante no eixo $Y$. O jogador terá uma variável de gravidade que o puxa para baixo e uma de impulso que o empurra para cima.
Sincronia de Áudio: O mapa não é aleatório. Cada espinho será posicionado de acordo com os milissegundos da música. Se a batida cai no segundo 1.5, um espinho estará na posição de colisão exatamente nesse tempo.

🎨 2. Interface e Experiência do Usuário (UI/UX)
A Tela Inicial (O Hub)
Não é apenas um menu estático. O fundo terá formas geométricas passando lentamente em baixa opacidade.
Seleção de Fases: Três grandes botões interativos. Ao passar o mouse, eles brilham em neon.
O Seletor de Dificuldade: Após escolher a fase, surge um pop-up elegante com as opções:
Fácil (Verde): Velocidade de 400 pixels/segundo. O jogador tem "hitboxes" (caixas de colisão) menores que o desenho, sendo mais difícil morrer "sem querer".
Médio (Amarelo): Velocidade de 600 pixels/segundo. Ritmo padrão da música original.
Difícil (Vermelho): Velocidade de 900 pixels/segundo. A tela dá um leve "zoom in", diminuindo o tempo de reação do jogador.

🕹️ 3. As Três Fases: A Jornada do Jogador
Fase 1: O Batismo de Fogo
Mecânica: Apenas o Cubo. O foco é o salto único.
Estética: Tons de azul e roxo.
Desafio: Introdução de plataformas flutuantes. O jogador precisa pular de uma plataforma para outra sem cair nos espinhos entre elas.
O Final: A música desacelera, e o jogador toca um pilar de luz para vencer.
Fase 2: A Ascensão Tecnológica
Mecânica: Cubo + Nave.
A Transição: Aos 50% da fase, o jogador atravessa um portal em forma de anel. O cubo ganha "asas" (muda o sprite) e a física muda instantaneamente.
Física da Nave: Se você segurar a tecla Espaço, o código aplica uma força negativa no eixo $Y$:
$$v_y = v_y - impulso\_nave$$
.
O Desafio: Um corredor estreito com serras em cima e embaixo. O jogador deve "vibrar" no meio do caminho para sobreviver.
Fase 3: O Paradoxo da Gravidade
Mecânica: Gravidade Invertida.
A Mudança: Aqui, em vez de voar, o jogador toca em portais amarelos que invertem o mundo.
Lógica Matemática: A gravidade, que era $g = 0.8$, passa a ser $g = -0.8$. O jogador agora "cai" para o teto.
O Desafio: O "zigue-zague". Portais de inversão colocados um logo após o outro, forçando o jogador a trocar de superfície em milissegundos.

💥 4. Sistema de Falha e Sucesso
O Game Over (A Morte)
Quando o retângulo do player toca no triângulo do espinho:
Congelamento: O jogo para por 0.5 segundos para o jogador processar o erro.
Partículas: O cubo explode em pequenos quadrados que caem pela tela.
Menu de Morte: Aparece um painel central:
"Tentativa #N" em destaque.
Barra de Progresso: "Você completou 65% da fase".
Botões: "Reiniciar" (foca no fluxo rápido) e "Menu Principal".
A Vitória (O Alívio)
Ao cruzar a linha de chegada:
A tela fica branca por um instante.
Uma mensagem de "LEVEL COMPLETE" surge com uma animação de escala.
O número de tentativas totais é exibido como um troféu: "Venceu em 45 tentativas".

🛠️ 5. Resumo Técnico para o Código
Componente
Função no Pygame
Player.rect
Controla a posição e colisões.
Camera_X
Variável que aumenta todo frame para mover o cenário.
Listas de Obstáculos
Uma lista de objetos que são deletados quando saem da tela à esquerda para economizar memória.
pygame.mixer
Controla a trilha sonora e o efeito de "clique" ao pular.


