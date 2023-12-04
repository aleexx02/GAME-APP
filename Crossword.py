'''
CIS 350 Fall 2023
Leah Barnes
Crossword Puzzle
'''
# Import pygame and button class
import pygame
#import button
import pygame_gui

# Initialize pygame
pygame.init()


# Colors defined
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (221, 0, 255)

# Display size
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

# Setting the screen and screen title
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

CLOCK = pygame.time.Clock()
MANAGER = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((84, 407), (241, 25)), manager=MANAGER, object_id="#main_text_entry")

# Game variables
game_menu = True
rules_menu = False
game_play = False

# Define fonts
main_font = pygame.font.SysFont("arialblack", 60)
little_font = pygame.font.SysFont("arialblack", 20)
hint_font = pygame.font.SysFont("arialblack", 15)
smaller_hint = pygame.font.SysFont("arialblack", 12)
nums_font = pygame.font.SysFont("arialblack", 10)

# Define colors
text_col = (0, 0, 0)

# Button class that makes buttons clickable
'''

'''
class Button():
    '''
    The class to create working clickable buttons

    ...

    Attributes
    ----------

    '''
    def __init__(self, x, y, image):
        '''
        :param x: int
            The x coordinate of where the image or the button will be placed
        :param y: int
            The y coordinate of where the image or the button will be placed
        :param image: str
            The file for the image used for the button
        '''
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        '''

        :return: Bool value which is if the mouse button was pressed or not
        '''
        action = False
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check mouse over button and clicked conditions
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        # draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

# Start, rules and exit buttons instances and locations
start_img = pygame.image.load('buttons/start_button.png').convert_alpha()
exit_img = pygame.image.load('buttons/exit_button.png').convert_alpha()
rule_img = pygame.image.load('buttons/rules_button.png').convert_alpha()
start_button = Button(300, 160, start_img)
rules_button = Button(300, 305, rule_img)
exit_button = Button(300, 450, exit_img)
ff_img = pygame.image.load('words/fantasticfour.png').convert_alpha()
ff = Button(4, 2, ff_img)
c_img = pygame.image.load('words/cars.png').convert_alpha()
#c = Button()

correct_words = ["Fantastic Four", "Cars", "Star Wars", "Titanic", "Interstellar",\
                 "I,Robot", "Bee Movie", "Oppenheimer", "Toy Story", "The Martian",\
                 "Barbie", "Legally Blonde", "The Avengers", "Shrek"]

# user_input = input()
# if user_input in correct_words:
#     print("yes")
#
# def getting_words():
#     num = 50
#     while num:
#         if user_input in correct_words:
#             print("yes")
#         num -= 1

# When text is used, call this method to put the words on the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# def insert():
#     hint_font = pygame.font.SysFont("arialblack", 15)
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#             if event.type == pygame.KEYDOWN:


# The function for creating the grid
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
        while col < 22:
            output = blank_board[row][col]
            output = correct_board[row][col]
            l_text = little_font.render(str(output), True, BLACK)
            screen.blit(l_text, pygame.Vector2((col * 36.2) + h_offset, (row * 25)))
            col += 1
        row += 1

# def text_box():
#     # Set up textbox
#     textbox_rect = pygame.Rect(50, 50, 200, 30)
#     textbox_text = ""
#     textbox_active = False
#
#     # Main game loop
#     while True:
#         screen.fill((0, 0, 0))
#
#         # Handle events
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if textbox_rect.collidepoint(event.pos):
#                     textbox_active = not textbox_active
#                 else:
#                     textbox_active = False
#             elif event.type == pygame.KEYDOWN:
#                 if textbox_active:
#                     if event.key == pygame.K_RETURN:
#                         print("Text entered:", textbox_text)
#                         textbox_text = ""
#                     elif event.key == pygame.K_BACKSPACE:
#                         textbox_text = textbox_text[:-1]
#                     else:
#                         textbox_text += event.unicode

