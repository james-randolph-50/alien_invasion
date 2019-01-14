import pygame

class Ship():

        def __init__(self, screen):
            self.screen = screen

            # Load the ship image
            self.image = pygame.image.load('images/ship.bmp')
            self.rect = self.image.get_rect()
            self.screen_rect = screen.get_rect()

            