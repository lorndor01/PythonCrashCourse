import pygame
class Ship:
    """A class to model the player's ship"""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        #Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #Start each new ship at bottom center of the screen.
        self.rect.midbottom =self.screen_rect.midbottom

        # Movement flags
        self.moving_left = False
        self.moving_right = False

        # Keep tracking of positions that are fractions of pixels.
        self.x = float(self.rect.x)


    def update(self):
        """Update the ship's position based on movement flags."""
        if (self.moving_right == True) and (self.rect.right < self.screen_rect.right):
            self.x += self.settings.ship_speed
        if self.moving_left == True and (self.rect.left >0):
            self.x -= self.settings.ship_speed

        #Update ship's rect position.
        self.rect.x = self.x

    def center_ship(self):
        """Centers the ship at the bottom of the game window"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the ship at its current position."""
        self.screen.blit(self.image, self.rect)