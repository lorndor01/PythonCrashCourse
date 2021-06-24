import sys
from time import sleep
import json

import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from score_board import ScoreBoard
from sound_mixer import SoundMixer


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self, fullscreen):
        """Initialize the game and create game resources."""
        self.session_name = None
        while self.session_name == None:
            possible_name = input("Please enter a name 4 letters or less for " +
                "your session: ")
            if len(possible_name) > 4:
                print("Your name me must be 4 letters or less.")
            elif len(possible_name) < 1:
                print("Your name must be a least 1 letter long.")
            else:
                self.session_name = possible_name
        self.high_score_file = "high_score.json"
        try:
            with open(self.high_score_file, 'r') as f:
                self.high_score_holder = json.load(f)['name']
        except FileNotFoundError:
            with open(self.high_score_file, 'w') as f:
                self.high_score_holder = self.session_name
                player = {'name':self.session_name, 'score':0}
                json.dump(player, f)


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

        self.game_stats = GameStats(self)

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        

        self.play_button = Button(self, "Play")

        self.score_board = ScoreBoard(self)

        self.mixer = SoundMixer()



    def run_game(self):
        """Main loop for the game."""

        while True:
            # Watch for keyboard and mouse events.
            self._check_events()

            if self.game_stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
    
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

    def _check_play_button(self, mouse_pos):
        """Start a new game when a player clicks Play"""

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.game_stats.game_active:
            #Reset the game statistics
            self.game_stats.reset_stats()
            self.score_board.prep_score()
            self.score_board.prep_level()
            self.score_board.prep_ships()
            self.game_stats.game_active = True

            #Get rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

            #Hide the mouse curson
            pygame.mouse.set_visible(False)

            #Reset game speeds
            self.settings.initialize_dynamic_settings()


    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw()
        self.aliens.draw(self.screen)
        self.score_board.show_score()

        if not self.game_stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _fire_bullet(self):
        """Create a bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            self.mixer.play_bullet_firing()
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        #Update bullets location
        self.bullets.update()

        #Get rid of bullets that have disappearerd.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_alien_bullet_collisions()

    def _check_alien_bullet_collisions(self):
        """Check to see if any bullets hit aliens.
        If so get rid of the bullet and alien"""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            self.mixer.play_alien_hit()
            for aliens in collisions.values():
                self.game_stats.score += self.settings.alien_points * len(aliens)
            self.score_board.prep_score()
            self.score_board.check_high_score()
        #Replenish fleet if empty.
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.game_stats.level +=1
            self.score_board.prep_level()


    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        alien.x = alien_width + 2*alien_width * alien_number
        alien.rect.x = alien.x

        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _create_fleet(self):
        #Create an alien and find the number of aliens in a row.
        #Spacing between each alien is one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2*alien_width)

        #Determine the number of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
            (3*alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _update_aliens(self):
        """Update the positions of all the aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()


    def _check_fleet_edges(self):
        """Respond appropriately if the aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        #Explosion will play no matter what.
        self.mixer.play_ship_alien_collision()

        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self.score_board.prep_ships()
            self.aliens.empty()
            self.bullets.empty()

            #Create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Give the player some time to prepare
            sleep(0.5)
        else:
            self.game_stats.game_active = False

            #Load in new high-score and player name if score is higher than 
            #score currently stored.
            current_high_score = 0
            with open(self.high_score_file) as f:
                player = json.load(f)
                current_high_score = player['score']
            
            if self.game_stats.high_score > current_high_score:
                with open(self.high_score_file, 'w') as f:
                    player = {'name':self.session_name, 'score':self.game_stats.high_score}
                    json.dump(player, f)


            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat it the same as if a ship got hit
                self._ship_hit()
                break

if __name__ == '__main__':
    # Make game instance and run the game.
    alien_invasion = AlienInvasion(False)
    alien_invasion.run_game()
