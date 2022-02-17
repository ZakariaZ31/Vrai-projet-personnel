import pygame
import random

# This is the screen size. I chose this one because I don't want the screen to be really huge.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576


# These are all the colors that we are going to use. These coordinates represents the Python code for the colors.
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


# This is the map that I am going to use.
# 18x25 blocks of 32x32 pixels
# 0 represents the unused space. 1 represents the horizontal path that the pacman can travel in.
# 2 represents the vertical path. 3 represents the connection between the 2 paths.


def map():
    grid = ((0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0))

    return grid

# This is for the lines that separate the path and the unused area
# Here, we also define the meaning of 1 and 2 in the map, the horizontal and vertical paths.

def create_map(screen):
    for a, row in enumerate(map()):
        for b, item in enumerate(row):
            if item == 1:
                pygame.draw.line(screen, GREEN, [b * 32, a * 32], [b * 32 + 32, a * 32], 3)
                pygame.draw.line(screen, GREEN, [b * 32, a * 32 + 32], [b * 32 + 32, a * 32 + 32], 3)
            elif item == 2:
                pygame.draw.line(screen, GREEN, [b * 32, a * 32], [b * 32, a * 32 + 32], 3)
                pygame.draw.line(screen, GREEN, [b * 32 + 32, a * 32], [b * 32 + 32, a * 32 + 32], 3)


# This is how to create the little dots that the pacman will eat.
class Dots(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        # Call the class sprite from pygame (it's a pygame class that represents visible objects in the game)
        pygame.sprite.Sprite.__init__(self)
        # Put the background color, which is transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        # Draw the ellipse (no circle because it's more complicated with the radius, etc)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# Now, I created the ghosts, the enemies in the game.
class Enemies(pygame.sprite.Sprite):
    def __init__(self, x, y, change_x, change_y):
        # Call the pygame class (Sprite) 
        pygame.sprite.Sprite.__init__(self)
        # Set the direction of the Enemies. This means that they can change their x and y.
        self.change_x = change_x
        self.change_y = change_y
        # Load the image of the enemies, that we got from pygame.
        self.image = pygame.image.load("slime.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# This is how to create the movement of the enemies, by putting conditions (if,elif)
    def update(self, horizontal_blocks, vertical_blocks):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        # If the objects go to the far right, they will teleport to the far left, and vice versa
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        # If the objects go down too much, they will teleport at the top, and vice versa
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0

# This is how to randomize the movement of the enemies. I need to import something called 'random'.
        # These are also conditions.
        if self.rect.topleft in self.cross():
            direction = random.choice(("left", "right", "up", "down"))
            if direction == "left" and self.change_x == 0:
                self.change_x = -2
                self.change_y = 0
            elif direction == "right" and self.change_x == 0:
                self.change_x = 2
                self.change_y = 0
            elif direction == "up" and self.change_y == 0:
                self.change_x = 0
                self.change_y = -2
            elif direction == "down" and self.change_y == 0:
                self.change_x = 0
                self.change_y = 2

# This is where I explain the number 3 in the map, which is the cross over of two paths
    def cross(self):
        items = []
        for a, row in enumerate(map()):
            for b, item in enumerate(row):
                if item == 3:
                    items.append((b * 32, a * 32))

        return items

# I created a class called Block. Those blocks are actually one 32x32 pixel square. They are defined by x and y.
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        # Call the pygame class (Sprite)
        pygame.sprite.Sprite.__init__(self)
        # Set the color and set it to be transparent, because we need to see what's over the block.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
