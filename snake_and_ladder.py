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
GRAY = (200, 200, 200)

# Game Constants
BOARD_SIZE = 10
CELL_SIZE = 50
PLAYER_SIZE = 20
DICE_SIZE = 50

players = {
    "Player 1": {"pos": 1, "color": BLUE},  
    "Player 2": {"pos": 1, "color": YELLOW} 
}

# Ladders (start, end)
ladders = {
    2: 38,   7: 14,   8: 31,   15: 26,
    21: 42,  28: 84,  36: 44,  51: 67,
    71: 91,  78: 98,  87: 94   
}

# Snakes (start, end)
snakes = {
    16: 6,   24: 11,  34: 19,  46: 25,
    53: 33,  62: 37,  64: 60,  74: 53,
    89: 68,  92: 88,  95: 75,  99: 5 
}

current_player = "Player 1"

# Dice
dice_value = 1
dice_rolling = False
roll_start_time = 0

# Animation variables
animating = False
animation_start = 0
animation_steps = 0
animation_current = 0
animation_player = ""
animation_path = []

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
    screen.fill(GRAY)

# Draw grid
    for i in range(100):
        row = 9 - i // 10
        col = i % 10
        if row % 2 == 1:
            col = 9 - col
        x = 100 + col * CELL_SIZE
        y = 50 + row * CELL_SIZE
        color = WHITE if (i % 2 == 0) else (240, 240, 240)
        pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
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
        segments = 20
        for i in range(segments):
            t1 = i/segments
            t2 = (i+1)/segments
                
            mid_t = (t1 + t2)/2
            offset = 10 * (1 - 2*abs(mid_t - 0.5))
                
            x1 = start_pos[0] + (end_pos[0]-start_pos[0])*t1
            y1 = start_pos[1] + (end_pos[1]-start_pos[1])*t1 + offset
                
            x2 = start_pos[0] + (end_pos[0]-start_pos[0])*t2
            y2 = start_pos[1] + (end_pos[1]-start_pos[1])*t2 + offset
                
            pygame.draw.line(screen, RED, (x1, y1), (x2, y2), 8)
        # Calculate direction vector
        direction = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
        length = (direction[0]**2 + direction[1]**2)**0.5
        if length > 0:  # Avoid division by zero
            unit = (direction[0]/length, direction[1]/length)
            # Draw snake head with eyes
            head = (end_pos[0] - unit[0]*20, end_pos[1] - unit[1]*20)
            pygame.draw.circle(screen, RED, head, 10)
            eye_offset = (-unit[1]*5, unit[0]*5)
            pygame.draw.circle(screen, WHITE, (head[0] + eye_offset[0], head[1] + eye_offset[1]), 3)



