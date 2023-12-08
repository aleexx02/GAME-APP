'''
CIS 350 Fall 2023
Leah Barnes
Crossword Puzzle
'''
# Import pygame and button class
import pygame
# import button
import pygame_gui
from PIL import Image

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

CLOCK = pygame.time.Clock()


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
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
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
new_ff = pygame.transform.scale(ff_img, (33, 346))

cars_img = pygame.image.load('words/cars.png').convert_alpha()
new_cars = pygame.transform.scale(cars_img, (139, 23))

starwars_image = pygame.image.load('words/starwars.png').convert_alpha()
new_star = pygame.transform.scale(starwars_image, (33, 223))

titanic_img = pygame.image.load('words/titanic.png').convert_alpha()
new_titanic = pygame.transform.scale(titanic_img, (251, 23))

int_img = pygame.image.load('words/interstellar.png').convert_alpha()
new_int = pygame.transform.scale(int_img, (34, 298))

robot_img = pygame.image.load('words/irobot.png').convert_alpha()
new_robot = pygame.transform.scale(robot_img, (250, 23))

bee_img = pygame.image.load('words/bee.png').convert_alpha()
new_bee = pygame.transform.scale(bee_img, (34, 220))

oppen_img = pygame.image.load('words/oppen.png').convert_alpha()
new_oppen = pygame.transform.scale(oppen_img, (396, 23))

toy_img = pygame.image.load('words/toy.png').convert_alpha()
new_toy = pygame.transform.scale(toy_img, (34, 223))

martian_img = pygame.image.load('words/martian.png').convert_alpha()
new_martian = pygame.transform.scale(martian_img, (396, 23))

barbie_img = pygame.image.load('words/Barbie.png').convert_alpha()
new_barbie = pygame.transform.scale(barbie_img, (34, 147))

blonde_img = pygame.image.load('words/blonde.png').convert_alpha()
new_blonde = pygame.transform.scale(blonde_img, (504, 25))

avengers_img = pygame.image.load('words/avengers.png').convert_alpha()
new_avengers = pygame.transform.scale(avengers_img, (34, 296))

shrek_img = pygame.image.load('words/shrek.png').convert_alpha()
new_shrek = pygame.transform.scale(shrek_img, (177, 23))


pngs = [new_ff, new_cars, new_star, new_titanic, new_int, new_robot,
        new_bee, new_oppen, new_toy, new_martian, new_barbie,
        new_blonde, new_avengers, new_shrek]

coords = [(4, 3), (4, 202), (110, 4), (110, 27), (291, 27), (220, 127),
          (509, 4), (183, 202), (654, 102), (75, 302), (582, 251),
          (292, 253), (763, 103), (473, 376)]

already_used = []

correct_words = ["Fantastic Four", "Cars", "Star Wars", "Titanic",
                 "Interstellar", "I,Robot", "Bee Movie", "Oppenheimer",
                 "Toy Story", "The Martian", "Barbie", "Legally Blonde",
                 "The Avengers",
                 "Shrek"]


# When text is used, call this method to put the words on the screen


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# The function for creating the grid
def draw_background():
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, BLACK, pygame.Rect(1, 1, 798, 400), 3)
    i = 1
    j = 1
    while (i * 36.2) < 800:  # Creates the vertical lines on the screen
        pygame.draw.line(screen, BLACK, pygame.Vector2((i * 36.2) + 1, 1),
                         pygame.Vector2((i * 36.2) + 1, 400), 3)
        i += 1

    while (j * 25) < 400:  # Creates the horizontal lines on the screen
        pygame.draw.line(screen, BLACK, pygame.Vector2(798, (j * 25) + 1),
                         pygame.Vector2(1, (j * 25) + 1), 3)
        j += 1

# Blank board for the user to start with a blank screen
blank_board = [[0 for x in range(23)] for y in range(16)]

