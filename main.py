import sys

import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

pygame.init()
pygame.mouse.set_visible(False)

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
FPS = 60
RIGHT = 1
LEFT = -1

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Alien(pygame.sprite.Sprite):
    SPEED = 20

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("alien.png").convert_alpha()
        self.rect = self.image.get_rect(
            center=((SCREEN_WIDTH - self.image.get_width()) / 2, SCREEN_HEIGHT - 100)
        )
        self.direction = RIGHT

    def change_direction(self, new_direction):
        if self.direction != new_direction:
            self.image = pygame.transform.flip(self.image, True, False)
            self.direction = new_direction

    def update(self, direction):
        self.change_direction(direction)

        if direction == RIGHT:
            if self.rect.x + (self.image.get_width() / 2) + self.SPEED < SCREEN_WIDTH:
                self.rect.move_ip(self.SPEED * direction, 0)
        elif direction == LEFT:
            if self.rect.x - self.SPEED > 0:
                self.rect.move_ip(self.SPEED * direction, 0)


class Ray(pygame.sprite.Sprite):
    SPEED = 5

    def __init__(self, x_pos, direction):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(x=x_pos, y=493)
        self.direction = direction

    def update(self):
        self.rect.move_ip(self.SPEED * self.direction, 0)

        if (self.rect.x < 0) or (self.rect.x > SCREEN_WIDTH):
            self.kill()


mars = pygame.image.load("mars.png").convert()
alien = Alien()

all_sprites = pygame.sprite.Group()
all_sprites.add(alien)
rays = pygame.sprite.Group()

running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == ord("a"):
                alien.update(direction=LEFT)
            if event.key == K_RIGHT or event.key == ord("d"):
                alien.update(direction=RIGHT)
            if event.key == K_SPACE:
                if alien.direction == RIGHT:
                    x_pos = alien.rect.right
                else:
                    x_pos = alien.rect.left
                ray = Ray(x_pos, alien.direction)

                rays.add(ray)
                all_sprites.add(ray)

    screen.fill((0, 0, 0))
    screen.blit(mars, (0, 400))

    for ray in rays:
        ray.update()

    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
