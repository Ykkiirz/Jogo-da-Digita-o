import pygame
import json
import random
import os

pygame.init()
tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jogo de Acentuação")
fonte = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (100, 100, 255)
VERDE = (0, 200, 100)
VERMELHO = (255, 0, 0)

# Carregar dados
with open("palavras.json", encoding="utf-8") as f:
    niveis = json.load(f)


# Carregar imagens
imagens = {item["imagem"]: pygame.image.load(os.path.join("imagens", item["imagem"])) for item in niveis}

pontos = 0
nivel = 0

def desenhar_texto(texto, x, y, cor=PRETO):
    img = fonte.render(texto, True, cor)
    tela.blit(img, (x, y))

def mostrar_pergunta(nivel_atual):
    tela.fill(BRANCO)
    dados = niveis[nivel_atual]

    # Mostrar imagem
    imagem = imagens[dados["imagem"]]
    tela.blit(imagem, (300, 50))

    # Gerar opções e embaralhar
    opcoes = dados["corretas"] + dados["erradas"]
    random.shuffle(opcoes)

    botoes = []
    for i, opcao in enumerate(opcoes):
        rect = pygame.Rect(250, 300 + i * 60, 300, 50)
        pygame.draw.rect(tela, AZUL, rect)
        desenhar_texto(opcao, rect.x + 20, rect.y + 10, BRANCO)
        botoes.append((rect, opcao))

    return botoes, dados["corretas"]

def mostrar_pontuacao_final():
    tela.fill(BRANCO)
    desenhar_texto("Fim de jogo!", 300, 200)
    desenhar_texto(f"Pontuação final: {pontos}", 250, 300)
    pygame.display.flip()
    pygame.time.wait(3000)

# Loop principal
rodando = True
botoes = []
resposta_correta = []

while rodando:
    tela.fill(BRANCO)

    if nivel < len(niveis):
        botoes, resposta_correta = mostrar_pergunta(nivel)
    else:
        mostrar_pontuacao_final()
        rodando = False
        continue

    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                esperando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                for rect, palavra in botoes:
                    if rect.collidepoint(evento.pos):
                        if palavra in resposta_correta:
                            pontos += 10
                            nivel += 1
                        else:
                            pontos -= 5
                        esperando = False

        clock.tick(30)

pygame.quit()