# Draws the rules to the screen
def rules_board():
    draw_text("Rules:", main_font, text_col, 299, 50)
    draw_text("1: Spaces", little_font, text_col, 10, 150)
    draw_text("- #1, #3, #7, #9, #10, #12 and #13 have spaces in the name, include it.", hint_font, text_col, 30, 180)
    draw_text("2: Commas", little_font, text_col, 10, 200)
    draw_text("- #6 has a comma instead of a space. Include the comma, exclude the space.", hint_font, text_col, 30, 230)
    draw_text("3: Buttons", little_font, text_col, 10, 250)
    draw_text("- 'Start' button:", hint_font, text_col, 30, 280)
    draw_text("Takes you into the game, to the puzzle board. Hit escape to go back to main menu.", hint_font, text_col, 50, 300)
    draw_text("- 'Rules' button:", hint_font, text_col, 30, 320)
    draw_text("You are here...takes you to the game rules. Hit escape to go back to main menu.", hint_font, text_col, 50, 340)
    draw_text("- 'Exit' button:", hint_font, text_col, 30, 360)
    draw_text("Will exit out of the game completely.", hint_font, text_col, 50, 380)
    draw_text("- Escape key:", hint_font, text_col, 30, 400)
    draw_text("Will take you back to the menu from rules or start. Exits completely in main menu.", hint_font, text_col, 50, 420)
    draw_text("- X in the top right:", hint_font, text_col, 30, 440)
    draw_text("Exits the game completely from whichever menu you are in.", hint_font, text_col, 50, 460)

# Draws the hints to the start screen
def hints():
    # Down hints
    draw_text("Hints", hint_font, text_col, 20, 400)
    draw_text("Down:", smaller_hint, text_col, 30, 420)
    draw_text("1: A space station crew is espoxed to a myserious cosmic", smaller_hint, text_col, 35, 435)
    draw_text("storm, giving them powers.", smaller_hint, text_col, 35 , 450)
    draw_text("3: Set a long time ago in a galaxy far, far away", smaller_hint, text_col, 35, 465)
    draw_text("5: Astronauts travel through a wormhole looking for a", smaller_hint, text_col, 35, 480)
    draw_text("new home for humankind", smaller_hint, text_col, 35, 495)
    draw_text("7: After an adenture outside the hive, he finds out", smaller_hint, text_col, 35, 510)
    draw_text("humans eat honey and sues them for it", smaller_hint, text_col, 35, 525)
    draw_text("9: Toys come to life when the owner isn't around", smaller_hint, text_col, 35, 540)
    draw_text("11: Doll has crisis about dreamhouse and journies away", smaller_hint, text_col, 35, 555)
    draw_text("13: A group of extraordinary individuals who were", smaller_hint, text_col, 35, 570)
    draw_text("assembled to defeat Loki and his army in New York", smaller_hint, text_col, 35, 585)
    # Across hints
    draw_text("Across:", smaller_hint, text_col, 420, 420)
    draw_text("2: Hotshot rookie racecar gets stranded in a little town", smaller_hint, text_col, 420, 435)
    draw_text("and learns that winning isn't everything", smaller_hint, text_col, 420, 450)
    draw_text("4: a 17 y/o aristocrat falls in love with a kind but poor", smaller_hint, text_col, 420, 465)
    draw_text("artist aboard a ship", smaller_hint, text_col, 420, 480)
    draw_text("6: A detective investigates an alleged suicide of a ", smaller_hint, text_col, 420, 495)
    draw_text("scientist beliving it was a murder, and uncovers a secret", smaller_hint, text_col, 420, 510)
    draw_text("8: Follows the Manhattan Project during WWII", smaller_hint, text_col, 420, 525)
    draw_text("10: An astronaut gets stranded on Mars after a storm", smaller_hint, text_col, 420, 540)
    draw_text("knocked him from his team. Now, he awaits to be rescued", smaller_hint, text_col, 420, 555)
    draw_text("12: A sorority girl follows ex to Haravd to win him back", smaller_hint, text_col, 420, 570)
    draw_text("14: A green ogre goes on a quest to save the princess", smaller_hint, text_col, 420, 585)

