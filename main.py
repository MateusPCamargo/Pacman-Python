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
pontos_fantasma = 200

tela = pygame.display.set_mode((LARGURA, ALTURA))
fonte = pygame.font.Font(None, 16)
clock = pygame.time.Clock()
pygame.display.set_caption("Pac-Man")

def novo_jogo():
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

    return mapa, pacman, blinky, [blinky, pinky, inky, clyde]


mapa, pacman, blinky, fantasmas = novo_jogo()


vidas = 3
game_over = False
pausa = 0 
vitoria = False
fonte_grande = pygame.font.Font(None, 48)

loop = True

while (loop):
    dt = clock.tick(60)

    for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if game_over or vitoria:
                    mapa, pacman, blinky, fantasmas = novo_jogo()
                    vidas = 3
                    game_over = False
                    vitoria = False
                    pausa = 0
                    pontos_fantasma = 200

    if not game_over and not vitoria and mapa.pontos_restantes() == 0:
        vitoria = True
    if pausa > 0:
        pausa -= dt
    elif not game_over and not vitoria:
        pacman.atualizar(dt)

        if pacman.pegou_poder:
            pacman.pegou_poder = False
            pontos_fantasma = 200
            for f in fantasmas:
                f.assustar(6000)                # duração em ms

        for fantasma in fantasmas:
            alvo = fantasma.calcular_alvo(pacman, blinky)
            fantasma.atualizar(dt, alvo)

        for fantasma in fantasmas:
            if fantasma.colidiu_com(pacman):
                if fantasma.assustado:
                    fantasma.resetar()
                    pacman.pontuacao += pontos_fantasma
                    pontos_fantasma *= 2        # 200, 400, 800, 1600
                else:
                    vidas -= 1
                    if vidas <= 0:
                        game_over = True
                    else:
                        pacman.resetar()
                        for f in fantasmas:
                            f.resetar()
                        pausa = 1000
                    break 

    

    tela.fill((0, 0, 0))

    mapa.desenhar_mapa()

    pacman.desenhar(tela)
    for fantasma in fantasmas:
        fantasma.desenhar_fantasma(tela)

    texto = fonte.render(f"Pontuação: {pacman.pontuacao}", True, (255, 255, 255))
    tela.blit(texto, (10, 4))

    tela.blit(fonte.render(f"Vidas: {vidas}", True, (255, 255, 255)), (10, 14))


    centro = tela.get_rect().center
    if game_over:
        tela.fill((0, 0, 0))
        texto = fonte_grande.render("GAME OVER", True, (255, 0, 0))
        tela.blit(texto, texto.get_rect(center=tela.get_rect().center))

        pontos = fonte.render(f"Pontuação: {pacman.pontuacao}", True, (255, 255, 255))
        tela.blit(pontos, pontos.get_rect(center=(centro[0], centro[1] + 25)))

        dica = fonte.render("Pressione ENTER para reiniciar", True, (200, 200, 200))
        tela.blit(dica, dica.get_rect(center=(centro[0], centro[1] + 60)))

    if vitoria:
        tela.fill((0, 0, 0))
        texto = fonte_grande.render("VOCÊ VENCEU!", True, (0, 255, 0))
        tela.blit(texto, texto.get_rect(center=tela.get_rect().center))

        pontos = fonte.render(f"Pontuação: {pacman.pontuacao}", True, (255, 255, 255))
        tela.blit(pontos, pontos.get_rect(center=(centro[0], centro[1] + 25)))

        dica = fonte.render("Pressione ENTER para reiniciar", True, (200, 200, 200))
        tela.blit(dica, dica.get_rect(center=(centro[0], centro[1] + 60)))

    pygame.display.flip()

    