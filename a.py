# random red,green,blue values for perlin noise
# I don't know its 3 dimensions which will be a pain to come up with an efficient algorithm,
# but you got this

import random
import sys
import time

import pygame
from pygame import QUIT

# BASE VARIABLES
dimensions = 100
grid = [[[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for x in range(dimensions)] for y in
        range(dimensions)]
cur_time = time.time()
change_in_time = 0
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
    grid = [[[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for x in range(dimensions)] for y
            in range(dimensions)]


def averaging_function(y, x, shape, radius):
    global grid
    global dimensions
    r = []
    g = []
    b = []

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
        r.append(grid[y][x][0])
        g.append(grid[y][x][1])
        b.append(grid[y][x][2])

    # Add the neighbors if they are within bounds
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < dimensions and 0 <= ny < dimensions:
            r.append(grid[ny][nx][0])
            g.append(grid[ny][nx][1])
            b.append(grid[ny][nx][2])

    # Calculate the average
    ra = sum(r) / len(r)
    ga = sum(g) / len(g)
    ba = sum(b) / len(b)
    return int(ra), int(ga), int(ba)


def averaged_matrix():
    global grid
    global dimensions
    new_matrix = [[[0, 0, 0]] * dimensions for _ in range(dimensions)]

    for i in range(dimensions):
        for j in range(dimensions):
            new_matrix[i][j] = averaging_function(i, j, 'circle', 3)
    grid = new_matrix


def stats():
    global counter
    global cur_time
    global change_in_time
    delta_time = change_in_time - cur_time
    avg = counter / delta_time
    print(f"iterations: {counter}, time started: {cur_time}, program time: {delta_time}, iter/second: {avg}")


# Function to draw the grid
def draw_grid():
    for y in range(dimensions):
        for x in range(dimensions):
            colour = grid[y][x]
            pygame.draw.rect(window, colour, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))


try:
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                stats()
                sys.exit()
        window.fill((0, 0, 0))
        draw_grid()
        pygame.display.flip()
        averaged_matrix()
        change_in_time = time.time()
        counter += 1
        # new_grid()
        #time.sleep(3)

except KeyboardInterrupt:
    stats()
    pygame.quit()
