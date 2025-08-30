import pygame
import random
from constants import *

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()

        # Load the cloud image
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (width, height))

        # Create a rect object for positioning
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Set the initial direction of the cloud movement randomly
        self.direction = random.choice([-1, 1])  # Randomly choose -1 (left) or 1 (right)
        self.speed = 1

        # Initialize the timing attribute with a random value
        self.timing = random.randint(300, 499)

    def update(self):
        # Move the cloud horizontally
        self.timing += 1  # Increment the timing for each frame
        self.rect.x += self.direction * self.speed

        # Check if the cloud has moved off the right edge
        if self.rect.right < 0:
            self.rect.left = WIDTH  # Wrap around to the right edge

        # Check if the cloud has moved off the left edge
        elif self.rect.left > WIDTH:
            self.rect.right = 0  # Wrap around to the left edge

        # Reset timing and change direction after a longer period
        if self.timing % 500 == 0:
            self.direction *= -1
            self.timing = 0  # Reset timing when direction changes

    def draw(self, screen):
        # Draw the cloud on the screen
        screen.blit(self.image, (self.rect.x, self.rect.y))


