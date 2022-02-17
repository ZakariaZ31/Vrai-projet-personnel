# I need to import everything in pygame and also the Game class.
import pygame
from game import Game

# Once again, we put a value to the height and width of the screen.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576


# I created this function, which will import everything necessary and initialize it.
def main():
    # Initialize all imported pygame modules
    pygame.init()
    # This is where we activate the width and the height of the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    # This will be the name of the game window.
    pygame.display.set_caption("PACMAN ZAKARIA")
    # Activate a loop that keep the window opened until the player clicks the quit button.
    done = False
    # The clock is used for the movement of the ghosts and the pacman
    clock = pygame.time.Clock()
    # Create a game object
    game = Game()
    # Now this is the main program loop, which will activate the whole game, levels, etc.
    while not done:
        # This means that when 'done' isn't activated, the gameplay, messages, clock, etc. will still run.
        done = game.gameplay()
        game.pacman_role()
        game.drawing_and_message(screen)
        clock.tick(30)
    # When the player close the window, he can quit.
    pygame.quit()

# This will open the game screen when we run the main file.
if __name__ == '__main__':
    main()
