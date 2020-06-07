"""Animate the created snowflakes as falling snow
inspiration: http://programarcadegames.com/python_examples/f.php?file=animating_snow.py"""
import LSystem
import pygame
import random

screen_width = 1000
screen_height = 600


class Snowflake:
    """Each instance of this class is a single snowflake"""

    def __init__(self, index):
        self.xPos = random.choice(range(0, screen_width))
        self.yPos = random.choice(range(0, screen_height))
        self.speedX = random.choice(range(-2, 2))
        self.width = random.choice(range(20, 100))
        self.height = self.width
        shape = pygame.image.load(LSystem.create_snowflake(index)).convert_alpha()
        shape = pygame.transform.scale(shape, (self.width, self.height))
        self.shape = shape

pygame.init()

SIZE = [screen_width, screen_height]

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Let it snow")

# background image
bg = pygame.image.load('background.jpg').convert()
bg = pygame.transform.scale(bg, (screen_width, screen_height))

# Create an empty array to fill with snowflakes
snow_list = []

# Loop 50 times and add a snowflake from class snowflake
for i in range(2):
    snow_list.append(Snowflake(i))

clock = pygame.time.Clock()

# Loop until the user clicks the close button.
done = False
while not done:

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # Set the screen background
    screen.blit(bg, [0, 0])

    # Process each snow flake in the list
    for i in range(len(snow_list)):
        # Move the snow flake
        snow_list[i].xPos += snow_list[i].speedX
        snow_list[i].yPos += 1

        # If the snow flake has moved off the bottom of the screen
        if snow_list[i].yPos > screen_height:
            # Reset it just above the top
            y = random.randrange(-50, -10)
            snow_list[i].yPos = y
            # Give it a new x position
            x = random.randrange(0, screen_width)
            snow_list[i].xPos = x

        screen.blit(snow_list[i].shape, (snow_list[i].xPos, snow_list[i].yPos))

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    clock.tick(20)

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
