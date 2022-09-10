import random
import sys

import pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

MIN_VER = (3, 7)

if sys.version_info[:2] < MIN_VER:
    sys.exit("This game requires Python {}.{}.".format(*MIN_VER))

pygame.init()
pygame.mouse.set_visible(False)

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
GROUND_LEVEL = SCREEN_HEIGHT - 75  # 525
FPS = 60
RIGHT = 1
LEFT = -1

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADD_ROVER = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ROVER, random.randrange(1000, 5000))

ADD_SATELLITE = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_SATELLITE, 10000)

ADD_BEAM = pygame.USEREVENT + 3
pygame.time.set_timer(ADD_BEAM, random.randrange(5000, 10000))

ADD_ASTEROID = pygame.USEREVENT + 4
pygame.time.set_timer(ADD_ASTEROID, random.randrange(7000, 11000))

DUST_STORM = pygame.USEREVENT + 5
pygame.time.set_timer(DUST_STORM, random.randrange(11000, 15000))


class Alien(pygame.sprite.Sprite):
    SPEED = 20

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("alien.png").convert_alpha()
        self.rect = self.image.get_rect(
            center=((SCREEN_WIDTH - self.image.get_width()) / 2, GROUND_LEVEL)
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


class Rover(pygame.sprite.Sprite):
    SPEED = 3

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("rover.png").convert_alpha()
        self.direction = random.choice([RIGHT, LEFT])
        self.rect = self.image.get_rect(y=SCREEN_HEIGHT - 85)
        self.rect.x = 0 - self.rect.width if self.direction == RIGHT else SCREEN_WIDTH

    def update(self):
        self.rect.move_ip(self.SPEED * self.direction, 0)

        if (self.rect.width < 0) or (self.rect.x > SCREEN_WIDTH):
            self.kill()


class Satellite(pygame.sprite.Sprite):
    SPEED = 1

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("satellite.png").convert_alpha()
        self.direction = RIGHT
        self.rect = self.image.get_rect(x=-10, y=100)

    def update(self):
        self.rect.move_ip(self.SPEED * self.direction, 0)

        if (self.rect.width < 0) or (self.rect.x > SCREEN_WIDTH):
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("asteroid.png").convert_alpha()
        self.rect = self.image.get_rect(
            x=random.randrange(-SCREEN_WIDTH, SCREEN_WIDTH), y=0
        )

    def update(self):
        self.rect.move_ip(random.randrange(10), random.randrange(5, 10))

        if self.rect.centery >= GROUND_LEVEL:
            self.kill()


class Ray(pygame.sprite.Sprite):
    SPEED = 5

    def __init__(self, x_pos, direction):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(x=x_pos, y=518)
        self.direction = direction

    def update(self):
        self.rect.move_ip(self.SPEED * self.direction, 0)

        if (self.rect.x < 0) or (self.rect.x > SCREEN_WIDTH):
            self.kill()


class Beam(pygame.sprite.Sprite):
    SPEED = 10

    def __init__(self, x_pos):
        super().__init__()
        self.image = pygame.Surface((2, 50))
        self.image.fill((250, 45, 182))
        self.rect = self.image.get_rect(x=x_pos, top=120)

    def update(self):
        self.rect.move_ip(0, self.SPEED)

        if self.rect.bottom >= GROUND_LEVEL:
            self.kill()


class Dust(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((3, 3))
        self.image.fill((181, 128, 95))
        self.rect = self.image.get_rect(
            x=random.randrange(SCREEN_WIDTH), y=random.randrange(SCREEN_HEIGHT)
        )
        self.start_time = pygame.time.get_ticks()
        self.duration = random.randrange(2500, 5000)

    def update(self):
        self.rect.x = random.randrange(SCREEN_WIDTH)
        self.rect.y = random.randrange(SCREEN_HEIGHT)

        if pygame.time.get_ticks() - self.start_time > self.duration:
            self.kill()


mars = pygame.image.load("mars.png").convert()
alien = Alien()

all_sprites = pygame.sprite.Group()
all_sprites.add(alien)

satellites = pygame.sprite.Group()
rays = pygame.sprite.Group()
enemies = pygame.sprite.Group()
dust_storm = pygame.sprite.Group()


class Game:
    def __init__(self):
        self.stage = 0
        self.score = 0
        self.running = True

    def play(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ):
                    self.running = False
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
                elif event.type == ADD_ROVER:
                    rover = Rover()
                    all_sprites.add(rover)
                    enemies.add(rover)
                elif event.type == ADD_SATELLITE and self.stage >= 1:
                    satellite = Satellite()
                    all_sprites.add(satellite)
                    satellites.add(satellite)
                    enemies.add(satellite)
                elif (
                    event.type == ADD_BEAM and self.stage >= 2 and satellites.sprites()
                ):
                    firing_satellite = random.choice(satellites.sprites())
                    beam = Beam(x_pos=firing_satellite.rect.x)
                    all_sprites.add(beam)
                    enemies.add(beam)
                elif event.type == ADD_ASTEROID and self.stage >= 3:
                    asteroid = Asteroid()
                    all_sprites.add(asteroid)
                    enemies.add(asteroid)
                elif event.type == DUST_STORM and self.stage >= 4:
                    for _ in range(20000):
                        dust = Dust()
                        dust_storm.add(dust)
                        all_sprites.add(dust)

            screen.fill((0, 0, 0))
            screen.blit(mars, (0, 400))

            for enemy in enemies:
                enemy.update()

            for ray in rays:
                ray.update()

            for dust in dust_storm:
                dust.update()

            for sprite in all_sprites:
                screen.blit(sprite.image, sprite.rect)

            if pygame.sprite.groupcollide(enemies, rays, True, True):
                self.score += 1

                if self.score > 20:
                    self.stage = 4
                elif self.score > 10:
                    self.stage = 3
                elif self.score > 5:
                    self.stage = 2
                elif self.score > 3:
                    self.stage = 1

            if pygame.sprite.spritecollideany(alien, enemies):
                self.running = False

            pygame.display.flip()
            clock.tick(FPS)

        self.game_over()

    def game_over(self):
        font = pygame.font.Font(None, 64)
        text = font.render(f"Game Over! You scored {self.score}", True, (181, 128, 95))
        textpos = text.get_rect(centerx=SCREEN_WIDTH / 2, y=50)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ):
                    pygame.quit()
                    sys.exit()

            screen.fill((0, 0, 0))
            screen.blit(mars, (0, 400))
            screen.blit(text, textpos)
            pygame.display.flip()


game = Game()
game.play()
