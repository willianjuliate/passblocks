import pygame
from random import randint
from time import sleep

pygame.init()

pygame_icon = pygame.image.load('assets/images/miniatura.png')
pygame.display.set_icon(pygame_icon)

# Definições da Janela
window = (1050, 400)
screen = pygame.display.set_mode(window)
pygame.display.set_caption('passblocks')

# FPS
clock = pygame.time.Clock()
dt = 0

# Definições dos Objetos
fonte = pygame.font.Font('assets/font/pixelart.ttf', 14)
fonte_lose = pygame.font.Font('assets/font/pixelart.ttf', 100)

player: pygame.Rect = pygame.Rect(10, 380, 20, 20)
apple: pygame.Rect = pygame.Rect(1030, 390, 8, 8)

heart: list = [
    (pygame.Rect(10, 15, 10, 10), pygame.Rect(10, 15, 10, 10)),
    (pygame.Rect(25, 15, 10, 10), pygame.Rect(25, 15, 10, 10)),
    (pygame.Rect(40, 15, 10, 10), pygame.Rect(40, 15, 10, 10)),
    (pygame.Rect(55, 15, 10, 10), pygame.Rect(55, 15, 10, 10))]

block: list = [
    (pygame.Rect(230, randint(1, 300), 150, 150), pygame.Rect(305, 0, 5, 400)),
    (pygame.Rect(410, randint(1, 300), 150, 150), pygame.Rect(485, 0, 5, 400)),
    (pygame.Rect(590, randint(1, 300), 150, 150), pygame.Rect(665, 0, 5, 400)),
    (pygame.Rect(770, randint(1, 300), 150, 150), pygame.Rect(845, 0, 5, 400))]

# Variaveis de controle
seends: tuple = (randint(1, 4), randint(1, 4), randint(1, 4), randint(1, 4))
direction_validation: list = [True, True, True, True]
running: bool = True
lifes: int = 4
score: int = 0


# Loop Game
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

    screen.fill('#262626')
    screen.blit(fonte.render(
        f'{score}', True, (255, 255, 255)), (10, 30))

    for i in range(len(block)):
        pygame.draw.rect(screen, '#303030', block[i][1])  # Barra
        pygame.draw.rect(screen, '#ca3f6d', block[i][0])  # Bloco

        pygame.draw.rect(screen, '#4d4d4d', heart[i][0])  # Vida
        pygame.draw.rect(screen, '#649cf9', heart[i][1])  # Sombra da Vida

        if direction_validation[i]:
            block[i][0].move_ip(0, seends[i])
            if block[i][0].bottom >= 400:
                direction_validation[i] = False
        if not direction_validation[i]:
            block[i][0].move_ip(0, -seends[i])
            if block[i][0].top <= 0:
                direction_validation[i] = True

        if player.colliderect(block[i][0]):
            seends = (randint(1, 4), randint(1, 4),
                      randint(1, 4), randint(1, 4))
            sleep(0.5)
            if score % 2 == 0:
                player.left = 10
            else:
                player.left = 1000
            heart[lifes-1][1].left = -20
            lifes -= 1

    pygame.draw.rect(screen, '#46d173', player)  # Jogador
    pygame.draw.rect(screen, '#f86c56', apple)  # Maçã

    # Colisão entre o objeto para capturar os pontos
    # Define se o 'player' reaparece na esquerda ou direita
    if player.colliderect(apple):
        seends = (randint(1, 4), randint(1, 4),
                  randint(1, 4), randint(1, 4))
        score += 1
        if score % 2 == 0:
            apple.left = 1030
        else:
            apple.left = 10

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.move_ip(2, 0)
        if player.right > 1050:
            player.right = 1050
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.move_ip(-2, 0)
        if player.left < -1:
            player.left = -1

    if lifes == 0:
        screen.blit(fonte_lose.render(f'you lose',
                    True, (255, 255, 255)), (250, 100))
        if keys[pygame.K_SPACE]:
            running = False

        if score % 2 == 0:
            player.left = 10
        else:
            player.left = 1000

    pygame.display.flip()
    dt = clock.tick(120)

pygame.quit()
