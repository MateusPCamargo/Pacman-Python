import pygame
import random
from collections import deque

pygame.init()

DIRECOES = {              
    "cima":     (0, -1),
    "esquerda": (-1, 0),
    "baixo":    (0, 1),
    "direita":  (1, 0),
}

OPOSTA = {"cima": "baixo", "baixo": "cima", "esquerda": "direita", "direita": "esquerda"}

class Fantasma:
    def __init__(self, x, y, mapa):
        self.largura = 20
        self.altura = 20

        self.x = x
        self.y = y
        self.mapa = mapa
        self.direcao = "direita"
        
        self.velocidade = 2

        self.sprite = pygame.image.load("assets/fantasmas/blinky.png")

        self.imagem = pygame.transform.scale(self.sprite, (self.largura, self.altura))

        self.tamanho_bloco = 24
        self.deslocamento = (self.tamanho_bloco - self.largura) // 2

    def desenhar_fantasma(self, tela):
        tela.blit(self.imagem, (self.x + self.deslocamento, self.y + self.deslocamento))


    def colisao(self, x, y):
        t = self.tamanho_bloco - 1   
        pontos = ((x, y), (x + t, y), (x, y + t), (x + t, y + t))
        return any(self.mapa.verificar_parede(px, py) for px, py in pontos)

    

    def livre(self, direcao, passos=None):
        dx, dy = DIRECOES[direcao]
        d = self.velocidade if passos is None else passos
        return not self.colisao(self.x + dx * d, self.y + dy * d)

    def alinhado(self):
        return self.x % self.tamanho_bloco == 0 and self.y % self.tamanho_bloco == 0

    def escolher_direcao(self, alvo=None):
        opcoes = [d for d in DIRECOES
                if d != OPOSTA[self.direcao] and self.livre(d, self.tamanho_bloco)]

        if not opcoes:                       # beco sem saída
            return OPOSTA[self.direcao]

        if alvo is None:                     # aleatório (modo assustado)
            return random.choice(opcoes)

        # tile onde está o alvo (usa o centro, para funcionar com o Pac-Man entre tiles)
        meta = (int((alvo[0] + self.tamanho_bloco // 2) // self.tamanho_bloco),
                int((alvo[1] + self.tamanho_bloco // 2) // self.tamanho_bloco))
        dist = self.mapa_distancias(meta)

        col = int(self.x // self.tamanho_bloco)
        lin = int(self.y // self.tamanho_bloco)

        def custo(d):
            dx, dy = DIRECOES[d]
            return dist.get((col + dx, lin + dy), float("inf"))

        melhor = min(opcoes, key=custo)
        if custo(melhor) == float("inf"):    # alvo inalcançável: anda aleatório
            return random.choice(opcoes)
        return melhor   

    def atualizar(self, dt, alvo=None):
        if self.alinhado():
            self.direcao = self.escolher_direcao(alvo)

        if self.livre(self.direcao):
            dx, dy = DIRECOES[self.direcao]
            self.x += dx * self.velocidade
            self.y += dy * self.velocidade

    def mapa_distancias(self, meta):
        dist = {meta: 0}
        fila = deque([meta])
        while fila:
            col, lin = fila.popleft()
            for dx, dy in DIRECOES.values():
                viz = (col + dx, lin + dy)
                if viz in dist:
                    continue
                centro_x = viz[0] * self.tamanho_bloco + self.tamanho_bloco // 2
                centro_y = viz[1] * self.tamanho_bloco + self.tamanho_bloco // 2
                if self.mapa.verificar_parede(centro_x, centro_y):
                    continue
                dist[viz] = dist[(col, lin)] + 1
                fila.append(viz)
        return dist
        

