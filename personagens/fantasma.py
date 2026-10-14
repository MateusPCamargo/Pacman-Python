import math
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

SPRITE = "assets/fantasmas/blinky.png"

class Fantasma:
    def __init__(self, x, y, mapa):
        self.largura = 20
        self.altura = 20

        self.x = x
        self.y = y
        self.x_inicial = x
        self.y_inicial = y

        self.mapa = mapa

        self.direcao = "direita"
        self.direcao_inicial = self.direcao
        
        self.velocidade = 2
        self.velocidade_normal = self.velocidade
        self.velocidade_assustado = 1          
        self.velocidade_desejada = self.velocidade
        self.assustado = False
        self.tempo_assustado = 0

        self.sprite = pygame.image.load(self.SPRITE)

        self.imagem = pygame.transform.scale(self.sprite, (self.largura, self.altura))
        self.imagem_normal = self.imagem
        self.imagem_assustada = self.criar_imagem_assustada()

        self.tamanho_bloco = 24
        self.deslocamento = (self.tamanho_bloco - self.largura) // 2

    def desenhar_fantasma(self, tela):
        imagem = self.imagem_normal
        if self.assustado:
            piscando = self.tempo_assustado < 2000 and int(self.tempo_assustado // 250) % 2 == 0
            if not piscando:
                imagem = self.imagem_assustada
        tela.blit(imagem, (self.x + self.deslocamento, self.y + self.deslocamento))


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

        if not opcoes:                      
            return OPOSTA[self.direcao]

        if alvo is None or self.assustado:                    
            return random.choice(opcoes)

        
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
        if self.assustado:
            self.tempo_assustado -= dt
            if self.tempo_assustado <= 0:
                self.normalizar()

        if self.alinhado():
            self.velocidade = self.velocidade_desejada   
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

    def tile_de(self, x, y):
        t = self.tamanho_bloco
        return (int((x + t // 2) // t), int((y + t // 2) // t))

    def tile_livre(self, col, lin):
        t = self.tamanho_bloco
        return not self.mapa.verificar_parede(col * t + t // 2, lin * t + t // 2)

    def ajustar_alvo(self, ponto, base):
        for passo in (1.0, 0.75, 0.5, 0.25, 0.0):
            col = round(base[0] + (ponto[0] - base[0]) * passo)
            lin = round(base[1] + (ponto[1] - base[1]) * passo)
            if self.tile_livre(col, lin):
                return (col, lin)
        return base

    def em_pixels(self, tile):
        t = self.tamanho_bloco
        return (tile[0] * t, tile[1] * t)

    def vetor_pacman(self, pacman):
        return DIRECOES.get(getattr(pacman, "direcao", None), (0, 0))

    def calcular_alvo(self, pacman, blinky=None):
        return (pacman.x, pacman.y)

    def colidiu_com(self, pacman):
        distancia = 12      
        return abs(self.x - pacman.x) < distancia and abs(self.y - pacman.y) < distancia

    def resetar(self):
        self.x = self.x_inicial
        self.y = self.y_inicial
        self.direcao = self.direcao_inicial
        self.normalizar()
        self.velocidade = self.velocidade_normal

    def assustar(self, duracao=6000):
        if not self.assustado:
            self.direcao = OPOSTA[self.direcao]      
        self.assustado = True
        self.tempo_assustado = duracao
        self.velocidade_desejada = self.velocidade_assustado

    def normalizar(self):
        self.assustado = False
        self.tempo_assustado = 0
        self.velocidade_desejada = self.velocidade_normal

    def criar_imagem_assustada(self):
        img = pygame.image.load("assets/fantasmas/assustado.png")
        return pygame.transform.scale(img, (self.largura, self.altura))

class Blinky(Fantasma):
    SPRITE = "assets/fantasmas/blinky.png"


class Pinky(Fantasma):
    SPRITE = "assets/fantasmas/pinky.png"

    def calcular_alvo(self, pacman, blinky=None):
        base = self.tile_de(pacman.x, pacman.y)
        dx, dy = self.vetor_pacman(pacman)
        ponto = (base[0] + dx * 4, base[1] + dy * 4)
        return self.em_pixels(self.ajustar_alvo(ponto, base))


class Inky(Fantasma):
    SPRITE = "assets/fantasmas/inky.png"

    def calcular_alvo(self, pacman, blinky=None):
        base = self.tile_de(pacman.x, pacman.y)
        dx, dy = self.vetor_pacman(pacman)
        meio = (base[0] + dx * 2, base[1] + dy * 2)
        if blinky is None:
            ponto = meio
        else:
            b = self.tile_de(blinky.x, blinky.y)
            ponto = (2 * meio[0] - b[0], 2 * meio[1] - b[1])
        return self.em_pixels(self.ajustar_alvo(ponto, base))


class Clyde(Fantasma):
    SPRITE = "assets/fantasmas/clyde.png"
    CANTO = None    # (coluna, linha) de um tile livre; None = achar automaticamente

    def __init__(self, x, y, mapa):
        super().__init__(x, y, mapa)
        self.canto = self.CANTO if self.CANTO is not None else self.achar_canto()

    def achar_canto(self):
        for lin in range(80, -1, -1):
            for col in range(0, 80):
                if self.tile_livre(col, lin):
                    return (col, lin)
        return (1, 1)

    def calcular_alvo(self, pacman, blinky=None):
        base = self.tile_de(pacman.x, pacman.y)
        meu = self.tile_de(self.x, self.y)
        if math.hypot(base[0] - meu[0], base[1] - meu[1]) > 8:
            return (pacman.x, pacman.y)
        return self.em_pixels(self.ajustar_alvo(self.canto, base))