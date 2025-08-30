import pygame
from button import Button
from slider import Slider  # Import the Slider class
from constants import *

class OptionsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.settings = {'left_key': pygame.K_LEFT, 'right_key': pygame.K_RIGHT, 'jump_key': pygame.K_UP}
        self.selected_setting = None
        self.should_return_to_menu = False
        self.buttons = []
        self.create_buttons()
        self.slider = Slider(WIDTH // 2 - 100, HEIGHT // 1.5, 200, 20, 0, 100, 50, BLACK, BLUE, 10)  # Create a slider for volume control

    def create_buttons(self):
        y_offset = 100
        for setting_name, setting_key in self.settings.items():
            button_text = f"{setting_name}: {pygame.key.name(setting_key)}"
            button = Button(WIDTH // 2 - 150, y_offset, 300, 50, button_text, self.font, BLACK, WHITE, BLUE)
            self.buttons.append(button)
            y_offset += 70

        # Create the "Back" button with the back_to_menu action
        back_button = Button(WIDTH // 2 - 100, HEIGHT - 100, 200, 50, "Back", self.font, BLACK, WHITE, BLUE, action=self.back_to_menu)
        self.buttons.append(back_button)

    def select_setting(self, setting_name):
        # Update the selected setting
        self.selected_setting = setting_name

    def change_setting(self, new_key):
        # Change the key binding for the selected setting
        if self.selected_setting:
            self.settings[self.selected_setting] = new_key
            # Update the button text to reflect the new key binding
            for button in self.buttons:
                if button.text.startswith(self.selected_setting):
                    button.text = f"{self.selected_setting}: {pygame.key.name(new_key)}"
                    break
            self.selected_setting = None

    def draw(self):
        self.screen.fill(BLUE)
        sound_text = self.font.render("Sound:", True, BLACK)
        sound_text_rect = sound_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5 - 50))
        self.screen.blit(sound_text, sound_text_rect)


        for button in self.buttons:
            button.draw(self.screen)
        self.slider.draw(self.screen)  # Draw the slider
        pygame.display.flip()

    def get_clicked_setting(self, pos):
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                # Extract the setting name from the button text
                setting_name = button.text.split(":")[0].strip()
                return setting_name

        return None

    def handle_click(self, pos):
        # Get the clicked setting name
        setting_name = self.get_clicked_setting(pos)
        if setting_name:
            self.select_setting(setting_name)

        # Check if the click is on the "Back" button
        for button in self.buttons:
            if button.text == "Back" and button.rect.collidepoint(pos):
                button.action()  # Execute the action associated with the "Back" button
                break

    def handle_events(self):
        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and self.selected_setting is not None:
                self.change_setting(event.key)
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     self.slider.handle_event(event)  # Handle slider events
            # elif event.type == pygame.MOUSEMOTION:  # Add this condition to handle slider drag
            #     self.slider.handle_event(event)  # Handle slider drag

    def back_to_menu(self):
        # Return to main menu
        self.should_return_to_menu = True

    def get_controls(self):
        # Return the current controls dictionary
        return self.settings

    def get_volume(self):
        # Return the current volume value
        return self.slider.value / 100


