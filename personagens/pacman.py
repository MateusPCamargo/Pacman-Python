import pygame

pygame.init()

DIRECOES = {
    "cima":     (0, -1),
    "esquerda": (-1, 0),
    "baixo":    (0, 1),
    "direita":  (1, 0),
}

class Pacman:
    def __init__(self, x, y, mapa, pontuacao):
        self.x = x
        self.y = y
        self.x_inicial = x
        self.y_inicial = y
        
        self.mapa = mapa
        self.tamanho_bloco = mapa.tamanho_bloco
        self.deslocamento = (self.tamanho_bloco - 20) // 2

        self.pontuacao = 0
        self.pegou_poder = False

        self.largura = 20
        self.altura = 20

        self.velocidade = 3
        self.direcao = "cima"

        self.direcao_inicial = self.direcao
        self.direcao_desejada = self.direcao
        self.tempo_buffer = 0     
        self.buffer_ms = 200      
        self.tolerancia = 6

        self.animacao = {
            
            "direita": [
            pygame.image.load("assets/pacman/direita/1.png").convert_alpha(),
            pygame.image.load("assets/pacman/direita/2.png").convert_alpha(),
            pygame.image.load("assets/pacman/direita/3.png").convert_alpha()
            ],

            "esquerda": [
            pygame.image.load("assets/pacman/esquerda/1.png").convert_alpha(),
            pygame.image.load("assets/pacman/esquerda/2.png").convert_alpha(),
            pygame.image.load("assets/pacman/esquerda/3.png").convert_alpha()
            ],

            "cima": [
            pygame.image.load("assets/pacman/cima/1.png").convert_alpha(),
            pygame.image.load("assets/pacman/cima/2.png").convert_alpha(),
            pygame.image.load("assets/pacman/cima/3.png").convert_alpha()
            ],

            "baixo": [
            pygame.image.load("assets/pacman/baixo/1.png").convert_alpha(),
            pygame.image.load("assets/pacman/baixo/2.png").convert_alpha(),
            pygame.image.load("assets/pacman/baixo/3.png").convert_alpha()
            ]

        }

        self.frame = 0
        self.tempo_animacao = 0


        self.imagem = pygame.transform.scale(
            self.animacao[self.direcao][self.frame],
            (self.largura, self.altura)
        )


    def atualizar(self, dt):
        teclas = pygame.key.get_pressed()

        pedida = None
        if teclas[pygame.K_RIGHT]:
            pedida = "direita"
        elif teclas[pygame.K_LEFT]:
            pedida = "esquerda"
        elif teclas[pygame.K_UP]:
            pedida = "cima"
        elif teclas[pygame.K_DOWN]:
            pedida = "baixo"

        if pedida:
            self.direcao_desejada = pedida
            self.tempo_buffer = self.buffer_ms

        if self.tempo_buffer > 0:
            if self.tentar_virar():
                self.tempo_buffer = 0
            else:
                self.tempo_buffer -= dt

        if self.livre(self.direcao):
            dx, dy = DIRECOES[self.direcao]
            self.x += dx * self.velocidade
            self.y += dy * self.velocidade

        self.tempo_animacao += dt

        if self.tempo_animacao >= 150:
            self.tempo_animacao = 0
            self.frame += 1

            if self.frame >= len(self.animacao[self.direcao]):
                self.frame = 0

        self.imagem = pygame.transform.scale(
            self.animacao[self.direcao][self.frame],
            (self.largura, self.altura)

        )

        self.comer_ponto()

    def livre(self, direcao, x=None, y=None):
        x = self.x if x is None else x
        y = self.y if y is None else y
        dx, dy = DIRECOES[direcao]
        return not self.colisao(x + dx * self.velocidade, y + dy * self.velocidade)

    def tentar_virar(self):
        nova = self.direcao_desejada
        if nova == self.direcao:
            return True

        T = self.tamanho_bloco
        horizontal_atual = self.direcao in ("direita", "esquerda")
        horizontal_nova = nova in ("direita", "esquerda")

        if horizontal_atual == horizontal_nova:          # meia-volta
            if self.livre(nova):
                self.direcao = nova
                return True
            return False

        if horizontal_atual:                             # vai virar para cima/baixo
            alvo_x = round(self.x / T) * T
            if abs(self.x - alvo_x) <= self.tolerancia and self.livre(nova, alvo_x, self.y):
                self.x = alvo_x
                self.direcao = nova
                return True
        else:                                            # vai virar para esquerda/direita
            alvo_y = round(self.y / T) * T
            if abs(self.y - alvo_y) <= self.tolerancia and self.livre(nova, self.x, alvo_y):
                self.y = alvo_y
                self.direcao = nova
                return True
        return False

    def colisao(self, novo_x, novo_y):
        t = self.tamanho_bloco - 1
        pontos = ((novo_x, novo_y), (novo_x + t, novo_y),
                  (novo_x, novo_y + t), (novo_x + t, novo_y + t))
        return any(self.mapa.verificar_parede(px, py) for px, py in pontos)

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x + self.deslocamento, self.y + self.deslocamento))

    def resetar(self):
        self.x = self.x_inicial
        self.y = self.y_inicial
        self.direcao = self.direcao_inicial
        self.direcao_desejada = self.direcao_inicial
        self.tempo_buffer = 0
        self.frame = 0
        self.tempo_animacao = 0

    def comer_ponto(self):
        coluna = int((self.x + self.tamanho_bloco // 2) // self.tamanho_bloco)
        linha = int((self.y + self.tamanho_bloco // 2) // self.tamanho_bloco)

        celula = self.mapa.mapa[linha][coluna]

        if celula == "3" or celula == "4":
            if celula == "3":
                self.pontuacao += 10
            else:
                self.pontuacao += 50
                self.pegou_poder = True      # o main lê isso e assusta os fantasmas

            self.mapa.mapa[linha] = (
                self.mapa.mapa[linha][:coluna]
                + "0"
                + self.mapa.mapa[linha][coluna + 1:]
            )
            