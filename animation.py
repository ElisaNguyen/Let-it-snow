"""Animate the created snowflakes as falling snow"""
import LSystem
import pygame
import random

screen_width = 500
screen_height = 500


class Snowflake:
    """Each instance of this class is a single snowflake"""

    def __init__(self):
        self.xPos = random.choice(range(0, screen_width))
        self.yPos = random.choice(range(0, screen_height))
        self.speedX = random.choice(range(-2, 2))
        self.width = random.choice(range(0, 10))
        self.height = self.width
        self.shape = None

pygame.init()
SIZE = [screen_width, screen_height]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Snow Animation")

# Create an empty array to fill with snowflakes
snow_list = []

# Loop 50 times and add a snowflake from class snowflake
for i in range(3):
    snow_list.append(Snowflake())

print(snow_list)
# create 50 snowflakes
LSystem.create_snowflakes(3)

clock = pygame.time.Clock()

# Loop until the user clicks the close button.
done = False
while not done:

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # Set the screen background
    screen.fill(BLACK)

    # Process each snow flake in the list
    for i in range(len(snow_list)):

        # Get the snowflake image
        snow_list[i].shape = pygame.image.load('snowflake' + str(i) + '.png').convert_alpha()

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
