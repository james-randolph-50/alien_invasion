import sys

import pygame

from settings import Settings

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_mode((1200, 800))pygame.display.set_caption("Alien Invasion")

    bg_color = (230, 230, 230)

    # Start the main loop for the game

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    # Redraw screen during each pass through the loop
    screen.fill(ai.settings.bg_color)

    # Make the most recently drawn screen visible
        pygame.display.flip()
    
run_game()
