import json
class GameStats:
    """Track statistics for alien invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        #Start in an inactive state
        self.game_active = False
        with open(ai_game.high_score_file) as f:
            self.high_score = json.load(f)['score']


    def reset_stats(self):
        """Initialize statistics that can change during a game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

