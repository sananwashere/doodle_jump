# floor.py

import pygame
from constants import HEIGHT, BLACK

class Floor:
    def __init__(self, width, height, color):
        # Initialise the floor with a rectangle representing the ground
        self.rect = pygame.Rect(0, HEIGHT - height, width, height)
        self.color = color

    # Draw the floor on the screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

