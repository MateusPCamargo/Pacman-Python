import pygame
import random
import sys
from personagens.pacman import Pacman
from mapas.mapa1 import Mapa
from personagens.fantasma import Fantasma

pygame.init()

TAMANHO_BLOCO = 24

LARGURA = 28 * TAMANHO_BLOCO
ALTURA = 24 * TAMANHO_BLOCO

pontuacao = 0

tela = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
pygame.display.set_caption("Pac-Man")


mapa = Mapa(tela)
pacman_x, pacman_y = mapa.definir_pacman(TAMANHO_BLOCO)
fantasma_x, fantasma_y = mapa.definir_fantasma(TAMANHO_BLOCO)

pacman = Pacman(pacman_x, pacman_y, mapa, pontuacao)
fantasma = Fantasma(fantasma_x, fantasma_y, mapa)

loop = True

fonte = pygame.font.Font(None, 16)

while (loop):
    dt = clock.tick(60)

    for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    

    pacman.atualizar(dt)
    alvo = (pacman.x, pacman.y)
    fantasma.atualizar(dt, alvo)

    tela.fill((0, 0, 0))

    mapa.desenhar_mapa()

    texto = fonte.render(f"Pontuação: {pacman.pontuacao}", True, (255, 255, 255))
    tela.blit(texto, (10, 10))

    pacman.desenhar(tela)
    fantasma.desenhar_fantasma(tela)

    pygame.display.flip()

    