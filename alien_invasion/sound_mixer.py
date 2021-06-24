from pygame.mixer import Sound
class SoundMixer:
    """Class to handle Alien Invasion sound effects"""

    def __init__(self):
        """initialize all the sound effect Sounds"""
        self.explosion_sound = Sound("SoundEffects/ship_alien_collision.wav")
        self.bullet_firing_sound = Sound("SoundEffects/bullet_firing.wav")
        self.alien_hit = Sound("SoundEffects/alien_hit.wav")

        #Adjust sound effect volumes.
        self.bullet_firing_sound.set_volume(.1)
        self.alien_hit.set_volume(.1)

    def play_ship_alien_collision(self):
        self.explosion_sound.play()

    def play_bullet_firing(self):
        self.bullet_firing_sound.play()

    def play_alien_hit(self):
        self.alien_hit.play()