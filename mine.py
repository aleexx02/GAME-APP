"""
Natalie Rodriguez
CIS 350
Minesweeper

"""

import sys
import os
import random
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 50
NUM_MINES = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (248, 200, 220)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Minesweeper")
font = pygame.font.Font(None, 36)

# Load and play music in a loop
# pygame.mixer.init()

# Load images

original_mine_img = pygame.image.load('mine.jpg')
original_tile_img = pygame.image.load('tile.jpg')

mine_img = pygame.transform.scale(original_mine_img, (50, 50))
tile_img = pygame.transform.scale(original_tile_img, (50, 50))

# Initialize the grid
grid = [[0 for _ in range(9)] for _ in range(9)]
revealed = [[False for _ in range(9)] for _ in range(9)]
mines = set()

running_in_minesweeper_menu = True

def exit_to_main_menu():
    global running_in_minesweeper_menu
    running_in_minesweeper_menu = False

def minesweeper_menu():
    global running_in_minesweeper_menu
    while running_in_minesweeper_menu:
        screen.fill(BLACK)

        options = [
            ("Start Minesweeper", run_minesweeper),
            ("Settings", None),  # For future implementation
            ("Exit to Main Menu", exit_to_main_menu)
        ]

        total_height = (50 + 10) * len(options) - 10  # Calculate the total height of all buttons
        y_offset = (SCREEN_HEIGHT - total_height) // 2  # Start drawing buttons from this vertical position

        button_height = 50
        rects = []
        for option_name, option_function in options:
            text = font.render(option_name, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, y_offset + button_height / 2))
            button_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 5, text_rect.width + 20, button_height)
            pygame.draw.rect(screen, PINK, button_rect)  # Draw the button
            screen.blit(text, text_rect)  # Draw the text on the button
            y_offset += button_height + 10
            rects.append((button_rect, option_function))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for rect, function in rects:
                    if rect.collidepoint(mouse_x, mouse_y) and function:
                        function()  # Run the corresponding option

        pygame.display.flip()

GRID_WIDTH = len(grid[0]) * GRID_SIZE
GRID_HEIGHT = len(grid) * GRID_SIZE

GRID_START_X = (SCREEN_WIDTH - GRID_WIDTH) // 2
GRID_START_Y = (SCREEN_HEIGHT - GRID_HEIGHT) // 2

def generate_mines():
   global mines
   mines = set()
   for y in range(len(grid)):
       for x in range(len(grid[0])):
           if random.random() < 1 / 8.1 and len(mines) < NUM_MINES:
               grid[y][x] = -1
               mines.add((x, y))
               update_adjacent_cells(x, y)

def handle_tile_click(grid_x, grid_y):
    """
    Handles the logic when a tile in the Minesweeper game is clicked.

    Args:
    - grid_x: The x-coordinate of the clicked tile in the grid.
    - grid_y: The y-coordinate of the clicked tile in the grid.

    Returns:
    - True if the game is over (a mine was clicked), False otherwise.
    """
    # If the cell contains a mine
    if grid[grid_y][grid_x] == -1:
        return True  # Game is over because a mine was clicked

    # Otherwise, reveal the cell and its adjacent cells if necessary
    game_over = not reveal_cell(grid_x, grid_y)

    return game_over

def update_adjacent_cells(x, y):
   for i in range(max(0, y - 1), min(len(grid), y + 2)):
       for j in range(max(0, x - 1), min(len(grid[0]), x + 2)):
           if grid[i][j] != -1:
               grid[i][j] += 1

def reveal_cell(x, y):
   if not (0 <= x < len(grid[0]) and 0 <= y < len(grid)):
       return False

   if revealed[y][x]:
       return False

   revealed[y][x] = True

   if grid[y][x] == 0:
       for i in range(max(0, y - 1), min(len(grid), y + 2)):
           for j in range(max(0, x - 1), min(len(grid[0]), x + 2)):
               reveal_cell(j, i)

   return grid[y][x] != -1

