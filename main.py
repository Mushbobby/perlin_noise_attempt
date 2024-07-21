import random
import sys
import time

import pygame
from pygame import QUIT

# BASE VARIABLES
dimensions = 400
grid = [[round(random.uniform(0, 0.7), 3) for x in range(dimensions)] for y in range(dimensions)]
cur_time = time.time()
dtime = 0
counter = 0

# PYGAME
pygame.init()
# Set up display dimensions
window_width = 800
window_height = 800
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Perlin noise')
# Calculate cell size based on window dimensions and grid dimensions
cell_size = min(window_width // dimensions, window_height // dimensions)


def new_grid():
    global grid
    grid = [[round(random.uniform(0, 1), 3) for x in range(dimensions)] for y in range(dimensions)]


def greyscale_to_rgb(grayscale_value):
    # Clamp the grayscale value to be within the [0, 1] range
    grayscale_value = max(0, min(grayscale_value, 1))

    # Convert the grayscale value to an 8-bit integer (0-255 range)
    rgb_value = int(round(grayscale_value * 255))

    # Return the RGB color as a tuple
    return rgb_value, rgb_value, rgb_value


def averaging_function(x, y, shape, radius):
    global grid
    global dimensions
    values = []

    if not isinstance(radius, int):
        print("Error: Radius must be an integer.")
        sys.exit(1)

    # Define directions based on shape and radius
    if shape == 'circle':
        directions = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx ** 2 + dy ** 2 <= radius ** 2:
                    directions.append((dx, dy))
    elif shape == 'square':
        directions = [(dx, dy) for dx in range(-radius, radius + 1) for dy in range(-radius, radius + 1)]
    else:
        raise ValueError("Shape must be 'circle' or 'square'")

    # Add the target element itself
    if 0 <= x < dimensions and 0 <= y < dimensions:
        values.append(grid[y][x])

    # Add the neighbors if they are within bounds
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < dimensions and 0 <= ny < dimensions:
            values.append(grid[ny][nx])

    # Calculate the average
    average = sum(values) / len(values)
    return average


def averaged_matrix():
    global grid
    global dimensions
    new_matrix = [[0] * dimensions for _ in range(dimensions)]

    for y in range(dimensions):
        for x in range(dimensions):
            new_matrix[y][x] = averaging_function(x, y, 'circle', 3)

    grid = new_matrix


def stats():
    global counter
    global cur_time
    global dtime
    delta_time = dtime - cur_time
    avg = counter / delta_time
    print(f"iterations: {counter}, time started: {cur_time}, program time: {dtime - cur_time}, iter/second: {avg}")


# Function to draw the grid
def draw_grid():
    for y in range(dimensions):
        for x in range(dimensions):
            color = (greyscale_to_rgb(grid[y][x]))
            pygame.draw.rect(window, color, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))


try:
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                stats()
                sys.exit()
        averaged_matrix()
        window.fill((0, 0, 0))
        draw_grid()
        pygame.display.flip()
        dtime = time.time()
        counter += 1
        new_grid()
        time.sleep(6)
        # Adjust the speed of the simulation

except KeyboardInterrupt:
    stats()
    pygame.quit()
