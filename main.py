import sys

import pygame
from pygame.locals import QUIT

pygame.init()
pygame.mouse.set_visible(False)

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))

mars = pygame.image.load("mars.png").convert()

running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False

    screen.fill((0, 0, 0))
    screen.blit(mars, (0, 400))
    pygame.display.flip()

pygame.quit()
