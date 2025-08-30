# player.py
import random
import pygame
from constants import *

class Player:
    def __init__(self, x, y, width, height, image_path, initial_controls):
        # Initialise player properties
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, height))

        # Initialise gravity, collision and jump variables

        self.vertical_speed = 0
        self.gravity = 0.5
        self.on_ground = False

        # Initialise variables to change y co-ordinate of objects

        self.scroll = 0
        self.plat_y = 0
        self.cloud_y = 0
        self.enemy_y = 0
        self.score = 0

        # Game variables

        self.game_over = False
        self.game_over_time = 0

        # Store initial control settings

        self.controls = initial_controls

        # Initialise small and big fonts

        self.small_font = pygame.font.SysFont('Lucida Sans', 20)
        self.big_font = pygame.font.SysFont('Lucida Sans', 30)

    # Update controls with new player key binds
    def update_controls(self, new_controls):
        self.controls = new_controls

    # Handle player controls for movement and jumping
    def handle_controls(self, speed):
        keys = pygame.key.get_pressed()

        # Move left or right based on key presses
        if keys[self.controls['left_key']] or keys[self.controls['right_key']]:
            self.rect.x += (keys[self.controls['right_key']] - keys[self.controls['left_key']]) * speed

            # Wrap around the screen
            if self.rect.left > WIDTH:
                self.rect.right = 0
            elif self.rect.right < 0:
                self.rect.left = WIDTH

        # Jump if the jump key is pressed
        if keys[self.controls['jump_key']]:
            self.jump()

    # Move the player vertically and check for collisions with platforms
    def move(self, speed, platforms, floor, clouds, enemy):

        # adding gravity makes it fall down
        self.vertical_speed += self.gravity

        # adds speed + scroll to player
        # self.rect.y += self.vertical_speed

        # Limits falling speed at 9
        if self.vertical_speed > 8:
            self.vertical_speed = 8

        # Check for collisions with platforms
        self.check_platform_collision(platforms)

        # Moves the platforms downwards to create the scrolling screen illusion
        self.move_platforms_down(platforms, clouds, enemy)

        # Create new platforms when current platforms move below the screen
        self.create_new_platforms(platforms)

        # Check if player has lost the game
        self.player_lose(platforms)

        # Create new clouds when current clouds move below the screen
        self.create_new_clouds(clouds)

        # Create new enemy when the current enemy moves below the screen
        self.create_new_enemy(enemy)

        # Restrict player to the bottom of the screen
        if self.rect.colliderect(floor.rect) and self.rect.bottom >= floor.rect.top:
            self.rect.y = floor.rect.top - self.rect.height
            self.on_ground = True
            self.vertical_speed = 0
        else:
            self.on_ground = False

    # Make the player jump
    def jump(self):
        if self.on_ground:  # Only jump if on the ground
            self.vertical_speed = -17
            self.on_ground = False

    # Check for collisions with all platforms and adjust player position
    def check_platform_collision(self, platforms):
        keys = pygame.key.get_pressed()
        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):

                if self.rect.bottom >= platform.rect.top:

                    if self.vertical_speed >= 0:
                        self.rect.y = platform.rect.y - self.rect.height
                        self.on_ground = True

                        # Check if the platform is jumpy
                        if platform.is_jumpy:
                            # Adjust the jump power for jumpy platforms
                            self.vertical_speed = -20
                            if self.score > 50:
                                self.vertical_speed = -17

                        # Check if platform is death
                        elif platform.is_death:
                            # Move the death platform down
                            platform.rect.y += 1

                            # Checks if score is over 50 and 100 if condition is met difficulty increases
                            if self.score > 50:
                                platform.rect.y += 2
                            elif self.score > 100:
                                platform.rect.y += 3

                        # Check if platform is side
                        elif platform.is_side:
                            # Move platform to side
                            platform.rect.x += 1
                        else:
                            self.vertical_speed = 0

                    # Jump if on platform
                    if keys[pygame.K_UP]:
                        self.jump()

    def move_platforms_down(self, platforms, clouds, enemy):
        # if player is past the threshold
        if self.rect.top <= SCROLL_THRESH:

            # Only occurs when player is jumping upwards -> prevents downwards interaction
            if self.vertical_speed < 0:
                # Scroll is equal to the distance jumped (negatively)
                self.scroll = -self.vertical_speed

                for platform in platforms:
                    platform.rect.y += self.scroll

                for cloud in clouds:
                    cloud.rect.y += self.scroll / 2
                enemy.rect.y += self.scroll

        # This updates player's y position using vertical speed and the scroll
        self.rect.y += self.vertical_speed + self.scroll

    #     # Check if the platform is below the screen after updating player's position
    # def create_new_platforms(self, platforms):
    #     if self.rect.top <= SCROLL_THRESH:
    #         for platform in platforms:
    #             if platform.rect.top >= HEIGHT:
    #                 platform.rect.y = random.randint(-90,-10)

    # Check if the platform is below the screen after updating player's position
    def create_new_platforms(self, platforms):
        for index, platform in enumerate(platforms):

            if platform.rect.top >= HEIGHT:
                self.plat_y += index * -1
                if self.plat_y < -600:
                    self.plat_y = -600

                # Check if the platform is jumpy and adjust its x-coordinate
                if platform.is_jumpy:
                    platform.rect.x = random.randint(50, WIDTH - 50)

                # Respawn the platform at the top with a new random y-coordinate
                platform.rect.y = self.plat_y
                self.score += 1

            if self.score > 150:
                pass

    # Check if clouds is below the screen after updating cloud position
    def create_new_clouds(self, clouds):
        for index, cloud in enumerate(clouds):

            if cloud.rect.top >= HEIGHT:
                self.cloud_y += index * -1

                if self.cloud_y < -500:
                    self.cloud_y = -500

                # Respawn cloud at the top with new random y-coordinate
                cloud.rect.y = self.cloud_y

    # Check if enemy is below the screen after updating enemy position
    def create_new_enemy(self, enemy):

        if enemy.rect.top >= HEIGHT:
            self.enemy_y += -5

            if self.enemy_y < -500:
                self.enemy_y = -500

                # Respawn enemy at the top with new random y coordinate
                enemy.rect.y = self.enemy_y

    # Check if player is below the screen and game is not over
    def player_lose(self, platforms):

        if self.rect.y > HEIGHT and not self.game_over:
            # Check if player is falling
            if self.vertical_speed > 0:

               self.scroll = self.vertical_speed
               self.game_over = True



    # Display the score at the top left of the screen
    def display_score(self, screen):
        score_text = self.big_font.render(f"Score: {self.score}", True, (BLACK))  # Create a text surface
        screen.blit(score_text, (10, 10))  # Draw the text surface on the screen

    # Edits floor y co-ord just like a platform
    def update_floor_position(self, floor):
        floor.rect.y += self.scroll

    # Draw the player on the screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # Reset game variables when space bar is pressed
    def reset_game(self,floor, enemy):
        # Reset player properties for a new game
        self.rect.y = floor.rect.y - 50
        self.vertical_speed = 0
        self.on_ground = False
        self.scroll = 0
        self.plat_y = 0
        self.score = 0
        self.game_over = False
        self.game_over_time = 0
        enemy.rect.y = 0

    # Create a dictionary of the players x and y position to be sent to the server
    def get_movement_data(self):
        return {
            'x': self.rect.x,
            'y': self.rect.y,

        }




