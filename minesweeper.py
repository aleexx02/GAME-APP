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
GRID_SIZE = 40
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

original_mine_img = pygame.image.load("mine.jpg")
original_tile_img = pygame.image.load("tile.jpg")

mine_img = pygame.transform.scale(original_mine_img, (40, 40))
tile_img = pygame.transform.scale(original_tile_img, (40, 40))

selected_level = 'Easy'

MEDIUM_GRID_SIZE = 16
MEDIUM_NUM_MINES = 40

HARD_GRID_WIDTH = 30
HARD_GRID_HEIGHT = 16
HARD_NUM_MINES = 99

# Initialize the grid
grid = [[0 for _ in range(9)] for _ in range(9)]
revealed = [[False for _ in range(9)] for _ in range(9)]
mines = set()

running_in_minesweeper_menu = True

def choose_level():
    global selected_level
    running_level_menu = True
    while running_level_menu:
        screen.fill(BLACK)

        levels = [
            ("Easy", "Easy"),
            ("Medium", "Medium"),
            ("Hard", "Hard"),
            ("Back", "Back")
        ]

        total_height = (50 + 10) * len(levels) - 10  # Calculate the total height of all buttons
        y_offset = (SCREEN_HEIGHT - total_height) // 2  # Start drawing buttons from this vertical position

        button_height = 50
        rects = []
        for level_name, level_value in levels:
            text = font.render(level_name, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, y_offset + button_height / 2))
            button_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 5, text_rect.width + 20, button_height)
            pygame.draw.rect(screen, PINK, button_rect)  # Draw the button
            screen.blit(text, text_rect)  # Draw the text on the button
            y_offset += button_height + 10
            rects.append((button_rect, level_value))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for rect, level_value in rects:
                    if rect.collidepoint(mouse_x, mouse_y):
                        if level_value == "Back":
                            running_level_menu = False
                        else:
                            selected_level = level_value
                            running_level_menu = False

        pygame.display.flip()

def exit_to_main_menu():
    global running_in_minesweeper_menu
    running_in_minesweeper_menu = False


def calculate_screen_size(grid_width, grid_height):
    width = grid_width * GRID_SIZE
    height = grid_height * GRID_SIZE
    return width, height

def minesweeper_menu():
    global running_in_minesweeper_menu, screen
    screen = pygame.display.set_mode((800, 600))
    running_in_minesweeper_menu = True
    while running_in_minesweeper_menu:
        screen.fill(BLACK)

        options = [
            ("Start Minesweeper", run_minesweeper),
            ("Choose Level", choose_level),
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

def generate_mines():
    global mines
    mines.clear()

    global selected_level
    if selected_level == 'Easy':
        total_mines = NUM_MINES
        grid_width = grid_height = 9
    elif selected_level == 'Medium':
        total_mines = MEDIUM_NUM_MINES
        grid_width = grid_height = MEDIUM_GRID_SIZE
    else:  # 'Hard'
        total_mines = HARD_NUM_MINES
        grid_width = HARD_GRID_WIDTH
        grid_height = HARD_GRID_HEIGHT

    while len(mines) < total_mines:
        x = random.randint(0, grid_width - 1)
        y = random.randint(0, grid_height - 1)
        if (x, y) not in mines:
            mines.add((x, y))
            grid[y][x] = -1
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

def draw_grid(screen, grid, revealed, mines, game_over):
    grid_width = len(grid[0])
    grid_height = len(grid)
    grid_start_x = (screen.get_width() - grid_width * GRID_SIZE) // 2
    grid_start_y = (screen.get_height() - grid_height * GRID_SIZE) // 2

    for y in range(grid_height):
        for x in range(grid_width):
            rect = pygame.Rect(grid_start_x + x * GRID_SIZE, grid_start_y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, PINK, rect, 1)

            if revealed[y][x]:
                if grid[y][x] == -1:
                    pygame.draw.circle(screen, BLACK, rect.center, GRID_SIZE // 2 - 5)
                elif grid[y][x] > 0:
                    text = font.render(str(grid[y][x]), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
            else:
                # Display the tile image for unrevealed tiles
                screen.blit(tile_img, rect.topleft)

    if game_over:
        for mine_x, mine_y in mines:
            mine_rect = pygame.Rect(grid_start_x + mine_x * GRID_SIZE, grid_start_y + mine_y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            screen.blit(mine_img, mine_rect.topleft)


game_over = False  # Track if the game is over
generate_mines()

def display_end_message(message):
    current_screen_width, current_screen_height = screen.get_size()  # Get the current window size

    # Adjust the size and position of the message box based on the window size
    rect_width = current_screen_width // 2
    rect_height = 150
    rect_x = (current_screen_width - rect_width) // 2
    rect_y = (current_screen_height - rect_height) // 2

    font_size = min(current_screen_width // 15, 48)  # Example calculation
    message_font = pygame.font.Font(None, font_size)

    # Draw the message box
    pygame.draw.rect(screen, PINK, (rect_x, rect_y, rect_width, rect_height))

    # Render and blit the message
    text = message_font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(current_screen_width // 2, current_screen_height // 2 - 50))
    screen.blit(text, text_rect)

    # Draw option buttons
    options = [("Replay", run_minesweeper), ("Back to Menu", minesweeper_menu)]
    button_rects = []  # List to store button rectangles for click detection

    y_offset = current_screen_height // 2
    for option_text, _ in options:
        text = message_font.render(option_text, True, WHITE)
        text_rect = text.get_rect(center=(current_screen_width / 2, y_offset))
        button_rect = text_rect.inflate(20, 10)  # Increase rect size for easier clicking
        button_rects.append((button_rect, option_text))  # Store the rect and the option text
        screen.blit(text, text_rect)
        y_offset += font_size + 10  # Adjust spacing based on font size

    pygame.display.flip()  # Update the display

    # Event handling for buttons
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for rect, option_text in button_rects:
                    if rect.collidepoint(mouse_x, mouse_y):
                        if option_text == "Replay":
                            return run_minesweeper()
                        elif option_text == "Back to Menu":
                            return minesweeper_menu()

        pygame.display.flip()
def run_minesweeper():
    global grid, revealed, mines, game_over, screen, GRID_START_X, GRID_START_Y
    if selected_level == 'Easy':
        grid_width = grid_height = 9
        NUM_MINES = 10
    elif selected_level == 'Medium':
        grid_width = grid_height = MEDIUM_GRID_SIZE
        NUM_MINES = MEDIUM_NUM_MINES
    elif selected_level == 'Hard':
        grid_width = HARD_GRID_WIDTH
        grid_height = HARD_GRID_HEIGHT
        NUM_MINES = HARD_NUM_MINES

    grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    revealed = [[False for _ in range(grid_width)] for _ in range(grid_height)]
    mines.clear()
    game_over = False
    generate_mines()

    # Calculate and set the new window size for the game based on grid size
    new_screen_width, new_screen_height = calculate_screen_size(grid_width, grid_height)
    screen = pygame.display.set_mode((new_screen_width, new_screen_height))

    # Recalculate GRID_START_X and GRID_START_Y for the new grid
    GRID_START_X = (new_screen_width - grid_width * GRID_SIZE) // 2
    GRID_START_Y = (new_screen_height - grid_height * GRID_SIZE) // 2

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

                    if (SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100) and (SCREEN_HEIGHT // 2 <= mouse_y <= SCREEN_HEIGHT // 2 + 30):
                        return run_minesweeper()

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
                            draw_grid(screen, grid, revealed, mines, game_over)
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
            draw_grid(screen, grid, revealed, mines, game_over)
            pygame.display.flip()
