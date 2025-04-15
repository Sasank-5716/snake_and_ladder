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