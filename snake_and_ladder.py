import pygame
import random
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snakes & Ladders")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game Constants
BOARD_SIZE = 10
CELL_SIZE = 50
PLAYER_SIZE = 20
DICE_SIZE = 50

# Ladders (start, end)
ladders = {
    3: 22,
    5: 8,
    11: 26,
    20: 29,
    17: 4,  
    27: 1   
}

# Snakes (start, end)
snakes = {
    17: 4,
    19: 7,
    21: 9,
    27: 1
}

# Player positions
players = {
    "Player 1": {"pos": 0, "color": RED},
    "Player 2": {"pos": 0, "color": BLUE}
}
current_player = "Player 1"

# Dice
dice_value = 1
dice_rolling = False
roll_start_time = 0

# Helper functions
def get_board_position(cell):
    """Convert cell number to screen coordinates"""
    row = 9 - (cell-1) // BOARD_SIZE
    col = (cell-1) % BOARD_SIZE
    if row % 2 == 1:
        col = 9 - col
    x = 100 + col * CELL_SIZE + CELL_SIZE//2
    y = 50 + row * CELL_SIZE + CELL_SIZE//2
    return x, y

def draw_board():
    """Draw the Snakes & Ladders board"""
    screen.fill(WHITE)

# Draw grid
    for i in range(100):
        row = 9 - i // 10
        col = i % 10
        if row % 2 == 1:
            col = 9 - col
        x = 100 + col * CELL_SIZE
        y = 50 + row * CELL_SIZE
        pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
        
        # Draw cell numbers
        font = pygame.font.SysFont(None, 20)
        text = font.render(str(i+1), True, BLACK)
        screen.blit(text, (x + 5, y + 5))

# Draw ladders
    for start, end in ladders.items():
        start_pos = get_board_position(start)
        end_pos = get_board_position(end)
        pygame.draw.line(screen, GREEN, start_pos, end_pos, 5)
        # Draw ladder rungs
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        for i in range(1, 4):
            x = start_pos[0] + dx*i/4
            y = start_pos[1] + dy*i/4
            pygame.draw.line(screen, GREEN, 
                           (x - dy/15, y + dx/15),
                           (x + dy/15, y - dx/15), 3)
            

# Draw snakes
    for start, end in snakes.items():
        start_pos = get_board_position(start)
        end_pos = get_board_position(end)
        pygame.draw.line(screen, RED, start_pos, end_pos, 5)
        # Draw snake head
        direction = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
        length = (direction[0]**2 + direction[1]**2)**0.5
        unit = (direction[0]/length, direction[1]/length)
        head = (end_pos[0] - unit[0]*20, end_pos[1] - unit[1]*20)
        pygame.draw.circle(screen, RED, head, 8)