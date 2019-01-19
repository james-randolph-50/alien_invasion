import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from alien = Alien
import game_functions as gf

def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # Make an alien
    alien = Alien(ai_settings, screen)
    
    # Set the background color.
    bg_color = (230, 230, 230)
    
    # Make a ship, bullet, and alien fleet
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Create the fleet of aliens
    gf.create_fleet(ai_settings, screen, aliens)

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_aliens(ai_settings, aliens)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)
        gf.update_aliens(aliens)
        gf.update_bullets(aliens, bullets)

    # Remove bullets that fly off screen
    for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)

run_game()