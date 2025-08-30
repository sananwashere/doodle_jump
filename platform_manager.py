# platform_manager.py

# Import random library
import random

# Platform Manager Class
class PlatformManager:
    def __init__(self, platforms, speed, distance):
        # Initialize the PlatformManager with a list of platforms, speed, and movement distance
        self.platforms = platforms
        self.speed = speed
        self.distance = distance

        # Assign random directions to each platform
        for platform in self.platforms:
            platform.direction = random.choice([-1, 1])

    # Move all platforms managed by the PlatformManager
    def move(self):
        for platform in self.platforms:
            platform.move(self.speed, self.distance)

    # Draw all platforms managed by the PlatformManager on the screen
    def draw(self, screen):
        for platform in self.platforms:
            platform.draw(screen)

    # Reset the positions of all platforms
    def reset_platforms(self):
        self.platforms = []
        self.speed = 0
        self.distance = 0



