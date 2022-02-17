from player import Pacman
from enemies import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


# This is the class for the game. I will set the rules, the score, the levels, etc.


class Game(object):
    def __init__(self):
        self.font = pygame.font.Font(None, 40)
        self.lost = False
        self.game_over = True
        # Make a variable that will be the score
        self.score = 0
        # Create a zone for putting the scoreboard in the game
        self.font = pygame.font.Font(None, 35)
        # Create the menu of the game
        # Create the name of the levels (level 1, level 2, level 3)
        # We also need to define the color of the writing in the menu. I chose white.
        self.menu = Home_Menu(("Level 1", "Level 2", "Level 3", "Exit"), font_color=WHITE, font_size=60)
        # Create the player, and his spawn location.
        self.player = Pacman(32, 128, "player.png")
        # Create the blocks that will set the paths where the player can go
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        # Create a group for the dots on the screen, which is linked to the ellipse class.
        self.dots_group = pygame.sprite.Group()
        # Here, we set the dots in the map.
        for a, row in enumerate(map()):
            for b, item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(Block(b * 32 + 8, a * 32 + 8, BLACK, 16, 16))
                elif item == 2:
                    self.vertical_blocks.add(Block(b * 32 + 8, a * 32 + 8, BLACK, 16, 16))
        # Create the enemies, and their location, which can be whatever I want but not too close to the pacman.
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Enemies(288, 96, 0, 2))
        self.enemies.add(Enemies(288, 320, 0, -2))
        self.enemies.add(Enemies(544, 128, 0, 2))
        self.enemies.add(Enemies(32, 224, 0, 2))
        self.enemies.add(Enemies(160, 64, 2, 0))
        self.enemies.add(Enemies(448, 64, -2, 0))
        self.enemies.add(Enemies(640, 448, 2, 0))
        self.enemies.add(Enemies(448, 320, 2, 0))
        # Add the dots inside the game
        for a, row in enumerate(map()):
            for b, item in enumerate(row):
                if item != 0:
                    self.dots_group.add(Dots(b * 32 + 12, a * 32 + 12, RED, 8, 8))

        # Load the sound effects, when pacman eats and when he dies.
        self.pacman_sound = pygame.mixer.Sound("pacman_sound.ogg")
        self.game_over_sound = pygame.mixer.Sound("game_over_sound.ogg")

    # Now this is the part where I create levels. I put a condition where something happens if the user does something.
    def gameplay(self):
        for event in pygame.event.get():  # When the player does something
            if event.type == pygame.QUIT:  # If user clicked close
                return True
            self.menu.choose_level(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over and not self.lost:
                        if self.menu.state == 0:
                            # 2 enemies in the first level.
                            self.__init__()
                            self.enemies = pygame.sprite.Group()
                            self.enemies.add(Enemies(288, 96, 0, 2))
                            self.enemies.add(Enemies(288, 320, 0, -2))
                            # Not game over until pacman touches enemies
                            self.game_over = False

                            # If Pacman dies, Game Over
                            self.lost = True

                        elif self.menu.state == 1:
                            # 4 enemies in the second level.
                            self.__init__()
                            self.enemies = pygame.sprite.Group()
                            self.enemies.add(Enemies(288, 96, 0, 2))
                            self.enemies.add(Enemies(288, 320, 0, -2))
                            self.enemies.add(Enemies(544, 128, 0, 2))
                            self.enemies.add(Enemies(32, 224, 0, 2))
                            # Not game over until pacman touches enemies
                            self.game_over = False

                            # If Pacman dies, Game Over
                            self.lost = True

                        elif self.menu.state == 2:
                            # 8 enemies in the third level
                            self.__init__()
                            self.enemies = pygame.sprite.Group()
                            self.enemies.add(Enemies(288, 96, 0, 2))
                            self.enemies.add(Enemies(288, 320, 0, -2))
                            self.enemies.add(Enemies(544, 128, 0, 2))
                            self.enemies.add(Enemies(32, 224, 0, 2))
                            self.enemies.add(Enemies(160, 64, 2, 0))
                            self.enemies.add(Enemies(448, 64, -2, 0))
                            self.enemies.add(Enemies(640, 448, 2, 0))
                            self.enemies.add(Enemies(448, 320, 2, 0))
                            # Not game over until pacman touches enemies
                            self.game_over = False

                            # If Pacman dies, Game Over
                            self.lost = True

                        elif self.menu.state == 3:
                            # This is the exit in the menu
                            #  If the user clicked exit, then the screen will close.
                            return True

                # Again, I need to set the movement, because I will directly import this class in the main file.
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()

                elif event.key == pygame.K_LEFT:
                    self.player.move_left()

                elif event.key == pygame.K_UP:
                    self.player.move_up()

                elif event.key == pygame.K_DOWN:
                    self.player.move_down()

                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    self.lost = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()

            elif event.type == pygame.K_DOWN:
                self.player.explosion = True

        return False

    # This is the role of pacman and what happens when he enters in contact with other things.
    def pacman_role(self):
        if not self.game_over:
            self.player.update(self.horizontal_blocks, self.vertical_blocks)
            eat_dot = pygame.sprite.spritecollide(self.player, self.dots_group, True)
            # When the eat_dot contains one sprite that means that player hit a dot
            # We add 1 point in the score.
            if len(eat_dot) > 0:
                # Here, we will activate be the sound effect
                self.pacman_sound.play()
                self.score += 10
            # This is were we activate the death of the pacman, when he enters in collision with an enemy
            enemy_kill = pygame.sprite.spritecollide(self.player, self.enemies, True)
            if len(enemy_kill) > 0:
                self.player.explosion = True
                self.game_over_sound.play()
            self.game_over = self.player.game_over
            self.enemies.update(self.horizontal_blocks, self.vertical_blocks)

    def drawing_and_message(self, screen):
        # Set the screen to be black.
        screen.fill(BLACK)
        # Write this message when the player loses.
        if self.game_over:
            if self.lost:
                self.game_message(screen, "Game Over")

            else:
                self.menu.place_message(screen)
        else:
            # Draw the game here
            self.horizontal_blocks.draw(screen)
            self.vertical_blocks.draw(screen)
            create_map(screen)
            self.dots_group.draw(screen)
            self.enemies.draw(screen)
            screen.blit(self.player.image, self.player.rect)
            # Put the score on the screen and set the color (white).
            Scoreboard = self.font.render("SCORE: " + str(self.score), True, WHITE)
            # Put the text on the screen
            screen.blit(Scoreboard, [120, 20])

        # Update the screen, so that the new changes we made will appear.
        pygame.display.flip()

    def game_message(self, screen, message, color=(255, 0, 0)):
        label = self.font.render(message, True, color)
        # Get the width and height of the message (label is the term in Python that designs a message)
        width_of_label = label.get_width()
        height_of_label = label.get_height()
        # Determine the position of the message
        horizontal_position = (SCREEN_WIDTH / 2) - (width_of_label / 2)
        vertical_position = (SCREEN_HEIGHT / 2) - (height_of_label / 2)
        # Choose the location of the message
        screen.blit(label, (horizontal_position, vertical_position))


# This is the home menu class.
class Home_Menu(object):
    state = 0

    def __init__(self, items, font_color=(0, 0, 0), select_color=(255, 0, 0), ttf_font=None, font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font, font_size)

    # This part is for the details about the home menu (location of the levels, size of the writing, etc.)
    def place_message(self, screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                text_zone = self.font.render(item, True, self.select_color)
            else:
                text_zone = self.font.render(item, True, self.font_color)

            width_of_text = text_zone.get_width()
            height_of_text = text_zone.get_height()

            horizontal_position = (SCREEN_WIDTH / 2) - (width_of_text / 2)
            # This is the total height of text block
            total_height = len(self.items) * height_of_text
            vertical_position = (SCREEN_HEIGHT / 2) - (total_height / 2) + (index * height_of_text)

            screen.blit(text_zone, (horizontal_position, vertical_position))

    # In this, I choose how the player will navigate in the menu. I put the keyboard, so he can't use a mouse.
    def choose_level(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) - 1:
                    self.state += 1
