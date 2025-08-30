import pygame
import random
from platformm import Platform
from Cloud import Cloud
from constants import *

def generate_random_platforms(num_platforms, width, height):
    platforms = []

    # Generate regular platforms
    for i in range(num_platforms-2):
        p_y = i * 100
        for j in range(1):
            # Add random x-coordinate to platform
            p_x = random.randint(50, width - 50)

            image_path = "platform_image.png"

            # Initialise platform instance
            return_platform = Platform(p_x, p_y, 90, 10, image_path)

            # Add platform instance into platform list
            platforms.append(return_platform)

    # Generate special platform 1 with a random position
    special_platform1 = Platform(random.randint(50, width - 50), random.randint(0, height - 30), 90, 10, 'death_platform.png', is_jumpy=False, is_death=True, is_side=False)
    platforms.append(special_platform1)

    # Generate special platform 2 with a random position
    special_platform2 = Platform(random.randint(50, width - 50), random.randint(0, height - 30), 90, 10, 'jumpy_platform.png', is_jumpy=True, is_death=False, is_side=False)
    platforms.append(special_platform2)

    special_platform3 = Platform(random.randint(50, width - 50), random.randint(0, height - 30), 90, 10,
                                 'move_side_platform.png', is_jumpy=False, is_death=False, is_side=True)
    platforms.append(special_platform3)

    return platforms


def generate_random_clouds(num_clouds, cloud_width, cloud_height):
    clouds = []
    # Generate clouds
    for i in range(num_clouds):

        # Add random x and y-coordinates to clouds
        c_x = random.randint(0, WIDTH - cloud_width)
        c_y = random.randint(0, HEIGHT - 30)

        image_path = "cloud.png"

        # initialise clouds instance
        return_cloud = Cloud(c_x, c_y, cloud_width, cloud_height, image_path)

        # Add instance to the cloud list
        clouds.append(return_cloud)

    return clouds