# Colors the blank squares black
def squares():
    pygame.draw.rect(screen, BLACK, pygame.Rect(38, 2, 70, 201))
    pygame.draw.rect(screen, BLACK, pygame.Rect(146, 4, 360, 24))
    pygame.draw.rect(screen, BLACK, pygame.Rect(146, 51, 146, 75))
    pygame.draw.rect(screen, BLACK, pygame.Rect(362, 25, 145, 100))
    pygame.draw.rect(screen, BLACK, pygame.Rect(326, 52, 37, 75))
    pygame.draw.rect(screen, BLACK, pygame.Rect(471, 126, 35, 74))
    pygame.draw.rect(screen, BLACK, pygame.Rect(326, 151, 146, 49))
    pygame.draw.rect(screen, BLACK, pygame.Rect(146, 126, 72, 75))
    pygame.draw.rect(screen, BLACK, pygame.Rect(219, 151, 71, 50))
    pygame.draw.rect(screen, BLACK, pygame.Rect(146, 202, 35, 50))
    pygame.draw.rect(screen, BLACK, pygame.Rect(38, 228, 106, 74))
    pygame.draw.rect(screen, BLACK, pygame.Rect(37, 301, 35, 24))
    pygame.draw.rect(screen, BLACK, pygame.Rect(38, 327, 106, 71))
    pygame.draw.rect(screen, BLACK, pygame.Rect(2, 351, 34, 50))
    pygame.draw.rect(screen, BLACK, pygame.Rect(184, 228, 108, 72))
    pygame.draw.rect(screen, BLACK, pygame.Rect(184, 327, 288, 71))
    pygame.draw.rect(screen, BLACK, pygame.Rect(326, 226, 327, 25))
    pygame.draw.rect(screen, BLACK, pygame.Rect(470, 302, 111, 73))
    pygame.draw.rect(screen, BLACK, pygame.Rect(327, 277, 252, 23))
    pygame.draw.rect(screen, BLACK, pygame.Rect(545, 4, 253, 96))
    pygame.draw.rect(screen, BLACK, pygame.Rect(545, 102, 106, 100))
    pygame.draw.rect(screen, BLACK, pygame.Rect(581, 202, 71, 25))
    pygame.draw.rect(screen, BLACK, pygame.Rect(617, 277, 35, 99))
    pygame.draw.rect(screen, BLACK, pygame.Rect(690, 102, 71, 150))
    pygame.draw.rect(screen, BLACK, pygame.Rect(690, 278, 71, 120))
    pygame.draw.rect(screen, BLACK, pygame.Rect(653, 326, 35, 73))
    pygame.draw.rect(screen, BLACK, pygame.Rect(146, 251, 38, 50))
    pygame.draw.rect(screen, BLACK, pygame.Rect(146, 326, 38, 75))
    pygame.display.flip()


# Puts the numbers in the boxes
def nums():
    # Down numbers
    draw_text("1", nums_font, text_col, 4, 1)
    draw_text("3", nums_font, text_col, 112, 1)
    draw_text("5", nums_font, text_col, 293, 26)
    draw_text("7", nums_font, text_col, 510, 1)
    draw_text("9", nums_font, text_col, 655, 100)
    draw_text("11", nums_font, text_col, 582, 250)
    draw_text("13", nums_font, text_col, 762, 100)
    # Across numbers
    draw_text("2", nums_font, text_col, 4, 200)
    draw_text("4", nums_font, text_col, 112, 26)
    draw_text("6", nums_font, text_col, 221, 125)
    draw_text("8", nums_font, text_col, 184, 200)
    draw_text("10", nums_font, text_col, 75, 300)
    draw_text("12", nums_font, text_col, 292, 250)
    draw_text("14", nums_font, text_col, 473, 375)


