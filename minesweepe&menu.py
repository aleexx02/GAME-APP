import pygame
import sys
import os
import random


# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 50
NUM_MINES = 10


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (248, 200, 220)
RED = (255, 0, 0)  # Color for the game over message


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Menu")

pygame.mixer.init()

# Load and play music in a loop


font = pygame.font.Font(None, 36)
# Load images
image_folder = "C:\\Users\\XxCri\\PycharmProjects\\cis350\\assets\\images"


original_mine_img = pygame.image.load(os.path.join(image_folder, 'mine.jpg'))
original_tile_img = pygame.image.load(os.path.join(image_folder, 'tile.jpg'))


mine_img = pygame.transform.scale(original_mine_img, (50, 50))
tile_img = pygame.transform.scale(original_tile_img, (50, 50))


# Initialize the grid
grid = [[0 for _ in range(9)] for _ in range(9)]
revealed = [[False for _ in range(9)] for _ in range(9)]
mines = set()

def minesweeper_menu():
    while True:
        screen.fill(BLACK)
        y_offset = 100
        options = [
            ("Start Minesweeper", run_minesweeper),
            ("Settings", None),  # For future implementation
            ("Exit to Main Menu", main_menu)
        ]

        button_height = 50
        rects = []
        for option_name, option_function in options:
            text = font.render(option_name, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, y_offset))
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


#minesweeper functions
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






def display_game_over_message():
   font = pygame.font.Font(None, 48)
   text = font.render("Game Over - You hit a mine!", True, RED)
   text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
   screen.blit(text, text_rect)




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
        display_game_over_message()





game_over = False  # Flag to track if the game is over
generate_mines()


# Main game loop
def run_minesweeper():
   pygame.mixer.music.load("C:\\Users\\XxCri\\PycharmProjects\\cis350\\assets\\sounds\\Gameplay.mp3")
   pygame.mixer.music.play(-1)
   global grid, revealed, mines, game_over
   grid = [[0 for _ in range(9)] for _ in range(9)]
   revealed = [[False for _ in range(9)] for _ in range(9)]
   mines = set()
   game_over = False
   generate_mines()

   while True:
       redraw_screen = False  # A flag to determine if the screen should be updated

       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
           elif event.type == pygame.MOUSEBUTTONDOWN:
               mouse_x, mouse_y = pygame.mouse.get_pos()

               # Adjusted grid calculations
               grid_x = (mouse_x - GRID_START_X) // GRID_SIZE
               grid_y = (mouse_y - GRID_START_Y) // GRID_SIZE

               if 0 <= grid_x < len(grid[0]) and 0 <= grid_y < len(grid):
                   game_over = handle_tile_click(grid_x, grid_y)
                   redraw_screen = True  # Set the flag to redraw the screen later

       # Only redraw if necessary
       if redraw_screen:
           screen.fill(BLACK)
           draw_grid()
           if game_over:
               display_game_over_message()

           pygame.display.flip()


# Function to display the menu
def display_menu(screen, screen_width, screen_height):
   # Load the background image (assuming it's a JPEG image)
   background_image = pygame.image.load("C:\\Users\\Xxcri\\PycharmProjects\\cis350\\assets\\images\\bg.jpg")
   background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
   # Blit the background image to the screen
   screen.blit(background_image, (0, 0))

# Main menu loop
def main_menu():
    while True:
        screen.fill(BLACK)
        display_menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT) # Display the menu background

        y_offset = 100
        game_buttons = [
            ("Play Minesweeper", minesweeper_menu),
            # Add other games here
            # ("Play Game 2", game2_function),
            # ("Play Game 3", game3_function)
        ]

        rects = []  # To store button rectangles and their corresponding functions
        for game_name, game_function in game_buttons:
            text = font.render(game_name, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, y_offset))
            button_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 5, text_rect.width + 20, 50)
            pygame.draw.rect(screen, PINK, button_rect)  # Draw the button
            screen.blit(text, text_rect)  # Draw the text on the button
            rects.append((button_rect, game_function))
            y_offset += 60

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for rect, function in rects:
                    if rect.collidepoint(mouse_x, mouse_y) and function:
                        function()

        pygame.display.flip()

# Run the main menu
if __name__ == "__main__":
   screen_width, screen_height = 800, 600
   screen = pygame.display.set_mode((screen_width, screen_height))
   main_menu()
