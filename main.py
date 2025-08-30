# Import necessary libraries
import pygame  # Pygame library for game development
import socket  # Socket library for networking
import pickle  # Pickle library for object serialization


# Import respective classes and functions from other .py files
from constants import WIDTH, HEIGHT, FPS, WHITE, BLACK, BLUE  # Importing game constants
from player import Player  # Importing the Player class
from platform_manager import PlatformManager  # Importing the PlatformManager class
from floor import Floor  # Importing the Floor class
from game_objects import generate_random_platforms, generate_random_clouds  # Importing functions to generate random platforms and clouds
from enemy import Enemy  # Importing the Enemy class
from button import Button  # Importing the Button class
from options_menu import OptionsMenu  # Importing the OptionsMenu class


# Initialize the font module and create a font
pygame.font.init()
your_font = pygame.font.Font(None, 36)  # Creates the font and size


# Function to start single player game loop
def single_player_game_loop():

    # Initialise pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Set up the game window
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('Single Player Game')

    # Create a floor object at the bottom of the screen
    floor = Floor(WIDTH, 10, BLACK)

    # Generate a list of random platforms
    num_platforms = 8
    platforms = generate_random_platforms(num_platforms, WIDTH, HEIGHT)

    # Generate a list of random clouds
    num_clouds = 5
    clouds = generate_random_clouds(num_clouds, 60, 60)

    options_menu = OptionsMenu(screen)

    # Set up the player character
    initial_controls = options_menu.get_controls()

    player_start_x = WIDTH // 2
    player = Player(player_start_x, floor.rect.y - 50, 30, 30, 'img.png', initial_controls)

    # Create a platform manager to handle platform movement
    platform_manager = PlatformManager(platforms, 1, 50)

    # Initialize variables for bird enemy
    bird_spawned = False
    enemy = Enemy('bird.png', 0, HEIGHT - 50, 50, 50, num_frames=9)

    exit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, "Exit to Menu", your_font, BLACK, WHITE, BLUE, main)

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BLUE)

        # Draw the floor
        floor.draw(screen)

        # Move all the platforms in the platform list
        platform_manager.move()

        # Draw the clouds in the cloud list onto the screen, updating there position
        for cloud in clouds:
            cloud.update()
            cloud.draw(screen)

        # Draw all the platforms in the platform list onto the screen
        platform_manager.draw(screen)

        # Update initial controls with new controls
        player.update_controls(initial_controls)

        # Handle player controls, movement, and drawing, Also handles creating new platforms, clouds and enemies
        player.handle_controls(3)
        player.move(3, platforms, floor, clouds, enemy)

        # Update the floor's position based on the player's movement
        player.update_floor_position(floor)

        # Draw the player on the screen
        player.draw(screen)

        # Display the score if the game is not over
        player.display_score(screen)

        # Check for collisions between the player and the bird
        if pygame.sprite.collide_rect(player, enemy):
            player.game_over = True  # Set game over if player collides with the bird

        # Check if the score is 20 and spawn the bird for increased difficulty, creates instance of bird
        if player.score == 20 and not bird_spawned:
            bird_spawned = True # Bird has spawned
            enemy = Enemy('bird.png', 0, HEIGHT - 50, 50, 50, num_frames=9)

        # If bird is spawned, update and draw it
        if bird_spawned:
            enemy.update()
            enemy.draw(screen)

        # If game over, display "Game Over" and the score
        if player.game_over:
            screen.fill(BLUE)
            game_over_text = your_font.render("Game Over", True, WHITE)
            score_text = your_font.render(f"Score: {player.score}", True, WHITE)
            replay = your_font.render("Press Space to Play Again", True, WHITE)
            exit_button.draw(screen)  # Draw the exit button
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height() // 2 + 10))
            screen.blit(replay, (WIDTH // 2 - replay.get_width() // 2, HEIGHT // 2 + replay.get_height() // 2 + 40))

        # Event handling, player can quit the game or press space to play the game again
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and options_menu.selected_setting is not None:
                # Change the setting with the newly pressed key
                options_menu.change_setting(event.key)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Reset the game if space is pressed and the game is over
                if player.game_over:
                    # Reset the game state
                    floor.rect.y = HEIGHT - 10  # Reset the floor position
                    player.reset_game(floor, enemy)  # Reset the player's position and score
                    player.rect.x = WIDTH // 2
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.rect.collidepoint(event.pos):
                    main()  # Return to main menu if the exit button is clicked

        pygame.display.flip()

    pygame.quit()


def multiplayer_game_loop():

    # Initialise pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Set up the game window
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('Multiplayer Game')

    # Set up the socket for multiplayer
    SERVER_HOST = socket.gethostbyname(socket.gethostname())  # Get the IP address of the server
    SERVER_PORT = 1237  # Define the port for communication
    BUFFER_SIZE = 1024  # Define the buffer size for receiving data

    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    client_socket.connect((SERVER_HOST, SERVER_PORT))  # Connect to the server using the IP address and port

    # Create a floor object at the bottom of the screen
    floor = Floor(WIDTH, 10, BLACK)

    # Generate a list of random platforms
    num_platforms = 8
    platforms = generate_random_platforms(num_platforms, WIDTH, HEIGHT)

    # Generate a list of random clouds
    num_clouds = 5
    clouds = generate_random_clouds(num_clouds, 60, 60)

    options_menu = OptionsMenu(screen)

    # Set up the player character
    initial_controls = options_menu.get_controls()

    # Set up the player one and player two characters
    player_start_x = WIDTH // 2
    player1 = Player(player_start_x, floor.rect.y - 50, 30, 30, 'img.png', initial_controls)
    player2 = Player(player_start_x + 50, floor.rect.y - 50, 30, 30, 'player2.png', initial_controls)

    # Create a platform manager to handle platform movement
    platform_manager = PlatformManager(platforms, 1, 50)

    # Initialize variables for bird enemy
    bird_spawned = False
    enemy = Enemy('bird.png', 0, HEIGHT - 50, 50, 50, num_frames=9)

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BLUE)

        # Draw the floor
        floor.draw(screen)

        platform_manager.move()

        # Draw the clouds
        for cloud in clouds:
            cloud.update()
            cloud.draw(screen)

        # Draw moving platforms from platform list onto screen
        platform_manager.draw(screen)

        # Handle player one controls, movement, and drawing
        player1.handle_controls(3)

        # Handles creating new platforms, clouds and enemies, for player one and two
        player1.move(3, platforms, floor, clouds, enemy)
        player2.move(3, platforms, floor, clouds, enemy)

        # Update the floor's position based on the player's movement for player one and two
        player1.update_floor_position(floor)
        player2.update_floor_position(floor)

        # Draw the players on the screen
        player1.draw(screen)
        player2.draw(screen)

        # Display the score if the game is not over for player one
        player1.display_score(screen)

        # Create a nested dictionary combining player movement data and platform positions
        data_to_send = {
            'player1_movement': player1.get_movement_data(),
            'platform_positions': {index: (platform.rect.x, platform.rect.y) for index, platform in enumerate(platforms)}
        }

        # Serialize the nested dictionary
        data_to_send_serialized = pickle.dumps(data_to_send)  # Convert the nested dictionary into a byte stream

        # Send data to the server
        try:
            client_socket.send(data_to_send_serialized)  # Send the serialized data to the server
        except socket.error as e:
            print(f"Error sending data to the server: {e}")  # Print an error message if sending fails
            break  # Exit the loop if there's an error with the socket

        # Check for collisions between the player and the bird
        if pygame.sprite.collide_rect(player1, enemy) or pygame.sprite.collide_rect(player2, enemy):
            player1.game_over = True  # Set game over if player1 collides with the bird
            player2.game_over = True  # Set game over if player2 collides with the bird



        # Receive data from the server
        try:
            # Attempt to receive data from the server
            received_data_serialized = client_socket.recv(BUFFER_SIZE)

            # Check if data is received
            if received_data_serialized:
                # Deserialize the received data
                received_data = pickle.loads(received_data_serialized)

                # Check if valid data is received
                if received_data:
                    # Extract player2 movement data and platform positions
                    player2_movement = received_data.get('player1_movement')
                    platform_positions = received_data.get('platform_positions')

                    # Update player2's position based on received movement data
                    if player2_movement is not None:
                        if 'x' in player2_movement:
                            player2.rect.x = player2_movement['x']
                        if 'y' in player2_movement:
                            player2.rect.y = player2_movement['y']

                    # Update platforms based on received positions
                    if platform_positions is not None:
                        for index, position in platform_positions.items():
                            platforms[index].rect.x, platforms[index].rect.y = position
            else:
                print("No data received from the server.")
        except socket.error as e:
            # Handle socket error
            print(f"Error receiving data from the server: {e}")
            break  # Exit the loop if there's an error with the socket

        # Check if the score is 20 and spawn the bird
        if player1.score == 20 and not bird_spawned:
            bird_spawned = True
            enemy = Enemy('bird.png', 0, HEIGHT - 50, 50, 50, num_frames=9)

        # If bird is spawned, update and draw it
        if bird_spawned:
            enemy.update()
            enemy.draw(screen)

        # If game over, display "Game Over" and the score
        if player1.game_over:
            screen.fill(BLUE)
            game_over_text = your_font.render("Game Over", True, WHITE)
            score_text = your_font.render(f"Score: {player1.score}", True, WHITE)
            replay = your_font.render("Press Space to Play Again", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height() // 2 + 10))
            screen.blit(replay, (WIDTH // 2 - replay.get_width() // 2, HEIGHT // 2 + replay.get_height() // 2 + 40))

        # Event handling for quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        pygame.display.flip()

    # Close the client socket when the game loop exits
    client_socket.close()
    pygame.quit()


def open_options():
    # Initialize pygame
    pygame.init()

    # Set up the game window
    options_screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('Options')

    # Set up fonts
    title_font = pygame.font.Font(None, 48)
    option_font = pygame.font.Font(None, 36)

    # Create an instance of OptionsMenu
    options_menu = OptionsMenu(options_screen)

    # Options menu loop
    running = True
    while running:

        # Render title
        title_text = title_font.render("Options", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
        options_screen.blit(title_text, title_rect)

        # Draw buttons for key binds
        options_menu.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game if the window close button is clicked
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse click events
                options_menu.handle_click(event.pos)



            elif event.type == pygame.KEYDOWN and options_menu.selected_setting is not None:
                # Change the setting with the newly pressed key
                options_menu.change_setting(event.key)
            elif options_menu.should_return_to_menu:
                return  # Exit the options menu loop and return to the main menu



        pygame.display.flip()

    pygame.quit()


# Function to create and manage the menu
def menu(screen):

    # Initialize the mixer module for handling audio
    pygame.mixer.init()

    # Create buttons for single player, multiplayer, and options
    single_player_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, "Single Player", your_font, BLACK, WHITE, BLUE, single_player_game_loop)
    multiplayer_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 50, "Multiplayer", your_font, BLACK, WHITE, BLUE, multiplayer_game_loop)
    options_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50, "Options", your_font, BLACK, WHITE, BLUE, open_options)

    buttons = [single_player_button, multiplayer_button, options_button]

    # Load background music
    pygame.mixer.music.load('background_music.wav')
    # Set background music volume
    pygame.mixer.music.set_volume(0.1)  # Adjust the volume as needed
    # Play background music
    pygame.mixer.music.play(-1)  # '-1' loops the music indefinitely

    # Load background image for menu background
    background_image = pygame.image.load('background.png').convert()

    running = True
    while running:
        # Fills screen with blue colour
        screen.fill(BLUE)

        # Event handling loop
        for event in pygame.event.get():
            # Quit the game if the window close button is clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            for button in buttons:
                # Handle events for each button
                button.handle_event(event)

        # Draw the background image
        screen.blit(background_image, (0, 0))

        # Draw each button on the screen
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()


# Main function to run the game
def main():
    # Initialize pygame
    pygame.init()

    # Set up the game window
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('NEA Project')

    # Call the menu function to start the main menu loop
    menu(screen)

    pygame.quit()


if __name__ == "__main__":
    main()
