import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
    """Class to model an alien ship"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #Position alien in the top left corner.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien to the right."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """Return true if alien as at edge of screen"""
        screen_rect = self.screen.get_rect()
        if((self.rect.right >= screen_rect.right) or (self.rect.left <= 0)):
            return True
        else: return False