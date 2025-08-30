import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, text_color, background_color, hover_color, action=None):
        # Initialize button attributes
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.background_color = background_color
        self.hover_color = hover_color
        self.action = action
        self.hovered = False

    def draw(self, surface):
        # Draw the button on the given surface
        color = self.hover_color if self.hovered else self.background_color
        # Draw button background
        pygame.draw.rect(surface, color, self.rect)
        # Draw button border
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        # Handle mouse events for the button
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and self.action:
                self.action()
