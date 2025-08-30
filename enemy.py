import pygame
import random
from constants import WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, x, y, width, height, num_frames):
        super().__init__()

        # Load the sprite sheet and scale it by 1.6
        original_sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()
        scaled_width = int(original_sprite_sheet.get_width() * 1.6)
        scaled_height = int(original_sprite_sheet.get_height() * 1.6)
        self.sprite_sheet = pygame.transform.scale(original_sprite_sheet, (scaled_width, scaled_height))

        # Set up initial properties
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.y = 0
        self.animation_frames = num_frames
        self.current_frame = 0
        self.animation_speed = 5
        self.speed = 2
        self.direction = random.choice([-1, 1])  # -1 for left, 1 for right

    def update(self):
        # Move the enemy bird horizontally
        self.rect.x += self.speed * self.direction

        # Check if the enemy bird has moved off the screen
        if self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = WIDTH

        # Update the animation frame
        self.current_frame = (self.current_frame + 1) % self.animation_frames

    def draw(self, screen):
        # Calculate the frame's position on the sprite sheet
        frame_width = self.sprite_sheet.get_width() // self.animation_frames
        frame_x = frame_width * self.current_frame

        # Extract the current frame from the sprite sheet
        frame = self.sprite_sheet.subsurface(pygame.Rect(frame_x, 0, frame_width, self.rect.height))

        # Mirror the sprite if it's moving right
        if self.direction == 1:  # Only flip if moving right
            frame = pygame.transform.flip(frame, True, False)

        # Draw the current frame on the screen
        screen.blit(frame, self.rect)