def draw_dice():
    """Draw the dice and current value"""
    pygame.draw.rect(screen, BLACK, (WIDTH - 100, HEIGHT - 100, DICE_SIZE, DICE_SIZE), 0, 10)  # Added rounded corners
    pygame.draw.rect(screen, WHITE, (WIDTH - 95, HEIGHT - 95, DICE_SIZE-10, DICE_SIZE-10), 0, 5)
    
    if dice_rolling:
        value = random.randint(1, 6)
    else:
        value = dice_value

    # Draw dice dots
    dot_positions = {
        1: [(DICE_SIZE//2, DICE_SIZE//2)],
        2: [(DICE_SIZE//4, DICE_SIZE//4), (3*DICE_SIZE//4, 3*DICE_SIZE//4)],
        3: [(DICE_SIZE//4, DICE_SIZE//4), (DICE_SIZE//2, DICE_SIZE//2), (3*DICE_SIZE//4, 3*DICE_SIZE//4)],
        4: [(DICE_SIZE//4, DICE_SIZE//4), (3*DICE_SIZE//4, DICE_SIZE//4),
            (DICE_SIZE//4, 3*DICE_SIZE//4), (3*DICE_SIZE//4, 3*DICE_SIZE//4)],
        5: [(DICE_SIZE//4, DICE_SIZE//4), (3*DICE_SIZE//4, DICE_SIZE//4),
            (DICE_SIZE//2, DICE_SIZE//2),
            (DICE_SIZE//4, 3*DICE_SIZE//4), (3*DICE_SIZE//4, 3*DICE_SIZE//4)],
        6: [(DICE_SIZE//4, DICE_SIZE//4), (3*DICE_SIZE//4, DICE_SIZE//4),
            (DICE_SIZE//4, DICE_SIZE//2), (3*DICE_SIZE//4, DICE_SIZE//2),
            (DICE_SIZE//4, 3*DICE_SIZE//4), (3*DICE_SIZE//4, 3*DICE_SIZE//4)]
    }
    
    for pos in dot_positions[value]:
        pygame.draw.circle(screen, BLACK, 
                         (WIDTH - 100 + pos[0], HEIGHT - 100 + pos[1]), 4)
        
def draw_players():
    """Draw the players on the board"""
    for i, (player, data) in enumerate(players.items()):
        pos = data["pos"]
        color = data["color"]
        if pos > 0 and pos <= 100:  # Only draw if position is valid
            x, y = get_board_position(pos)
            # Offset players slightly
            offset = 10 if i == 0 else -10
            pygame.draw.circle(screen, color, (x + offset, y), PLAYER_SIZE)
            pygame.draw.circle(screen, BLACK, (x + offset, y), PLAYER_SIZE, 1)


        

def draw_ui():
    """Draw user interface elements"""
    # Current player indicator
    font = pygame.font.SysFont(None, 36)
    turn_text = font.render(f"{current_player}'s Turn", True, players[current_player]["color"])
    screen.blit(turn_text, (50, HEIGHT - 50))
    
    # Player info indicators
    p1_text = font.render("Player 1", True, BLUE)
    screen.blit(p1_text, (50, 30))
    pygame.draw.circle(screen, BLUE, (150, 40), PLAYER_SIZE)
    
    p2_text = font.render("Player 2", True, YELLOW)
    screen.blit(p2_text, (50, 70))
    pygame.draw.circle(screen, YELLOW, (150, 80), PLAYER_SIZE)
    
    # Dice label
    dice_label = font.render("Roll:", True, BLACK)
    screen.blit(dice_label, (WIDTH - 150, HEIGHT - 70))

def handle_movement(player, steps):
    global current_player, animating, animation_start, animation_steps, animation_player, animation_path
    
    animating = True
    animation_start = pygame.time.get_ticks()
    animation_steps = steps
    animation_current = 0
    animation_player = player
    animation_path = []
    start_pos = players[player]["pos"]
    players[player]["pos"] += steps
    
     # Create path for animation
    current_pos = players[player]["pos"]
    for step in range(1, steps + 1):
        new_pos = start_pos + step  # Start from the saved starting position
        if new_pos > 100:
            new_pos = 100 - (new_pos - 100)  # Bounce back if over 100
        animation_path.append(new_pos)
    
    # Check for snake or ladder at final position
    final_pos = players[player]["pos"]
    if final_pos in ladders:
        players[player]["pos"] = ladders[final_pos]  # Move player to ladder end
        animation_path.append(ladders[final_pos]) # Add ladder end to path
    elif final_pos in snakes:
        players[player]["pos"] = snakes[final_pos]  # Move player to snake end
        animation_path.append(snakes[final_pos]) # Add snake end to path

def update_animation():
    global animating, animation_start, animation_current, current_player, dice_value
    
    if pygame.time.get_ticks() - animation_start > 300:  # 300ms per step
        animation_start = pygame.time.get_ticks()
        animation_current += 1
        
        if animation_current < len(animation_path):
            players[animation_player]["pos"] = animation_path[animation_current]
        else:
            # Animation complete
            animating = False
            final_pos = players[animation_player]["pos"]
            
            if final_pos >= 100:
                show_winner(animation_player)
            else:
                # Switch player
                current_player = "Player 2" if current_player == "Player 1" else "Player 1"
                

def show_winner(player):
    font = pygame.font.SysFont(None, 72)
    text = font.render(f"{player} Wins!", True, players[player]["color"])
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    
    restart_font = pygame.font.SysFont(None, 36)
    restart_text = restart_font.render("Click to play again", True, BLACK)
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
                reset_game()
        
        screen.fill(WHITE)
        screen.blit(text, text_rect)
        screen.blit(restart_text, restart_rect)
        pygame.display.flip()
        clock.tick(30)

def reset_game():
    global players, current_player, dice_value, dice_rolling, animating
    
    players = {
        "Player 1": {"pos": 1, "color": BLUE},
        "Player 2": {"pos": 1, "color": YELLOW}
    }
    current_player = "Player 1"
    dice_value = 1
    dice_rolling = False
    animating = False

def handle_events():
    global dice_rolling, roll_start_time, dice_value
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if (WIDTH - 100 <= x <= WIDTH - 50 and 
                HEIGHT - 100 <= y <= HEIGHT - 50):
                if not dice_rolling:
                    dice_rolling = True
                    roll_start_time = pygame.time.get_ticks()

while True:
    handle_events()
    
    # Dice rolling animation
    if dice_rolling:
        if pygame.time.get_ticks() - roll_start_time > 1000:
            dice_rolling = False
            dice_value = random.randint(1, 6)
            handle_movement(current_player, dice_value)
    
    # Handle movement animation
    if animating:
        update_animation()

    # Drawing
    draw_board()
    draw_players()
    draw_dice()
    
    # UI Elements
    font = pygame.font.SysFont(None, 36)
    turn_text = font.render(f"{current_player}'s Turn", True, BLACK)
    screen.blit(turn_text, (50, HEIGHT - 50))
    
    pygame.display.flip()
    clock.tick(30)