# Correct board to compare the user's inputs with the correct answers
correct_board = [
    ['F', ' ', ' ', 'S', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['A', ' ', ' ', 'T', 'I', 'T', 'A', 'N', 'I', 'C', ' ',
     ' ', ' ', ' ', 'E', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['N', ' ', ' ', 'A', ' ', ' ', ' ', ' ', 'N', ' ', ' ',
     ' ', ' ', ' ', 'E', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['T', ' ', ' ', 'R', ' ', ' ', ' ', ' ', 'T', ' ', ' ',
     ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['A', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'E', ' ', ' ',
     ' ', ' ', ' ', 'M', ' ', ' ', ' ', 'T', ' ', ' ', 'T'],
    ['S', ' ', ' ', 'W', ' ', ' ', 'I', ',', 'R', 'O', 'B',
     'O', 'T', ' ', 'O', ' ', ' ', ' ', 'O', ' ', ' ', 'H'],
    ['T', ' ', ' ', 'A', ' ', ' ', ' ', ' ', 'S', ' ', ' ',
     ' ', ' ', ' ', 'V', ' ', ' ', ' ', 'Y', ' ', ' ', 'E'],
    ['I', ' ', ' ', 'R', ' ', ' ', ' ', ' ', 'T', ' ', ' ',
     ' ', ' ', ' ', 'I', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['C', 'A', 'R', 'S', ' ', 'O', 'P', 'P', 'E', 'N', 'H',
     'E', 'I', 'M', 'E', 'R', ' ', ' ', 'S', ' ', ' ', 'A'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'L', ' ', ' ',
     ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', ' ', 'V'],
    ['F', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'L', 'E', 'G',
     'A', 'L', 'L', 'Y', ' ', 'B', 'L', 'O', 'N', 'D', 'E'],
    ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'A', ' ', ' ',
     ' ', ' ', ' ', ' ', ' ', 'A', ' ', 'R', ' ', ' ', 'N'],
    ['U', ' ', 'T', 'H', 'E', ' ', 'M', 'A', 'R', 'T', 'I',
     'A', 'N', ' ', ' ', ' ', 'R', ' ', 'Y', ' ', ' ', 'G'],
    ['R', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', 'E'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' ', ' ', ' ', ' ', 'I', ' ', ' ', ' ', ' ', 'R'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' ', 'S', 'H', 'R', 'E', 'K', ' ', ' ', ' ', 'S']
]

# Draws either the correct board or the blank board function to the screen,
# whichever is chosen


# def draw_letters():
#     row = 0
#     h_offset = 15
#     while row < 16:
#         col = 0
#         while col < 22:
#             output = blank_board[row][col]
#             # output = correct_board[row][col]
#             l_text = little_font.render(str(output), True, BLACK)
#             screen.blit(l_text, pygame.Vector2((col * 36.2) + h_offset,
#                                                (row * 25)))
#             col += 1
#         row += 1


# Draws the rules to the screen


def rules_board():
    draw_text("Rules:", main_font, text_col, 299, 50)
    draw_text("1: Spaces", little_font, text_col, 10, 150)
    draw_text("- #1, #3, #7, #9, #10, #12 and #13 have spaces"
              " in the name, include it.", hint_font, text_col, 30, 180)
    draw_text("2: Commas", little_font, text_col, 10, 200)
    draw_text("- #6 has a comma instead of a space. Include the"
              " comma, exclude the space.", hint_font, text_col, 30, 230)
    draw_text("3: Buttons", little_font, text_col, 10, 250)
    draw_text("- 'Start' button:", hint_font, text_col, 30, 280)
    draw_text("Takes you into the game, to the puzzle board. Hit"
              " escape to go back to main menu.", hint_font, text_col, 50, 300)
    draw_text("- 'Rules' button:", hint_font, text_col, 30, 320)
    draw_text("You are here...takes you to the game rules. Hit escape"
              " to go back to main menu.", hint_font, text_col, 50, 340)
    draw_text("- 'Exit' button:", hint_font, text_col, 30, 360)
    draw_text("Will exit out of the game completely.", hint_font,
              text_col, 50, 380)
    draw_text("- Escape key:", hint_font, text_col, 30, 400)
    draw_text("Will take you back to the menu from rules or start."
              " Exits completely in main menu.", hint_font, text_col, 50, 420)
    draw_text("- X in the top right:", hint_font, text_col, 30, 440)
    draw_text("Exits the game completely from whichever menu you are"
              " in.", hint_font, text_col, 50, 460)

# Draws the hints to the start screen


def hints():
    # Down hints
    draw_text("Hints", hint_font, text_col, 20, 400)
    draw_text("Down:", smaller_hint, text_col, 30, 420)
    draw_text("1: A space station crew is espoxed to a myserious cosmic",
              smaller_hint, text_col, 35, 435)
    draw_text("storm, giving them powers.", smaller_hint,
              text_col, 35, 450)
    draw_text("3: Set a long time ago in a galaxy far, far away",
              smaller_hint, text_col, 35, 465)
    draw_text("5: Astronauts travel through a wormhole looking for a",
              smaller_hint, text_col, 35, 480)
    draw_text("new home for humankind", smaller_hint, text_col, 35, 495)
    draw_text("7: After an adenture outside the hive, he finds out",
              smaller_hint, text_col, 35, 510)
    draw_text("humans eat honey and sues them for it", smaller_hint,
              text_col, 35, 525)
    draw_text("9: Toys come to life when the owner isn't around",
              smaller_hint, text_col, 35, 540)
    draw_text("11: Doll has crisis about dreamhouse and journies away",
              smaller_hint, text_col, 35, 555)
    draw_text("13: A group of extraordinary individuals who were",
              smaller_hint, text_col, 35, 570)
    draw_text("assembled to defeat Loki and his army in New York",
              smaller_hint, text_col, 35, 585)
    # Across hints
    draw_text("Across:", smaller_hint, text_col, 420, 420)
    draw_text("2: Hotshot rookie racecar gets stranded in a little town",
              smaller_hint, text_col, 420, 435)
    draw_text("and learns that winning isn't everything", smaller_hint,
              text_col, 420, 450)
    draw_text("4: a 17 y/o aristocrat falls in love with a kind but poor",
              smaller_hint, text_col, 420, 465)
    draw_text("artist aboard a ship", smaller_hint, text_col, 420, 480)
    draw_text("6: A detective investigates an alleged suicide of a ",
              smaller_hint, text_col, 420, 495)
    draw_text("scientist beliving it was a murder, and uncovers a secret",
              smaller_hint, text_col, 420, 510)
    draw_text("8: Follows the Manhattan Project during WWII", smaller_hint,
              text_col, 420, 525)
    draw_text("10: An astronaut gets stranded on Mars after a storm",
              smaller_hint, text_col, 420, 540)
    draw_text("knocked him from his team. Now, he awaits to be rescued",
              smaller_hint, text_col, 420, 555)
    draw_text("12: A sorority girl follows ex to Haravd to win him back",
              smaller_hint, text_col, 420, 570)
    draw_text("14: A green ogre goes on a quest to save the princess",
              smaller_hint, text_col, 420, 585)

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


def combine_background():
    pygame.display.set_caption("Crossword Puzzle!")
    screen.fill((WHITE))
    draw_background()
    # draw_letters()
    squares()
    nums()
    hints()
    pygame.draw.rect(screen, (0, 0, 0), textbox_rect, 2)
    text_surface = little_font.render(textbox_text, True, BLACK)
    screen.blit(text_surface, (textbox_rect.x + 5, textbox_rect.y))
    if 'Fantastic Four' in already_used:
        screen.blit(new_ff, (4, 3))
    if 'Cars' in already_used:
        screen.blit(new_cars, (4, 202))
    if 'Star Wars' in already_used:
        screen.blit(new_star, (110, 2))
    if 'Titanic' in already_used:
        screen.blit(new_titanic, (112, 27))
    if 'Interstellar' in already_used:
        screen.blit(new_int, (291, 27))
    if 'I,Robot' in already_used:
        screen.blit(new_robot, (220, 127))
    if 'Bee Movie' in already_used:
        screen.blit(new_bee, (509, 4))
    if 'Oppenheimer' in already_used:
        screen.blit(new_oppen, (183, 202))
    if 'Toy Story' in already_used:
        screen.blit(new_toy, (654, 102))
    if 'The Martian' in already_used:
        screen.blit(new_martian, (75, 302))
    if 'Barbie' in already_used:
        screen.blit(new_barbie, (582, 251))
    if 'Legally Blonde' in already_used:
        screen.blit(new_blonde, (292, 253))
    if 'The Avengers' in already_used:
        screen.blit(new_avengers, (763, 103))
    if 'Shrek' in already_used:
        screen.blit(new_shrek, (473, 376))
    if word_num == 0:
        screen.fill(WHITE)
        draw_text("You have completed the game!",
                  little_font, text_col, 200, 200)


def print_pics(text):
    for i in correct_words:
        if text == i:
            if text not in already_used:
                already_used.append(i)
                return False
            else:
                print("Word has already been used")
                return True
            # for i in already_used:
            #     pass
            print('already used: ', already_used)


# Game variables
run = True
menu = True
game = False
rules = False

textbox_rect = pygame.Rect(106, 405, 220, 25)
textbox_text = ""
textbox_active = False
word_num = 14

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
        else:
            complete = True

        # Exits if escape or x is hit
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            elif event.type == pygame.QUIT:
                run = False

    # Game screen
    if game:
        combine_background()
        CLOCK.tick(60)/1000
        mpos = pygame.mouse.get_pos()
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
                    # text()
                    if event.key == pygame.K_RETURN:
                        if textbox_text in correct_words:
                            print(word_num)
                            word_num -= 1
                            print(word_num)
                            print_pics(textbox_text)
                            if word_num == 0:
                                print("over")
                            print("Text entered:", textbox_text)
                            if textbox_text == correct_words[0]:
                                show_image1 = True
                            if textbox_text == correct_words[1]:
                                show_image2 = True
                            textbox_text = ""
                        else:
                            textbox_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        textbox_text = textbox_text[:-1]
                    else:
                        textbox_text += event.unicode
            elif event.type == pygame.QUIT:
                run = False
                pygame.quit()

    # Rules button pressed
    if rules:
        screen.fill((WHITE))
        # Draws the rules to the screen
        rules_board()
        # Rules caption
        pygame.display.set_caption("Crossword Puzzle Rules!")
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rules = False
                    menu = True
            elif event.type == pygame.QUIT:
                run = False

    pygame.display.update()

pygame.quit()
