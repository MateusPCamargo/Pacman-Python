import pygame
import random
import sys
from personagens.pacman import Pacman
from mapas.mapa1 import Mapa
from personagens.fantasma import Blinky, Pinky, Inky, Clyde

pygame.init()

TAMANHO_BLOCO = 24

LARGURA = 28 * TAMANHO_BLOCO
ALTURA = 24 * TAMANHO_BLOCO

pontuacao = 0

tela = pygame.display.set_mode((LARGURA, ALTURA))
fonte = pygame.font.Font(None, 16)
clock = pygame.time.Clock()
pygame.display.set_caption("Pac-Man")


mapa = Mapa(tela)
pacman_x, pacman_y = mapa.definir_pacman(TAMANHO_BLOCO)
blinky_x, blinky_y = mapa.definir_Blinky(TAMANHO_BLOCO)
pinky_x, pinky_y = mapa.definir_Pinky(TAMANHO_BLOCO)
inky_x, inky_y = mapa.definir_Inky(TAMANHO_BLOCO)
clyde_x, clyde_y = mapa.definir_Clyde(TAMANHO_BLOCO)


pacman = Pacman(pacman_x, pacman_y, mapa, pontuacao)
blinky = Blinky(blinky_x, blinky_y, mapa)
pinky = Pinky(pinky_x, pinky_y, mapa)
inky = Inky(inky_x, inky_y, mapa)
clyde = Clyde(clyde_x, clyde_y, mapa)

fantasmas = [blinky, pinky, inky, clyde]

loop = True

while (loop):
    dt = clock.tick(60)

    for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    

    pacman.atualizar(dt)
    for fantasma in fantasmas:
        alvo = fantasma.calcular_alvo(pacman, blinky)
        fantasma.atualizar(dt, alvo)

    

    tela.fill((0, 0, 0))

    mapa.desenhar_mapa()

    texto = fonte.render(f"Pontuação: {pacman.pontuacao}", True, (255, 255, 255))
    tela.blit(texto, (10, 10))

    pacman.desenhar(tela)
    for fantasma in fantasmas:
        fantasma.desenhar_fantasma(tela)

    pygame.display.flip()

    