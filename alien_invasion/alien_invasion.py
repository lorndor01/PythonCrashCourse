import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self, fullscreen):
        """Initialize the game and create game resources."""
        pygame.init()
        self.settings = Settings()

        if fullscreen:
            #Run the game in full screen mode
            self.screen = pygame.display.set_mode(
            (0,0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
            self.settings.ship_speed = 3
        
        else: 
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()

            self.ship.update()
            self._update_bullets()

            #Make the most recently drawn screen visible.
            self._update_screen()


    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN:
                    self._handle_key_down(event)

                elif event.type == pygame.KEYUP:
                    self._handle_key_up(event)
    
    def _handle_key_down(self, event):
        """Handle key down events."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _handle_key_up(self, event):
        """Handle key up events."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw()
        pygame.display.flip()

    def _fire_bullet(self):
        """Create a bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        #Update bullets location
        self.bullets.update()
        
        #Get rid of bullets that have disappearerd.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

if __name__ == '__main__':
    # Make game instance and run the game.
    alien_invasion = AlienInvasion(False)
    alien_invasion.run_game()
