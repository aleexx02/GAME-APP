'''
CIS 350 Fall 2023
Leah Barnes
Crossword Puzzle
'''
# Import pygame and button class
import pygame
import button

# Initialize pygame
pygame.init()

# Colors defined
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Display size
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

# Setting the screen and screen title
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Crossword Puzzle!")

# Start, rules and exit buttons instances and locations
start_img = pygame.image.load('buttons/start_button.png').convert_alpha()
exit_img = pygame.image.load('buttons/exit_button.png').convert_alpha()
rule_img = pygame.image.load('buttons/rules_button.png').convert_alpha()
start_button = button.Button(300, 160, start_img)
rules_button = button.Button(300, 305, rule_img)
exit_button = button.Button(300, 450, exit_img)

# Game variables
game_menu = True
rules_menu = False
game_play = False

# Define fonts
main_font = pygame.font.SysFont("arialblack", 60)
little_font = pygame.font.SysFont("arialblack", 20)

# Define colors
text_col = (0, 0, 0)

# When text is used, call this method to put the words on the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# The function for creating the gir
def draw_background():
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, BLACK, pygame.Rect(1, 1, 798, 400), 3)
    i = 1
    j = 1
    while (i * 36.2) < 800: # Creates the vertical lines on the screen
        pygame.draw.line(screen, BLACK, pygame.Vector2((i * 36.2) + 1, 1), pygame.Vector2((i * 36.2) + 1, 400), 3)
        i += 1

    while (j * 25) < 400: # Creates the horizontal lines on the screen
        pygame.draw.line(screen, BLACK, pygame.Vector2(798, (j * 25) + 1), pygame.Vector2(1, (j * 25) + 1), 3)
        j += 1

# Blank board for the user to start with a blank screen
blank_board = [
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],

]

# Correct board to compare the user's inputs with the correct answers
correct_board = [
    ['F', ' ', ' ', 'S', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['A', ' ', ' ', 'T', 'I', 'T', 'A', 'N', 'I', 'C', ' ', ' ', ' ', ' ', 'E', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['N', ' ', ' ', 'A', ' ', ' ', ' ', ' ', 'N', ' ', ' ', ' ', ' ', ' ', 'E', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['T', ' ', ' ', 'R', ' ', ' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['A', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'E', ' ', ' ', ' ', ' ', ' ', 'M', ' ', ' ', ' ', 'T', ' ', ' ', 'T'],
    ['S', ' ', ' ', 'W', ' ', ' ', 'I', ',', 'R', 'O', 'B', 'O', 'T', ' ', 'O', ' ', ' ', ' ', 'O', ' ', ' ', 'H'],
    ['T', ' ', ' ', 'A', ' ', ' ', ' ', ' ', 'S', ' ', ' ', ' ', ' ', ' ', 'V', ' ', ' ', ' ', 'Y', ' ', ' ', 'E'],
    ['I', ' ', ' ', 'R', ' ', ' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', ' ', 'I', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['C', 'A', 'R', 'S', ' ', 'O', 'P', 'P', 'E', 'N', 'H', 'E', 'I', 'M', 'E', 'R', ' ', ' ', 'S', ' ', ' ', 'A'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'L', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', ' ', 'V'],
    ['F', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'L', 'E', 'G', 'A', 'L', 'L', 'Y', ' ', 'B', 'L', 'O', 'N', 'D', 'E'],
    ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'A', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'A', ' ', 'R', ' ', ' ', 'N'],
    ['U', ' ', 'T', 'H', 'E', ' ', 'M', 'A', 'R', 'T', 'I', 'A', 'N', ' ', ' ', ' ', 'R', ' ', 'Y', ' ', ' ', 'G'],
    ['R', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', 'E'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'I', ' ', ' ', ' ', ' ', 'R'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'S', 'H', 'R', 'E', 'K', ' ', ' ', ' ', 'S']
]

# Draws either the correct board or the blank board function to the screen, whichever is chosen
def draw_letters():
    row = 0
    h_offset = 15
    while row < 16:
        col = 0
        while col < 21:
            output = blank_board[row][col]
            l_text = little_font.render(str(output), True, BLACK)
            screen.blit(l_text, pygame.Vector2((col * 36.2) + h_offset, (row * 25)))
            col += 1
        row += 1


# Game loop
run = True
while run:

    screen.fill((0, 0, 0))
    draw_background()
    draw_letters()

    # If in the game menu, show buttons and text
    if game_menu:
         # Background color
         screen.fill((255, 255, 255))
         # Title text
         draw_text("Crossword Puzzle", main_font, text_col, 115, 50)
         # Take you to the game
         if start_button.draw():
             game_menu = False

         # Takes you to a screen with rules not yet but maybe
         if rules_button.draw():
             game_menu = False
         # Exit the game
         if exit_button.draw():
             run = False

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_menu == False: #if we are not in the game menu and esc is pressed, takes us back there
                    game_menu = True
                else: #if we are in the game menu and esc is pressed, exit the game
                    run = False
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
