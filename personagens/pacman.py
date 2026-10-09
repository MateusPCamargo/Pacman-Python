import pygame

pygame.init()

class Pacman:
    def __init__(self, x, y, mapa, pontuacao):
        self.x = x
        self.y = y
        self.mapa = mapa

        self.pontuacao = 0

        self.largura = 15
        self.altura = 15

        self.velocidade = 3

        self.direcao = "cima"
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

        if teclas[pygame.K_RIGHT]:
            self.direcao = "direita"

        elif teclas[pygame.K_LEFT]:
            self.direcao = "esquerda"

        elif teclas[pygame.K_UP]:
            self.direcao = "cima"

        elif teclas[pygame.K_DOWN]:
            self.direcao = "baixo"

        if self.direcao == "direita":
            novo_x = self.x + self.velocidade
            if not self.colisao(novo_x, self.y):
                self.x = novo_x

        elif self.direcao == "esquerda":
            novo_x = self.x - self.velocidade
            if not self.colisao(novo_x, self.y):
                self.x = novo_x

        elif self.direcao == "cima":
            novo_y = self.y - self.velocidade
            if not self.colisao(self.x, novo_y):
                self.y = novo_y

        elif self.direcao == "baixo":
            novo_y = self.y + self.velocidade
            if not self.colisao(self.x, novo_y):
                self.y = novo_y

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


    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))


    def colisao(self, novo_x, novo_y):
        visao = [
            (novo_x, novo_y),
            (novo_x + self.largura - 1, novo_y),
            (novo_x, novo_y + self.altura - 1),
            (novo_x + self.largura - 1, novo_y + self.altura - 1)
        ]

        for x, y in visao:
            if self.mapa.verificar_parede(x, y):
                return True

        return False

    def comer_ponto(self):
        coluna = int((self.x + self.largura // 2) // self.mapa.tamanho_bloco)
        linha = int((self.y + self.altura // 2) // self.mapa.tamanho_bloco)

        if self.mapa.mapa[linha][coluna] == "3":
            self.pontuacao += 10
            self.mapa.mapa[linha] = (
                self.mapa.mapa[linha][:coluna]
                + "0"
                + self.mapa.mapa[linha][coluna + 1:]
            )
            