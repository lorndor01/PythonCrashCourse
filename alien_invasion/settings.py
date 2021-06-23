class Settings:
    """A class to store all the settings for the game Alien Invasion"""

    def __init__(self):
        """Initialize the game's sfettings."""
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        self.ship_speed = 1.5
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 6

        # Alien settings
        self.alien_speed = .5
        self.fleet_drop_speed = 25
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        #Statistics
        self.ship_limit = 2

        