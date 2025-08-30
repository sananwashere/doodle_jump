import pygame

class Slider:
    def __init__(self, x, y, length, height, min_value, max_value, default_value, color, handle_color, handle_radius):
        # Initialize slider attributes
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = default_value
        self.color = color
        self.handle_color = handle_color
        self.handle_radius = handle_radius

        # Create rects for slider track and handle
        self.rect = pygame.Rect(self.x, self.y - self.height // 2, self.length, self.height)
        self.handle_rect = pygame.Rect(self.x + (self.length * (self.value - self.min_value) // (self.max_value - self.min_value)) - self.handle_radius, self.y - self.handle_radius, 2 * self.handle_radius, 2 * self.handle_radius)
        # Flag to indicate if the handle is being dragged
        self.dragging = False

    def draw(self, screen):
        # Draw slider track
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.height // 2)

        # Draw gradient overlay
        gradient_rect = pygame.Rect(self.rect)
        gradient_rect.width = self.handle_rect.centerx - self.rect.x
        gradient = pygame.Surface((gradient_rect.width, gradient_rect.height), pygame.SRCALPHA)
        gradient.fill((0, 0, 0, 0))
        pygame.draw.rect(gradient, (255, 255, 255, 100), gradient.get_rect(), border_radius=self.height // 2)
        screen.blit(gradient, gradient_rect)

        # Draw handle
        pygame.draw.circle(screen, self.handle_color, self.handle_rect.center, self.handle_radius)

    def update(self):
        # Update handle position based on current value
        self.handle_rect.centerx = self.x + (self.length * (self.value - self.min_value) // (self.max_value - self.min_value))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check if mouse click is on the handle
                if self.handle_rect.collidepoint(event.pos):
                    self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False  # Stop dragging when mouse button released
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Update value based on mouse position
                mouse_x = event.pos[0]
                new_value = self.min_value + (mouse_x - self.x) * (self.max_value - self.min_value) // self.length
                # Ensure new value stays within bounds
                if new_value < self.min_value:
                    self.value = self.min_value
                elif new_value > self.max_value:
                    self.value = self.max_value
                else:
                    self.value = new_value
                # Update handle position
                self.update()