# def text_box():
#     textbox_rect = pygame.Rect(106, 405, 220, 25)
#     textbox_text = ""
#     textbox_active = False
#     while True:
#         screen.fill((0, 0, 0))
#
#         # Handle events
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if textbox_rect.collidepoint(event.pos):
#                     textbox_active = not textbox_active
#                 else:
#                     textbox_active = False
#             elif event.type == pygame.KEYDOWN:
#                 if textbox_active:
#                     if event.key == pygame.K_RETURN:
#                         if textbox_text in correct_words:
#                             print("Text entered:", textbox_text)
#                             textbox_text = ""
#                         else:
#                             textbox_text = ""
#                     elif event.key == pygame.K_BACKSPACE:
#                         textbox_text = textbox_text[:-1]
#                     else:
#                         textbox_text += event.unicode
#
#         # Draw textbox
#         pygame.draw.rect(screen, (255, 255, 255), textbox_rect, 2)
#         text_surface = little_font.render(textbox_text, True, BLACK)
#         screen.blit(text_surface, (textbox_rect.x + 5, textbox_rect.y + 5))

def draw_words(text):
    if text == correct_words[0]:
        show_image1 = True
        print("do we get here")
    elif text == correct_words[1]:
        c_img
    pygame.display.update()

# Game variables
run = True
menu = True
game = False
rules = False

textbox_rect = pygame.Rect(106, 405, 220, 25)
textbox_text = ""
textbox_active = False
show_image1 = False
show_image2 = False


# Game loop
while run:

    # Menu screen
    if menu:

        # Menu caption
        pygame.display.set_caption("Crossword Puzzle Menu!")
        # Background color
        screen.fill((255, 255, 255))
        # Title text
        draw_text("Crossword Puzzle", main_font, text_col, 115, 50)
        # Start button pressed -> game menu
        if start_button.draw():
            print("start button pressed")
            game = True
            menu = False
        # Rules button pressed -> rules menu
        if rules_button.draw():
            print("rules button pressed")
            rules = True
            menu = False
        # Exit button pressed -> exit game
        if exit_button.draw():
            print("exit button pressed")
            run = False
        # Exits if escape or x is hit
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            elif event.type == pygame.QUIT:
                run = False

    # Game screen
    if game:

        # Caption at the top
        pygame.display.set_caption("Crossword Puzzle!")
        screen.fill((0, 0, 0))
        #UI_REFRESH_RATE = CLOCK.tick(60)/1000
        # Draw the grid
        draw_background()
        # text_box()
        # Draw either blank board or filled in board
        draw_letters()
        # Draws hints at the bottom of the screen
        hints()
        # Get mouse position
        mpos = pygame.mouse.get_pos()
        # Grid numbers
        nums()
        # Black squares
        squares()
        #text_box()
        #print(mpos)
        # getting_words()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(mpos)
                if textbox_rect.collidepoint(event.pos):
                    textbox_active = not textbox_active
                else:
                    textbox_active = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = False
                    menu = True
                if textbox_active:
                    if event.key == pygame.K_RETURN:
                        if textbox_text in correct_words:
                            draw_words(textbox_text)
                            print("Text entered:", textbox_text)
                            textbox_text = ""
                        else:
                            textbox_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        textbox_text = textbox_text[:-1]
                    else:
                        textbox_text += event.unicode
            elif event.type == pygame.QUIT:
                pygame.quit()
            draw_words(textbox_text)
            if show_image1:
                screen.blit(ff_img, (4, 3))
                print("blitted")
            if show_image2:
                screen.blit(c_img, (50, 60))

    # Draw textbox
        pygame.draw.rect(screen, (0, 0, 0), textbox_rect, 2)
        text_surface = little_font.render(textbox_text, True, BLACK)
        screen.blit(text_surface, (textbox_rect.x + 5, textbox_rect.y + 5))

        # Update display
        pygame.display.flip()

    # Rules button pressed
    if rules:
        screen.fill((WHITE))
        # Draws the rules to the screen
        rules_board()
        # Rules caption
        pygame.display.set_caption("Crossword Puzzle Rules!")
        for event in pygame.event.get():
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rules = False
                    menu = True
            elif event.type == pygame.QUIT:
                run = False

    pygame.display.update()

pygame.quit()
