import sys

import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()
pygame.mouse.set_visible(False)

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("alien.png").convert_alpha()
        self.rect = self.surf.get_rect(
            center=((SCREEN_WIDTH - self.surf.get_width()) / 2, SCREEN_HEIGHT - 100)
        )

    def update(self, direction):
        if direction == "right":
            self.rect.move_ip(5, 0)
        elif direction == "left":
            self.rect.move_ip(-5, 0)


mars = pygame.image.load("mars.png").convert()
alien = Alien()

all_sprites = pygame.sprite.Group()
all_sprites.add(alien)

running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
        if event.type == KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord("a"):
                alien.update(direction="left")
            if event.key == pygame.K_RIGHT or event.key == ord("d"):
                alien.update(direction="right")

    screen.fill((0, 0, 0))
    screen.blit(mars, (0, 400))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()


pygame.quit()
