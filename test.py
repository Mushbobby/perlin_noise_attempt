import random
import sys
import time

import pygame
from pygame import QUIT, KEYDOWN, K_UP, K_DOWN

# Constants
DIMENSIONS = 1000
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
INITIAL_CELL_SIZE = 1
UPDATE_INTERVAL = 0.1  # Seconds

# Global Variables
grid = [[round(random.uniform(0, 1), 3) for _ in range(DIMENSIONS)] for _ in range(DIMENSIONS)]
cell_size = INITIAL_CELL_SIZE
counter = 0
cur_time = time.time()

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Perlin noise')


def new_grid():
    global grid
    grid = [[round(random.uniform(0, 1), 3) for _ in range(DIMENSIONS)] for _ in range(DIMENSIONS)]


def greyscale_to_rgb(grayscale_value):
    grayscale_value = max(0, min(grayscale_value, 1))
    rgb_value = int(round(grayscale_value * 255))
    return rgb_value, rgb_value, rgb_value


def averaging_function(x, y, shape, radius):
    values = []

    if shape == 'circle':
        directions = [(dx, dy) for dx in range(-radius, radius + 1) for dy in range(-radius, radius + 1) if
                      dx ** 2 + dy ** 2 <= radius ** 2]
    elif shape == 'square':
        directions = [(dx, dy) for dx in range(-radius, radius + 1) for dy in range(-radius, radius + 1)]
    else:
        raise ValueError("Shape must be 'circle' or 'square'")

    if 0 <= x < DIMENSIONS and 0 <= y < DIMENSIONS:
        values.append(grid[y][x])

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < DIMENSIONS and 0 <= ny < DIMENSIONS:
            values.append(grid[ny][nx])

    average = sum(values) / len(values)
    return average


def averaged_matrix():
    global grid
    new_matrix = [[0] * DIMENSIONS for _ in range(DIMENSIONS)]

    for y in range(DIMENSIONS):
        for x in range(DIMENSIONS):
            new_matrix[y][x] = averaging_function(x, y, 'circle', 4)

    grid = new_matrix


def stats():
    global counter, cur_time
    delta_time = time.time() - cur_time
    avg = counter / delta_time
    print(f"iterations: {counter}, program time: {delta_time}, iter/second: {avg:.2f}")


def draw_grid():
    global cell_size
    for y in range(DIMENSIONS):
        for x in range(DIMENSIONS):
            color = greyscale_to_rgb(grid[y][x])
            pygame.draw.rect(window, color, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))


# Main Loop
try:
    last_update_time = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                stats()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    cell_size += 1  # Zoom in
                elif event.key == K_DOWN:
                    cell_size = max(1, cell_size - 1)  # Zoom out (ensure cell_size doesn't go below 1)

        if time.time() - last_update_time > UPDATE_INTERVAL:
            # averaged_matrix()
            last_update_time = time.time()

        window.fill((0, 0, 0))
        draw_grid()
        pygame.display.flip()

        counter += 1
        new_grid()  # Uncomment if you want to regenerate the grid periodically

except KeyboardInterrupt:
    stats()
    pygame.quit()
