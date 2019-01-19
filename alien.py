import pygame
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self, ai_settings, screen):
        #init the Alien and set the starting position
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
