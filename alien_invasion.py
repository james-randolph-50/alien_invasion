import sys

import pygame

from settings import Settings
from ship import Ship
import game_functions as gf

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_mode((1200, 800))pygame.display.set_caption("Alien Invasion")

    # Make a ship
    ship = Ship(screen)

    # Start the main loop for the game

    while True:

        gf.check_events()

    # Redraw screen during each pass through the loop
    screen.fill(ai.settings.bg_color)
    ship.blitme()

    # Make the most recently drawn screen visible
        pygame.display.flip()
    
run_game()