def has_player_won():
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if not revealed[y][x] and grid[y][x] != -1:  # If a non-mine tile is not revealed
                return False  # Player hasn't won yet
    return True

def draw_grid():
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            rect = pygame.Rect(GRID_START_X + x * GRID_SIZE, GRID_START_Y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, PINK, rect, 1)

            if revealed[y][x]:
                if grid[y][x] == -1:
                    pygame.draw.circle(screen, BLACK, rect.center, GRID_SIZE // 2 - 5)
                elif grid[y][x] > 0:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(grid[y][x]), True, BLACK)
                    text_rect = text.get_rect(center=(GRID_START_X + x * GRID_SIZE + GRID_SIZE // 2, GRID_START_Y + y * GRID_SIZE + GRID_SIZE // 2))
                    screen.blit(text, text_rect)
            else:
                # Display the tile image for unrevealed tiles
                screen.blit(tile_img, rect.topleft)

    # Display the mine image for the tile that contains a mine when the game is over
    if game_over:
        for mine_x, mine_y in mines:
            mine_rect = pygame.Rect(GRID_START_X + mine_x * GRID_SIZE, GRID_START_Y + mine_y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            screen.blit(mine_img, mine_rect.topleft)


game_over = False  # Track if the game is over
generate_mines()

def display_end_message(message):
    font = pygame.font.Font(None, 48)

    # Calculate the width and height of the pink rectangle
    rect_width = SCREEN_WIDTH // 2
    rect_height = 150

    rect_x = (SCREEN_WIDTH - rect_width) // 2
    rect_y = (SCREEN_HEIGHT - rect_height) // 2

    # Draw the pink rectangle
    pygame.draw.rect(screen, PINK, (rect_x, rect_y, rect_width, rect_height))

    # Render and blit the message
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    options = [("Replay", run_minesweeper), ("Back to Menu", minesweeper_menu)]
    y_offset = SCREEN_HEIGHT // 2
    for option_text, option_function in options:
        text = font.render(option_text, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, y_offset))
        screen.blit(text, text_rect)
        y_offset += 50

def run_minesweeper():
    # pygame.mixer.music.load("Gameplay.mp3")
    # pygame.mixer.music.set_volume(0.3)
    # pygame.mixer.music.play(-1)
    global grid, revealed, mines, game_over
    grid = [[0 for _ in range(9)] for _ in range(9)]
    revealed = [[False for _ in range(9)] for _ in range(9)]
    mines = set()
    game_over = False
    generate_mines()

    # cooldown variable so it doesn't count menu click towards the game
    cooldown_duration = 500
    start_time = pygame.time.get_ticks()

    end_game = False
    while True:
        elapsed_time = pygame.time.get_ticks() - start_time  # Calculate the elapsed time

        if end_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Check if "Replay" was clicked
                    if (SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100) and (SCREEN_HEIGHT // 2 <= mouse_y <= SCREEN_HEIGHT // 2 + 30):
                        return run_minesweeper()

                    # Check if "Back to Menu" was clicked
                    if (SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100) and (SCREEN_HEIGHT // 2 + 50 <= mouse_y <= SCREEN_HEIGHT // 2 + 80):
                        return minesweeper_menu()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and elapsed_time > cooldown_duration:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = (mouse_x - GRID_START_X) // GRID_SIZE
                    grid_y = (mouse_y - GRID_START_Y) // GRID_SIZE

                    if 0 <= grid_x < len(grid[0]) and 0 <= grid_y < len(grid):
                        game_over = handle_tile_click(grid_x, grid_y)
                        if game_over:
                            end_game = True
                            screen.fill(BLACK)
                            draw_grid()
                            display_end_message("Game Over!")
                            pygame.display.flip()

                        elif has_player_won():
                            end_game = True
                            screen.fill(BLACK)
                            draw_grid()
                            display_end_message("You've won!")
                            pygame.display.flip()

        if not end_game:
            screen.fill(BLACK)
            draw_grid()
            pygame.display.flip()

        # if game_over or has_player_won():
            # pygame.mixer.music.stop()