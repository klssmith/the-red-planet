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
    SPEED = 20

    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("alien.png").convert_alpha()
        self.rect = self.surf.get_rect(
            center=((SCREEN_WIDTH - self.surf.get_width()) / 2, SCREEN_HEIGHT - 100)
        )
        self.direction = "right"

    def change_direction(self, new_direction):
        if self.direction != new_direction:
            self.surf = pygame.transform.flip(self.surf, True, False)
            self.direction = new_direction

    def update(self, move):
        self.change_direction(move)

        if move == "right":
            if self.rect.x + (self.surf.get_width() / 2) + self.SPEED < SCREEN_WIDTH:
                self.rect.move_ip(self.SPEED, 0)
        elif move == "left":
            if self.rect.x - self.SPEED > 0:
                self.rect.move_ip(-self.SPEED, 0)


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
                alien.update(move="left")
            if event.key == pygame.K_RIGHT or event.key == ord("d"):
                alien.update(move="right")

    screen.fill((0, 0, 0))
    screen.blit(mars, (0, 400))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()


pygame.quit()
