"""
Natalie Rodriguez
CIS 350
Minesweeper

"""
# pylint: disable=no-member
import sys
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

TESTING_MODE = False  # change to True for test grid

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Minesweeper")
font = pygame.font.Font(None, 36)

# Load and play music in a loop
pygame.mixer.init()

# Load images

original_mine_img = pygame.image.load("mine.jpg")
original_tile_img = pygame.image.load("tile.jpg")

mine_img = pygame.transform.scale(original_mine_img, (40, 40))
tile_img = pygame.transform.scale(original_tile_img, (40, 40))

bg_image = pygame.image.load("catpaw.jpg")
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


SELECTED_LEVEL = 'Easy'

MEDIUM_GRID_SIZE = 16
MEDIUM_NUM_MINES = 40

HARD_GRID_WIDTH = 30
HARD_GRID_HEIGHT = 16
HARD_NUM_MINES = 99

# Initialize the grid
grid = [[0 for _ in range(9)] for _ in range(9)]
revealed = [[False for _ in range(9)] for _ in range(9)]
mines = set()

RUNNING_IN_MINESWEEPER_MENU = True


def setup_predefined_mines(predefined_mines):
    """
    Sets up mines in specific, predefined locations on the grid.
    This function is used for testing purposes to
    create a predictable game state.

    """
    global mines
    mines = set(predefined_mines)
    for y in range(9):
        for x in range(9):
            grid[y][x] = -1 if (x, y) in mines else 0
    for mine in mines:
        update_adjacent_cells(*mine)


def choose_level():
    """
    Displays a menu for the player to select the game's difficulty level.
    The player can choose between Easy, Medium, Hard,
    or go Back to the previous menu.
    """
    global SELECTED_LEVEL
    running_level_menu = True
    while running_level_menu:
        screen.blit(bg_image, (0, 0))

        levels = [
            ("Easy", "Easy"),
            ("Medium", "Medium"),
            ("Hard", "Hard"),
            ("Back", "Back")
        ]
        # Calculate the total height of all buttons
        total_height = (50 + 10) * len(levels) - 10
        # Start drawing buttons from this vertical position
        y_offset = (SCREEN_HEIGHT - total_height) // 2

        button_height = 50
        rects = []
        for level_name, level_value in levels:
            text = font.render(level_name, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH / 2,
                                              y_offset + button_height / 2))
            button_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 5,
                                      text_rect.width + 20, button_height)
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
                            SELECTED_LEVEL = level_value
                            running_level_menu = False

        pygame.display.flip()


def exit_to_main_menu():
    """"
    Exits the current menu and returns to the main menu of the game.
    """
    global RUNNING_IN_MINESWEEPER_MENU
    RUNNING_IN_MINESWEEPER_MENU = False


def calculate_screen_size(grid_width, grid_height):
    """
    Calculates the pixel dimensions of the game window based on the grid size.

    Args:
    - grid_width: The width of the grid in number of cells.
    - grid_height: The height of the grid in number of cells.
    """
    width = grid_width * GRID_SIZE
    height = grid_height * GRID_SIZE
    return width, height


def minesweeper_menu():
    """
    Displays the main menu of the Minesweeper game.
    Provides options to start the game, choose the difficulty level,
    or exit to the main menu.
    """
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    RUNNING_IN_MINESWEEPER_MENU = True
    while RUNNING_IN_MINESWEEPER_MENU:
        screen.blit(bg_image, (0, 0))

        options = [
            ("Start Minesweeper", run_minesweeper),
            ("Choose Level", choose_level),
            ("Exit to Main Menu", exit_to_main_menu)
        ]

        total_height = (50 + 10) * len(options) - 10
        y_offset = (SCREEN_HEIGHT - total_height) // 2

        button_height = 50
        rects = []
        for option_name, option_function in options:
            text = font.render(option_name, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH /
                                              2, y_offset + button_height / 2))
            button_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 5,
                                      text_rect.width + 20, button_height)
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
    """
    Randomly generates mine locations on the grid based
    on the selected difficulty level.
    The number and placement of mines vary with the difficulty level.
    """
    global grid, SELECTED_LEVEL
    mines.clear()

    # Initialize the grid size based on the selected difficulty level
    if SELECTED_LEVEL == 'Easy':
        total_mines = NUM_MINES
        grid_width = grid_height = 9
    elif SELECTED_LEVEL == 'Medium':
        total_mines = MEDIUM_NUM_MINES
        grid_width = grid_height = MEDIUM_GRID_SIZE
    else:  # 'Hard'
        total_mines = HARD_NUM_MINES
        grid_width = HARD_GRID_WIDTH
        grid_height = HARD_GRID_HEIGHT

    # Initialize the grid with the correct dimensions
    grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

    # Place mines randomly on the grid
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
    is_game_over = False
    if grid[grid_y][grid_x] == -1:
        is_game_over = True  # Game is over because a mine was clicked
    else:
        is_game_over = not reveal_cell(grid_x, grid_y)
    return is_game_over


