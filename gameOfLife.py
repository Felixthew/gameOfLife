import pygame
import sys
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the window dimensions and cell size
width, height = 800, 800
cell_size = 10
rows = height // cell_size
cols = width // cell_size

# Set up the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game of Life")

# Define colors
bg_color = (0, 0, 0)  # Black background
grid_color = (40, 40, 40)  # Gray grid
alive_color = (255, 255, 255)  # White for alive cells

# Initialize the grid with random values
grid = np.random.randint(2, size=(rows, cols))

def draw_cell(x, y, state):
    """Draw or erase a cell at the given (x, y) coordinates."""
    color = alive_color if state == 1 else bg_color
    rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, grid_color, rect, 1)  # Draw grid line around the cell

def update_grid(grid):
    """Update the grid based on Conway's Game of Life rules and track changed cells."""
    new_grid = np.copy(grid)
    changes = []

    for x in range(rows):
        for y in range(cols):
            # Count the number of alive neighbors
            neighbors = np.sum(grid[max(0, x-1):min(x+2, rows), max(0, y-1):min(y+2, cols)]) - grid[x, y]

            # Apply the rules of the Game of Life
            if grid[x][y] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[x][y] = 0  # Die
                    changes.append((x, y, 0))
            elif grid[x][y] == 0:
                if neighbors == 3:
                    new_grid[x][y] = 1  # Become alive
                    changes.append((x, y, 1))

    return new_grid, changes

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the grid state and get the list of changes
    grid, changes = update_grid(grid)

    # Apply changes by updating only the cells that changed state
    for (x, y, state) in changes:
        draw_cell(x, y, state)

    # Update the display
    pygame.display.flip()

    # Control the speed of the game
    pygame.time.delay(100)  # Adjust the value to make the simulation faster/slower
