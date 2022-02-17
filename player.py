import pygame

# In every file, we need to define the screen size and the colors used.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# This is the pacman class. He affects the x and the y.
class Pacman(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    explosion = False
    game_over = False

    def __init__(self, x, y, filename):
        # Call the Sprite class, which is necessary for every visible element of the game.
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.image.set_colorkey(BLACK)
        # Load the image that represents the pacman walking
        picture = pygame.image.load("walk.png").convert()
        # Create the animations of the objects, 32x32 pixels
        self.move_right_animation = Animation(picture, 32, 32)
        self.move_left_animation = Animation(pygame.transform.flip(picture, True, False), 32, 32)
        self.move_up_animation = Animation(pygame.transform.rotate(picture, 90), 32, 32)
        self.move_down_animation = Animation(pygame.transform.rotate(picture, 270), 32, 32)
        # Load explosion image, when the pacman dies.
        picture = pygame.image.load("explosion.png").convert()
        self.explosion_animation = Animation(picture, 30, 30)
        # Save the player image, so that the pacman stays the same in every game
        self.player_image = pygame.image.load(filename).convert()
        self.player_image.set_colorkey(BLACK)

    # This is for the teleportation from one side to another for the player
    def update(self, horizontal_blocks, vertical_blocks):
        if not self.explosion:
            if self.rect.right < 0:
                self.rect.left = SCREEN_WIDTH
            elif self.rect.left > SCREEN_WIDTH:
                self.rect.right = 0
            if self.rect.bottom < 0:
                self.rect.top = SCREEN_HEIGHT
            elif self.rect.top > SCREEN_HEIGHT:
                self.rect.bottom = 0
            self.rect.x += self.change_x
            self.rect.y += self.change_y

            # This will stop the pacman from entering the walls
            # So, the pacman can't pass through the walls.

            for block in pygame.sprite.spritecollide(self, horizontal_blocks, False):
                self.rect.centery = block.rect.centery
                self.change_y = 0
            for block in pygame.sprite.spritecollide(self, vertical_blocks, False):
                self.rect.centerx = block.rect.centerx
                self.change_x = 0

            # This will cause the animation to start when he moves (up, down, left, right), or when he dies.

            if self.change_x > 0:
                self.move_right_animation.quality(10)
                self.image = self.move_right_animation.current_image()
            elif self.change_x < 0:
                self.move_left_animation.quality(10)
                self.image = self.move_left_animation.current_image()

            if self.change_y > 0:
                self.move_down_animation.quality(10)
                self.image = self.move_down_animation.current_image()
            elif self.change_y < 0:
                self.move_up_animation.quality(10)
                self.image = self.move_up_animation.current_image()
        else:
            if self.explosion_animation.index == self.explosion_animation.get_length() - 1:
                pygame.time.wait(500)
                self.game_over = True
            self.explosion_animation.quality(30)
            self.image = self.explosion_animation.current_image()

# Set the movement of the pacman, and when he stops. This is the speed of the pacman
    def move_right(self):
        self.change_x = 4

    def move_left(self):
        self.change_x = -4

    def move_up(self):
        self.change_y = -4

    def move_down(self):
        self.change_y = 4

    def stop_move_right(self):
        if self.change_x != 0:
            self.image = self.player_image
        self.change_x = 0

    def stop_move_left(self):
        if self.change_x != 0:
            self.image = pygame.transform.rotate(self.player_image, 180)
        self.change_x = 0

    def stop_move_up(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image, 90)
        self.change_y = 0

    def stop_move_down(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image, 270)
        self.change_y = 0

# This class is for the movement of the pacman and the enemies. The mouth of the pacman needs to be animated.
class Animation(object):
    def __init__(self, img, width, height):
        self.sprite_sheet = img
        # This list stores the images, so they won't disappear
        self.image_list = []
        self.load_images(width, height)
        # This variable holds the current image in the list
        self.index = 0
        # Create a clock for the time Remember, time is necessary for the movement of the pacman.
        self.clock = 1

    def load_images(self, width, height):
        # This is for the loading of the images
        for y in range(0, self.sprite_sheet.get_height(), height):
            for x in range(0, self.sprite_sheet.get_width(), width):
                # We load the image in another list
                photo = self.get_image(x, y, width, height)
                self.image_list.append(photo)

    def get_image(self, x, y, width, height):
        # This is for the surface of the image
        image = pygame.Surface([width, height]).convert()
        # This is for the shrinking of the picture
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        # I chose black because it is transparent in the game, as the screen is already black.
        image.set_colorkey((0, 0, 0))
        return image

    def current_image(self):
        return self.image_list[self.index]

    def get_length(self):
        return len(self.image_list)
# This is for the quality of the animation. 30 fps is good enough because it's an arcade game.
    def quality(self, fps=30):
        step = 30 // fps
        frames = range(1, 30, step)
        if self.clock == 30:
            self.clock = 1
        else:
            self.clock += 1

        if self.clock in frames:
            self.index += 1
            if self.index == len(self.image_list):
                self.index = 0
