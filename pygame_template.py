import pygame
import sys
import math
import random

# базовые настройки экрана игры
WIDTH = 360
HEIGHT = 480
FPS = 30

# Цвет
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# инициализация игры и окна
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

running = True
while running:
    # цикл обновления экрана
    clock.tick(FPS)

    # событие игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK) # заполнение (рендеринг) экрана
    pygame.display.flip() # показываем экран

pygame.quit()