def update_adjacent_cells(x, y):
    """
    Updates the number of adjacent mines for all cells around a given mine.

    Args:
    - x: The x-coordinate of the mine in the grid.
    - y: The y-coordinate of the mine in the grid.
    """
    for i in range(max(0, y - 1), min(len(grid), y + 2)):
        for j in range(max(0, x - 1), min(len(grid[0]), x + 2)):
            if grid[i][j] != -1:
                grid[i][j] += 1


def reveal_cell(x, y):
    """
    Reveals the contents of a cell and recursively
    reveals adjacent cells if needed.
    If the cell is empty (no adjacent mines),
    adjacent cells are also revealed.

    Args:
    - x: The x-coordinate of the cell in the grid.
    - y: The y-coordinate of the cell in the grid.

    Returns:
    - True if the cell is not a mine, False otherwise.
    """
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
    """
    Checks if the player has won the game.
    The player wins if all non-mine cells have been revealed.

    Returns:
    - True if the player has won, False otherwise.
    """
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if not revealed[y][x] and grid[y][x] != -1:
                return False  # Player hasn't won yet
    return True


def draw_grid():
    """
    Draws the game grid on the screen.
    This includes drawing each cell, mines,
    and numbers indicating adjacent mines.
    """
    grid_width = len(grid[0])
    grid_height = len(grid)
    grid_start_x = (screen.get_width() - grid_width * GRID_SIZE) // 2
    grid_start_y = (screen.get_height() - grid_height * GRID_SIZE) // 2

    for y in range(grid_height):
        for x in range(grid_width):
            rect = pygame.Rect(grid_start_x + x * GRID_SIZE,
                               grid_start_y + y * GRID_SIZE,
                               GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, PINK, rect, 1)

            if revealed[y][x]:
                if grid[y][x] == -1:
                    pygame.draw.circle(screen, BLACK,
                                       rect.center, GRID_SIZE // 2 - 5)
                elif grid[y][x] > 0:
                    text = font.render(str(grid[y][x]), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
            else:
                # Display the tile image for unrevealed tiles
                screen.blit(tile_img, rect.topleft)

    if GAME_OVER:
        for mine_x, mine_y in mines:
            mine_rect = pygame.Rect(grid_start_x + mine_x * GRID_SIZE,
                                    grid_start_y + mine_y *
                                    GRID_SIZE, GRID_SIZE, GRID_SIZE)
            screen.blit(mine_img, mine_rect.topleft)

GAME_OVER = False  # Track if the game is over
generate_mines()


def display_end_message(message):
    """
    Displays a message box at the end of the game.
    Shows a message indicating whether the player has won or
    lost and provides options to replay or return to the main menu.
    """
    current_screen_width, current_screen_height = (
        screen.get_size())  # Get the current window size

    # Adjust the size and position of the message box based on the window size
    rect_width = current_screen_width // 2
    rect_height = 150
    rect_x = (current_screen_width - rect_width) // 2
    rect_y = (current_screen_height - rect_height) // 2

    font_size = min(current_screen_width // 15, 48)  # Example calculation
    message_font = pygame.font.Font(None, font_size)

    # Draw the message box
    pygame.draw.rect(screen, PINK, (rect_x,
                                    rect_y, rect_width, rect_height))

    # Render and blit the message
    text = message_font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(current_screen_width // 2,
                                      current_screen_height // 2 - 50))
    screen.blit(text, text_rect)

    # Draw option buttons
    options = [("Replay", run_minesweeper),
               ("Back to Menu", minesweeper_menu)]
    button_rects = []  # List to store button rectangles for click detection

    y_offset = current_screen_height // 2
    for option_text, _ in options:
        text = message_font.render(option_text, True, WHITE)
        text_rect = text.get_rect(center=(current_screen_width / 2, y_offset))
        button_rect = text_rect.inflate(20, 10)
        button_rects.append((button_rect, option_text))
        screen.blit(text, text_rect)
        y_offset += font_size + 10

    pygame.display.flip()

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
                        if option_text == "Back to Menu":
                            return minesweeper_menu()
        pygame.display.flip()


def run_minesweeper():
    """
    Main function to run the Minesweeper game.
    Sets up the game, handles user input, and updates the game state.
    """
    global grid, revealed, mines, GAME_OVER, screen
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("Gameplay.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    if SELECTED_LEVEL == 'Easy':
        grid_width = grid_height = 9
    elif SELECTED_LEVEL == 'Medium':
        grid_width = grid_height = MEDIUM_GRID_SIZE
        NUM_MINES = MEDIUM_NUM_MINES
    elif SELECTED_LEVEL == 'Hard':
        grid_width = HARD_GRID_WIDTH
        grid_height = HARD_GRID_HEIGHT
        NUM_MINES = HARD_NUM_MINES

    grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    revealed = [[False for _ in range(grid_width)] for _ in range(grid_height)]
    mines.clear()
    GAME_OVER = False

    if TESTING_MODE:
        predefined_mines = {(0, 2), (0, 8), (1, 1), (2, 0), (2, 3),
                            (4, 4), (6, 1), (6, 5), (7, 4), (8, 4)}
        setup_predefined_mines(predefined_mines)
    else:
        generate_mines()

    # Calculate and set the new window size for the game based on grid size
    new_screen_width, new_screen_height = (
        calculate_screen_size(grid_width, grid_height))
    screen = pygame.display.set_mode(
        (new_screen_width, new_screen_height))

    # Recalculate GRID_START_X and GRID_START_Y for the new grid
    grid_start_x = (new_screen_width -
                    grid_width * GRID_SIZE) // 2
    grid_start_y = (new_screen_height -
                    grid_height * GRID_SIZE) // 2
    # cooldown variable so it doesn't count menu click towards the game
    cooldown_duration = 500
    start_time = pygame.time.get_ticks()
    end_game = False
    while True:
        elapsed_time = pygame.time.get_ticks() - start_time

        if end_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if ((SCREEN_WIDTH // 2 - 100 <= mouse_x <=
                         SCREEN_WIDTH // 2 + 100) and
                            (SCREEN_HEIGHT // 2 <= mouse_y <=
                             SCREEN_HEIGHT // 2 + 30)):
                        return run_minesweeper()

                    if ((SCREEN_WIDTH // 2 - 100 <= mouse_x <=
                         SCREEN_WIDTH // 2 + 100) and
                            (SCREEN_HEIGHT // 2 + 50 <= mouse_y <=
                             SCREEN_HEIGHT // 2 + 80)):
                        return minesweeper_menu()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif (event.type == pygame.MOUSEBUTTONDOWN and
                      elapsed_time > cooldown_duration):
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = (mouse_x - grid_start_x) // GRID_SIZE
                    grid_y = (mouse_y - grid_start_y) // GRID_SIZE

                    if 0 <= grid_x < len(grid[0]) and 0 <= grid_y < len(grid):
                        GAME_OVER = handle_tile_click(grid_x, grid_y)
                        if GAME_OVER:
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
        if GAME_OVER or has_player_won():
            pygame.mixer.music.stop()

if __name__ == "__main__":
    minesweeper_menu()
# pylint: enable=no-member

