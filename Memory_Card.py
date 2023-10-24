import pygame
import sys
import random

# Initialize pygame library
pygame.init()
pygame.font.init()

# set up the display of the home screen of the game
home_screen_height = 600
home_screen_width = 600
home_screen = pygame.display.set_mode((home_screen_height, home_screen_width))
pygame.display.set_caption("Card Match Game")
menu_options = ["Play Game", "Settings", "Quit"]
selected_option = 0  # to keep track of the selected option of the player.
game_state = "Menu"  # initial game state.
N = 6  # number of DIFFERENT CARDS. Total number of cards will be N*2.
DELAY = 400
# set up the grid for the game (where cards will be)
grid_width = 600
grid_height = 600
grid_size = (3, 4)  # 3*4 grid.
card_size = grid_width // grid_size[1], grid_height // grid_size[0]  # size of each card.
card_back = pygame.image.load("card_back.jpg")
# rescale image to fit the screen:
card_back = pygame.transform.scale(card_back, (grid_width // grid_size[1], grid_height // grid_size[0]))
card_images = []  # to store the cards for the game.
# Will start by loading the images of my N different cards.
for i in range(N):
    image = pygame.image.load(f"card_{i}.jpg")  # to go over all images of the cards.
    # rescale images of cards to fit the screen:
    image = pygame.transform.scale(image, (grid_width // grid_size[1], grid_height // grid_size[0]))
    card_images.append(image)
card_images *= 2  # duplicate the list to have 2 of each card.
random.shuffle(card_images)  # randomly shuffle the cards in the list.
card_up = [False] * len(card_images)  # all cards are face down at first.
selected_cards = []  # store indexes of selected cards and be able to compare them later.
matches = 0  # will store the correct matches of the player.

black = (0, 0, 0)  # black color.
white = (255, 255, 255)  # white color.
light_blue = (0, 180, 190)  # blue color.
light_pink = (255, 182, 193)
pink = (255, 20, 150)
yellow = (255, 255, 80)
menu_font = pygame.font.SysFont("Elephant", 43)  # define the font size of menu
# store the state of each keyboard key inside the vector 'keys'.
# Each element in the vector will correspond to a key in the keyboard.
# If value is 1 --> key is pressed. If value is 0 --> key is not pressed.
# To check if key W is pressed --> keys[pygame.K_w] and check if it's 1 or 0.
keys = pygame.key.get_pressed()

# Function to display the Game Menu:
def display_menu(screen, menu_options, selected_option):
    screen.fill(pink)
    for i, option in enumerate(menu_options):
        # this will go through all items in menu_options array and store the index of each one of them in i.
        # the render() method is used to create a surface object from the text (surface containing that text).
        # render the text into a surface:
        text = menu_font.render(option, True, light_pink)
        # get_rect creates a rectangle from the surface containing this text:
        text_rect = text.get_rect(center=(home_screen_width // 2, (i + 1) * 150))
        # each option written in the menu screen will be located at these center coordinates.
        if i == selected_option:  # the current option selected by the player.
            pygame.draw.rect(screen, white, text_rect,
                             4)  # draw a rectangle surrounding the option selected by the user.
        screen.blit(text,
                    text_rect)  # this is to copy the contents from the 'text' surface into the menu_screen (screen) surface at the rectangle location('text_rect').


# function to display the main game.
def display_game(screen):
    screen.fill(light_pink)
    # Display cards on the grid FACEDOWN:
    for x in range(grid_size[1]):  # x: column in the grid.
        for y in range(grid_size[0]):  # y: row in the grid.
            # get_rect creates a rectangle from the surface containing this image (card):
            card_rect = card_back.get_rect()  # obtain rectangle object with same dimensions as the card image (card_back).
            # to specify the position of this rectangle, use 'topleft' which specifies the top-left corner position of the card image.
            card_rect.topleft = (x * card_size[0], y * card_size[
                1])  # card_size[0] = width of each card; card_size[1] = height of each card.
            screen.blit(card_back,
                        card_rect)  # actual drawing (copy) of the card image (card_back) into the game screen (screen), at the rectangle('card_rect') location.


def obtain_pos():  # obtain position of cards on the grid; will return a list of rectangles representing the cards.
    cards = []  # to store all rectangles that represent cards.
    for x in range(grid_size[1]):  # x: column in the grid.
        for y in range(grid_size[0]):  # y: row in the grid.
            index = x + (y * grid_size[1])  # to get the index of each card in the grid.
            card = card_images[index]  # we get the corresponding card from the card list.
            # get_rect creates a rectangle from the surface containing this image (card):
            card_rect = card.get_rect()  # obtain rectangle object with same dimensions as the card image.
            # to specify the position of this rectangle, use 'topleft' which specifies the top-left corner position of the card image.
            card_rect.topleft = (x * card_size[0], y * card_size[
                1])  # card_size[0] = width of each card; card_size[1] = height of each card.
            cards.append(card_rect)
            # screen.blit(card, card_rect) # actual drawing (copy) of the card image (card) into the game screen (screen), at the rectangle('card_rect') location.
    return cards


cards = obtain_pos()  # list of rectangles representing the cards.


def display_card(index):  # to flip the card selected by the user.
    card = card_images[index]
    card_rect = cards[index]  # get corresponding card's rectangle.
    home_screen.blit(card, card_rect)  # drawing the card on the position defined by the rectangle 'card_rect'.

# 2 main events:
# KEYDOWN: player presses a key from the keyboard.
# QUIT: display screen closure.
def start_memory_game(): #Put main game loop in a function to avoid error with menu - Natalie
    # MAIN GAME LOOP: run until player decides to quit the game
    global selected_option, game_state, home_screen, matches, selected_cards #Added to prevent errors with menu - Natalie
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # exits loop and so, exits game.
            elif event.type == pygame.KEYDOWN:  # the player presses a key.
                if event.key == pygame.K_ESCAPE:
                    # the player presses the key 'esc' on the top left corner of the keyboard, it exits the game.
                    running = False
                if game_state == "Menu":  # we are in the Menu Screen.
                    if event.key == pygame.K_UP:  # pointing up arrow.
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:  # press the 'Enter' key.
                        if selected_option == 0:  # START GAME
                            game_state = "Play"
                        elif selected_option == 1:  # SETTINGS
                            game_state = "Settings"
                        elif selected_option == 2:  # QUIT
                            running = False

                elif game_state == "Play":  # we are in the Game Screen.
                    ...
                    # handle the game specific input (KEYBOARD INPUT) while in the game state

            elif event.type == pygame.MOUSEBUTTONDOWN:  # player hits the mouse button.
                if game_state == "Menu":  # MENU SCREEN.
                    ...  # handle the menu specific input (MOUSE INPUT).
                elif game_state == "Play":  # GAME SCREEN.
                    mouse_position = pygame.mouse.get_pos()  # get position of the click of the mouse.
                    for i, card_rect in enumerate(cards):
                        if not card_up[i] and card_rect.collidepoint(mouse_position):
                            # if card is faced down and the mouse is on that card.
                            if len(selected_cards) < 2:  # only possible to choose 2 cards maximum.
                                card_up[i] = True  # turn the card face up.
                                selected_cards.append(i)

        # When no event occurs (when open the game):
        if game_state == "Menu":
            display_menu(home_screen, menu_options, selected_option)
        # when the player is playing, we display other screen.
        elif game_state == "Play":
            display_game(home_screen)
            for i, card_rect in enumerate(cards):  # if the card was selected --> need to turn it around.
                if card_up[i]:  # this means card was selected.
                    # need to turn the card face up.
                    display_card(i)

            if len(selected_cards) == 2:  # two cards have been selected --> compare them.
                card1 = card_images[selected_cards[0]]  # store image of first card selected in 'card1'.
                card2 = card_images[selected_cards[1]]  # store image of second card selected in 'card2'.
                if card1 == card2:  # CARDS MATCH.
                    matches = matches + 1  # add one match more.

                else:  # CARDS DON'T MATCH.
                    pygame.display.flip()  # to update the screen.
                    pygame.time.delay(DELAY)  # so the player can see the cards.
                    card_up[selected_cards[0]] = False  # flip the card back.
                    card_up[selected_cards[1]] = False  # flip the card back.
                selected_cards = []  # reset the selected cards list.

            if matches == N:  # when all cards have been
                home_screen.fill(black)
                message = "You won!!"
                text = menu_font.render("You won!!", True, light_pink)
                # get_rect creates a rectangle from the surface containing this text:
                text_rect = text.get_rect(center=(home_screen_width // 2, (i + 1) * 150))
                home_screen.blit(text,
                                 text_rect)  # this is to copy the contents from the 'text' surface into the menu_screen (screen) surface at the rectangle location('text_rect').
        pygame.display.flip()
    pygame.quit()

# # Cargar imágenes de cartas
# card_back = pygame.image.load("card_backward.jpg")  # Reemplaza "card_back.png" con tu propia imagen
# card_front = pygame.image.load("card_forward.jpg")  # Reemplaza "card_front.png" con tu propia imagen

# # Crear una lista de cartas
# cards = [card_front, card_front, card_front, card_front]

# # Barajar las cartas
# random.shuffle(cards)

# # Tamaño de las cartas
# card_width = 100
# card_height = 150

# # Posiciones de las cartas
# card_positions = [(100, 100), (250, 100), (400, 100), (550, 100)]

# # Lista para mantener el estado de las cartas (volteadas o no)
# card_state = [False, False, False, False]

# # Bucle principal del juego
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Comprobar clic izquierdo del mouse
#             # Comprobar si se hizo clic en una carta
#             for i, pos in enumerate(card_positions):
#                 x, y = pos
#                 if x <= event.pos[0] <= x + card_width and y <= event.pos[1] <= y + card_height:
#                     # Voltear la carta si no está volteada
#                     if not card_state[i]:
#                         card_state[i] = True


#     # Dibujar las cartas en la ventana (volteadas o boca abajo)
#     for i, pos in enumerate(card_positions):
#         x, y = pos
#         if card_state[i]:
#             window.blit(cards[i], (x, y))
#         else:
#             window.blit(card_back, (x, y))

#     # Actualizar la ventana
#     pygame.display.flip()

# # Salir de Pygame
# pygame.quit()
# sys.exit()