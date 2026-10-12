import pygame

pygame.init()

class Mapa:
    def __init__(self, tela):
        self.tela = tela
        self.tamanho_bloco = 24
        fonte = pygame.font.SysFont("arial", 32)

        self.mapa = [
            "1111111111111111111111111111",
            "1331333313333113333131333331",
            "1311333311313113111131333131",
            "1333333313313113111131113131",
            "1311111313333333333133333131",
            "1433333313111001113333333341",
            "1111333113116789113333111311",
            "3333333113111111113333333333",
            "1111113113333333333113133311",
            "1113333113111111113113333311",
            "1113113113111111113113133311",
            "1113113313333353333113133111",
            "1113113313111111113113133111",
            "1333343333333113333333333341",
            "1311133333313113113313111131",
            "1311133111113113113113111131",
            "1333133113333333333333113331",
            "1113133113111113113113333111",
            "1113113113133113313113333111",
            "1333334113333113333114333331",
            "1311131111113113111111311131",
            "1311133333113113111111311131",
            "1333333333333233333333333331",
            "1111111111111111111111111111",
            ]


    def desenhar_mapa(self):
        for linha, conteudo in enumerate(self.mapa):
            for coluna, bloco in enumerate(conteudo):

                x = coluna * self.tamanho_bloco
                y = linha * self.tamanho_bloco

                if bloco == "1":

                    pygame.draw.rect(
                        self.tela,
                        (000, 000, 150),
                        (x, y, self.tamanho_bloco, self.tamanho_bloco)
                    )


                elif bloco == "3":
                    pygame.draw.circle(
                        self.tela,
                        (255, 255, 255),
                        (
                            x + self.tamanho_bloco // 2,
                            y + self.tamanho_bloco // 2
                        ),
                        3
                    )

                elif bloco == "4":
                    pygame.draw.circle(
                        self.tela,
                        (255, 255, 255),
                        (
                        x + self.tamanho_bloco // 2,
                        y + self.tamanho_bloco // 2 
                        ),
                        6
                    )

            
    def verificar_parede(self, x, y):
        coluna = int(x // self.tamanho_bloco)
        linha = int(y // self.tamanho_bloco)

        if linha < 0 or linha >= len(self.mapa):
            return True

        if coluna < 0 or coluna >= len(self.mapa[linha]):
            return True

        return self.mapa[linha][coluna] == "1"

    def definir_pacman(self, tamanho_bloco):
        for linha in range(len(self.mapa)):
            for coluna in range(len(self.mapa[linha])):
                if self.mapa[linha][coluna] == "2":
                    x = coluna * tamanho_bloco 
                    y = linha * tamanho_bloco

                    self.mapa[linha] = (
                        self.mapa[linha][:coluna]
                        + "0" + self.mapa[linha][coluna + 1:]
                    )
                    return x, y

    def definir_fantasma(self, tamanho_bloco):
        for linha in range(len(self.mapa)):
            for coluna in range(len(self.mapa[linha])):
                if self.mapa[linha][coluna] == "6":
                    x = coluna * tamanho_bloco 
                    y = linha * tamanho_bloco
        
                    self.mapa[linha] = (
                        self.mapa[linha][:coluna]
                        + "0" + self.mapa[linha][coluna + 1:]
                    )
                    return x, y

    def definir_fantasma2(self, tamanho_bloco):
            for linha in range(len(self.mapa)):
                for coluna in range(len(self.mapa[linha])):
                    if self.mapa[linha][coluna] == "7":
                        x = coluna * tamanho_bloco 
                        y = linha * tamanho_bloco
            
                        self.mapa[linha] = (
                            self.mapa[linha][:coluna]
                            + "0" + self.mapa[linha][coluna + 1:]
                        )
                        return x, y
