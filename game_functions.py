import sys
from time import sleep
import pygame
from bullet import Bullet
# from ship import Ship


def check_keydown_events(event, ai_settings, screen, ship, bullets):
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            fire_bullet(ai_settings, screeen, ship, bullets)

def fire_bullet(ai_settings, screeen, ship, bullets):
            if len(bullets) < ai_settings.bullets_allowed:
                new_bullet = Bullet(ai_settings, screen, ship)
                bullets.add(new_bullet)


def check_keyup_events(event, ship):
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, ship, bullets, aliens, stats, play_button, mouse_x, mouse_y)
        
def check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, ship, screen, aliens, bullets):

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset game settings
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()

    # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

    # Create a new fleet and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def update_screen(ai_settings, screen, ship, aliens, bullets, stats, play_button):
    # Redraw the screen, each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Draw the score information.
    sb.show_score()
    
    # Redraw all bullets, behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    alien.blitme()
    aliens.draw(screen)

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)

# Create the first row of aliens
    for alien_number in range(number_aliens_x):
        # Create an alien and place it in a row
        alien = Alien(ai_settings, screen)
        create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def update_aliens(ai_settings, sb, ship, aliens, stats, screen, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # check for collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, sb, stats, screen, ship, aliens, bullets)

    # Check if aliens hit the bottom of the screen

    check_aliens_bottom(ai_settings, ship, stats, screen, aliens, bullets)

def check_fleet_edges(ai_settings, alien):
    for aliens in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settiings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
        ai_settings.fleet_direction *= -1

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.value():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

        # Empty the list of Aliens and Bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center a new ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Trea this the same as the ship getting hit.
                ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
                break

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

    # Make the most recently drawn screen visible.
    pygame.display.flip()


