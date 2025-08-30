import pygame
import random
from constants import *
# platform.py

class Platform:
    def __init__(self, x, y, width, height, image_path, is_jumpy=False, is_death=False, is_side=False):
        # Initialize platform properties
        self.rect = pygame.Rect(x, y, width, height)
        self.start_x = x
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (width, height+10))
        self.direction = 1
        self.timing = 0

        # Generate a random time interval
        self.random_time_interval = random.randint(200, 300)

        # New attribute to determine if the platform is a jumpy platform, death platform, side platform
        self.is_jumpy = is_jumpy
        self.is_death = is_death
        self.is_side = is_side

    # Move the platform horizontally with a given speed and distance
    def move(self, speed, distance):
        self.timing += 1  # Increment the timing for each frame
        self.rect.x += speed * self.direction

        # Wrap around when the platform moves beyond the screen boundaries
        if self.rect.right < 0:
            self.rect.x = WIDTH
        elif self.rect.left > WIDTH:
            self.rect.x = -self.rect.width

        # Reverse direction after a certain period of time
        if self.timing % self.random_time_interval == 0:
            self.direction *= -1
            self.timing = 0  # Reset timing when direction changes

    # Draw the platform using the loaded image
    def draw(self, screen):
        screen.blit(self.image, self.rect)
