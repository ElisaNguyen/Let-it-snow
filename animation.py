"""Animate the created snowflakes as falling snow"""
import os
#import turtle
#from LSystem import create_snowflake
#os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
import random


class Snowflake(pygame.sprite.Sprite):
    """Each instance of this class is a single snowflake sprite"""

    def __init__(self, index, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        shape = pygame.image.load(r'images\snowflake' + str(index) + '.png').convert_alpha()
        self.width = random.choice(range(20, 80))
        self.height = self.width
        self.index = index
        self.image = pygame.transform.scale(shape, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = random.uniform(0, screen_width)
        self.rect.y = random.uniform(0, screen_height)
        self.speedX = random.uniform(-2, 2)
        self.melt = False
        self.alpha = 255

    def update(self, screen_width, screen_height):
        self.rect.x += self.speedX
        if self.melt:  # If the fade effect is activated.
            # Reduce the alpha each frame, create a new copy of the original
            # image and fill it with white (with the self.alpha value)
            # and pass the BLEND_RGBA_MULT special_flag to reduce the alpha.
            self.alpha = max(0, self.alpha - 2)  # alpha should never be < 0.
            self.image.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
            if self.alpha <= 0:  # move it back up
                self.rect.y = screen_height + 1
                self.alpha = 255
                self.melt = False
                image = pygame.image.load(r'images\snowflake' + str(self.index) + '.png')
                self.image = pygame.transform.scale(image, (self.width, self.height))
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
        image = pygame.image.load(r'images\snowflake' + str(self.index) + '.png')
        self.image = pygame.transform.scale(image, (150, 150))


def let_it_snow():
    screen_width = 1000
    screen_height = 600
    pygame.init()

    SIZE = [screen_width, screen_height]

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Let it snow")

    # background image
    bg = pygame.image.load(r'images\background.jpg').convert()
    bg = pygame.transform.scale(bg, (screen_width, screen_height))

    # Create a sprite groups for the snowflakes
    snow_sprites = pygame.sprite.Group()

    # Loop 80 times and add a snowflake sprite
    for i in range(80):
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
                snowflake.zoom()
                snowflake.melt = True
            snowflake.update(screen_width, screen_height)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        clock.tick(20)

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

let_it_snow()
