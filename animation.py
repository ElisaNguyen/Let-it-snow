"""Animate the created snowflakes as falling snow"""
import turtle
from LSystem import create_snowflake
import pygame
import random


class Snowflake(pygame.sprite.Sprite):
    """Each instance of this class is a single snowflake sprite"""

    def __init__(self, index, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        shape = pygame.image.load(create_snowflake(index)).convert_alpha()
        self.width = random.choice(range(20, 100))
        self.height = self.width
        shape = pygame.transform.scale(shape, (self.width, self.height))
        self.image = shape
        self.rect = self.image.get_rect()
        self.rect.x = random.uniform(0, screen_width)
        self.rect.y = random.uniform(0, screen_height)
        self.speedX = random.uniform(-2, 2)

    def move(self, screen_width, screen_height):
        self.rect.x += self.speedX
        if self.rect.y > screen_height:
            # Reset it just above the top
            y = random.randrange(-50, -10)
            self.rect.y = y
            # Give it a new x position
            x = random.randrange(0, screen_width)
            self.rect.x = x
        else:
            self.rect.y += 1

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

    def zoom(self):
        self.image = pygame.transform.scale(self.image, (150, 150))

    def zoomout(self):
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


def let_it_snow(num_snowflakes):
    screen_width = 1000
    screen_height = 600
    pygame.init()

    SIZE = [screen_width, screen_height]

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Let it snow")

    # background image
    bg = pygame.image.load('background.jpg').convert()
    bg = pygame.transform.scale(bg, (screen_width, screen_height))

    # Create a sprite groups for the snowflakes
    snow_sprites = pygame.sprite.Group()

    # Loop num_snowflakes times and add a snowflake sprite
    for i in range(num_snowflakes):
        snow_sprites.add(Snowflake(i, screen_width, screen_height))

    clock = pygame.time.Clock()

    # Loop until the user clicks the close button.
    done = False
    while not done:

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        # Set the screen background
        screen.blit(bg, [0, 0])

        # Draw the sprites
        snow_sprites.draw(screen)

        for snowflake in snow_sprites:
            if snowflake.is_clicked():
                print('yes')
                snowflake.zoom()
            snowflake.move(screen_width, screen_height)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        clock.tick(20)

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
    turtle.done()

