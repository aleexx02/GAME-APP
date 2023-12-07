import pygame
import sys
import random


# Initialize pygame library
pygame.init()
pygame.font.init()

# set up the display of the home screen of the game
home_screen_height = 600
home_screen_width = 600
home_screen = pygame.display.set_mode((home_screen_height,home_screen_width))
pygame.display.set_caption("Card Match Game")
menu_options = ["Play Game", "Settings", "Game Rules", "Quit"]
game_levels = ["Easy", "Medium", "Hard", "Game Menu", "Exit Game"]
settings = ["Restart Game", "Select Level", "Game Menu", "Exit Game"]
selected_option = 0 # to keep track of the selected option of the player (MENU SCREEN).
selected_level = 0 # to keep track of the selected option of the player (GAME SCREEN).
selected_setting = 0 # to keep track of the selected option of the player (SETTINGS SCREEN).
game_state = "Menu" # initial game state.
game_level = "None" # initial game level.
setting_option = "Settings"
# set up the grid for the game (where cards will be)
grid_width = 550
grid_height = 600
card_back = pygame.image.load("card_back.jpg")
selected_cards = [] # store indexes of selected cards and be able to compare them later.
matches = 0 # will store the correct matches of the player.
x = 0 # to keep track of game.
# Colors and Fonts:
black = (0,0,0) # black color.
light_pink = (255, 182, 193)
pink = (255, 20, 150)
white = (255,255,255)
menu_font = pygame.font.SysFont("Elephant", 43) # define the font size of menu
game_font = pygame.font.SysFont("Californian FB", 35)
font1 = pygame.font.SysFont("Bahnschrift", 40)
font2 = pygame.font.SysFont("Bahnschrift", 35)
font3 = pygame.font.SysFont("Bahnschrift", 20)

class Button_Image: # settings button; doesn't contain text but an image.
    def __init__(self, x, y, width, height, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image,(30,30))
        self.highlight_image = pygame.transform.scale(self.image, (width + 10, height + 10))
        self.is_highlighted = False

    def draw(self, surface, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            surface.blit(self.highlight_image, self.rect.topleft)
        else:
            surface.blit(self.image, self.rect.topleft)
    
    def click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

settings_button = Button_Image(grid_width + 10, 20, 20, 20, "settings_button.jpg" )



# Function to display the Game Menu:
def display_menu(screen,menu_options, selected_option, menu_font, game_font):
    screen.fill(light_pink)
    text = menu_font.render("Card Match Game",True, pink)
    # get_rect creates a rectangle from the surface containing this text:
    text_rect = text.get_rect(center=(home_screen_width//2, 110))
    screen.blit(text, text_rect)
    for i, option in enumerate(menu_options):
    # this will go through all items in menu_options array and store the index of each one of them in i.
        # the render() method is used to create a surface object from the text (surface containing that text).
        # render the text into a surface:
        text = game_font.render(option,True, black)
        # get_rect creates a rectangle from the surface containing this text:
        text_rect = text.get_rect(center=(home_screen_width//2, (i+2)*100)) 
        # each option written in the menu screen will be located at these center coordinates.
        if i == selected_option: # the current option selected by the player.
            pygame.draw.rect(screen, pink, text_rect, 2) #draw a rectangle surrounding the option selected by the user.
        screen.blit(text, text_rect) # this is to copy the contents from the 'text' surface into the menu_screen (screen) surface at the rectangle location('text_rect').
        
# Function to display the game rules:
def display_rules(screen, mouse_pos, font1, font3):
    screen.fill(light_pink)
    global settings_button
    text = font1.render("Memory Card Match Rules:",True, pink)
    text1 = font3.render("1. Select two cards.", True, black)
    text2 = font3.render("2. If both cards match, keep trying for another match.", True, black)
    text3 = font3.render("3. If both cards do not match, the cards are turned over again.", True, black)
    text4 = font3.render("4. You win once you have matched all cards.", True, black)
    text_rect = text.get_rect(center=(home_screen_width//2, 130))
    text_rect1 = text1.get_rect(center=(home_screen_width//5, 210))
    text_rect2 = text1.get_rect(center=(home_screen_width//5, 250))
    text_rect3 = text1.get_rect(center=(home_screen_width//5, 290))
    text_rect4 = text1.get_rect(center=(home_screen_width//5, 330))
    screen.blit(text, text_rect)
    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)
    screen.blit(text3, text_rect3)
    screen.blit(text4, text_rect4)
    settings_button.draw(screen, mouse_pos)


# Function to display the game levels:
def display_game_levels(screen, game_levels, selected_level, font1, game_font, font2):
    screen.fill(light_pink)
    text = font1.render("Choose a level:",True, pink)
    # get_rect creates a rectangle from the surface containing this text:
    text_rect = text.get_rect(center=(home_screen_width//2, 110))
    screen.blit(text, text_rect)
    for i, level in enumerate(game_levels):
    # this will go through all items in menu_options array and store the index of each one of them in i.
        # the render() method is used to create a surface object from the text (surface containing that text).
        # render the text into a surface:
        if level == "Easy" or level == "Medium" or level == "Hard":
            text1 = game_font.render(level,True, black) # for the levels.
            text_rect1 = text1.get_rect(center=(home_screen_width//2, (i+3)*60))
            if i == selected_level: # the current option selected by the player.
                pygame.draw.rect(screen, pink, text_rect1, 2) #draw a rectangle surrounding the option selected by the user.
            screen.blit(text1, text_rect1) # this is to copy the contents from the 'text1' surface into the menu_screen (screen) surface at the rectangle location('text_rect1').
        if level == "Game Menu" or level == "Exit Game":
            text2 = font2.render(level, True, pink) # for the "Game Menu" and "Exit Game" options.
            # get_rect creates a rectangle from the surface containing this text:
            text_rect2 = text2.get_rect(center=(home_screen_width//2, (i+3)*65))
            # each option written in the menu screen will be located at these center coordinates.
            if i == selected_level: # the current option selected by the player.
                pygame.draw.rect(screen, black, text_rect2, 2) #draw a rectangle surrounding the option selected by the user.
            screen.blit(text2, text_rect2) # this is to copy the contents from the 'text2' surface into the menu_screen (screen) surface at the rectangle location('text_rect2').

# Function to store the card images of the game into a list:
def cards_game(rows, columns, N) -> list: # modifies the list card_images to store the cards of the game.
    grid_size = (rows, columns)
    card_images = [] # to store the cards for the game.
    # Will start by loading the images of my N different cards.
    for i in range(N):
        image = pygame.image.load(f"card_{i}.jpg") # to go over all images of the cards.
        # rescale images of cards to fit the screen:
        image = pygame.transform.scale(image, (grid_width // grid_size[1],grid_height // grid_size[0]))
        card_images.append(image) 
    card_images *= 2 # duplicate the list to have 2 of each card.
    random.shuffle(card_images) # randomly shuffle the cards in the list.
    return card_images # length of card_images is N*2

card_images1 = cards_game(3,4,6) # rows = 3; columns = 4; N = 6 (12 cards) -> Easy Level.
card_images2 = cards_game(4,4,8)
card_images3 = cards_game(4,5,10)

# Function to display the main game:
def display_game(screen, rows, columns, mouse_pos):
    screen.fill(light_pink)
    global card_back # to be able to access the global variable.
    global settings_button
    grid_size = (rows, columns)
    card_size = grid_width // grid_size[1], grid_height // grid_size[0] # size of each card.
    # rescale image to fit the screen:
    card_back = pygame.transform.scale(card_back, (grid_width // grid_size[1],grid_height // grid_size[0]))
    # Display cards on the grid FACEDOWN:
    for x in range(columns): # x: column in the grid.
        for y in range(rows): # y: row in the grid.
            # get_rect creates a rectangle from the surface containing this image (card):
            card_rect = card_back.get_rect() # obtain rectangle object with same dimensions as the card image (card_back).
             # to specify the position of this rectangle, use 'topleft' which specifies the top-left corner position of the card image.
            card_rect.topleft = (x*card_size[0],y*card_size[1]) # card_size[0] = width of each card; card_size[1] = height of each card.
            screen.blit(card_back, card_rect) # actual drawing (copy) of the card image (card_back) into the game screen (screen), at the rectangle('card_rect') location. 
    settings_button.draw(screen, mouse_pos)


# Function to obtain position of each card in the grid:
def obtain_pos(rows, columns, card_images) -> list:    # obtain position of cards on the grid; will return a list of rectangles representing the cards.
    cards =[] # to store all rectangles that represent cards.
    grid_size = (rows, columns)
    card_size = grid_width // grid_size[1], grid_height // grid_size[0] # size of each card.
    for x in range(grid_size[1]): # x: column in the grid.
        for y in range(grid_size[0]): # y: row in the grid.
            index = x + (y * grid_size[1]) # to get the index of each card in the grid.
            card = card_images[index] # we get the corresponding card from the card list.
            # get_rect creates a rectangle from the surface containing this image (card):
            card_rect = card.get_rect() # obtain rectangle object with same dimensions as the card image.
            # to specify the position of this rectangle, use 'topleft' which specifies the top-left corner position of the card image.
            card_rect.topleft = (x*card_size[0],y*card_size[1]) # card_size[0] = width of each card; card_size[1] = height of each card.
            cards.append(card_rect)
    return cards # length of cards is N*2

cards1 = obtain_pos(3,4,card_images1)
cards2 = obtain_pos(4,4,card_images2)
cards3 = obtain_pos(4,5,card_images3)
card_up1 = [False] * len(card_images1) # all cards are face down at first.
card_up2 = [False] * len(card_images2) # all cards are face down at first.
card_up3 = [False] * len(card_images3) # all cards are face down at first.

# Function to display card (turn over a card selected by the user):
def display_card(home_screen,index, card_images, cards): # to flip the card selected by the user.
            card = card_images[index]
            card_rect = cards[index] # get corresponding card's rectangle.
            home_screen.blit(card, card_rect) # drawing the card on the position defined by the rectangle 'card_rect'.

# Function to display the settings screen:
def display_settings(screen, settings, selected_setting, menu_font, game_font):
    screen.fill(light_pink)
    text = menu_font.render("Settings",True, pink)
    # get_rect creates a rectangle from the surface containing this text:
    text_rect = text.get_rect(center=(home_screen_width//2, 110))
    screen.blit(text, text_rect)
    for i, setting in enumerate(settings):
    # this will go through all items in menu_options array and store the index of each one of them in i.
        # the render() method is used to create a surface object from the text (surface containing that text).
        # render the text into a surface:
        text = game_font.render(setting,True, black)
        # get_rect creates a rectangle from the surface containing this text:
        text_rect = text.get_rect(center=(home_screen_width//2, (i+2.7)*80)) 
        # each option written in the menu screen will be located at these center coordinates.
        if i == selected_setting: # the current option selected by the player.
            pygame.draw.rect(screen, pink, text_rect, 3) #draw a rectangle surrounding the option selected by the user.
        screen.blit(text, text_rect) # this is to copy the contents from the 'text' surface into the menu_screen (screen) surface at the rectangle location('text_rect').

# MAIN GAME LOOP: run until player decides to quit the game
running = True
# 2 main events:
# KEYDOWN: player presses a key from the keyboard.
# QUIT: display screen closure. 
while running:
    mouse_position = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # exits loop and so, exits game.
        elif event.type == pygame.KEYDOWN: # the player presses a key.
            if event.key == pygame.K_ESCAPE:
            # the player presses the key 'esc' on the top left corner of the keyboard, it exits the game.
                running = False
            if game_state == "Menu": # we are in the Menu Screen.
                if event.key == pygame.K_UP: # pointing up arrow.
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN: # press the 'Enter' key.
                    if selected_option == 0: # START GAME
                        game_state = "Play"
                    elif selected_option == 1: # SETTINGS
                        game_state = "Settings"
                    elif selected_option == 2: # GAME RULES
                        game_state = "Rules"
                    elif selected_option == 3: # QUIT
                        running = False

            elif game_state == "Play": # we are in the Game Screen.
            # handle the game specific input (KEYBOARD INPUT) while in the game state.
                if event.key == pygame.K_UP: # pointing up arrow.
                    selected_level = (selected_level - 1) % len(game_levels)
                elif event.key == pygame.K_DOWN:
                    selected_level = (selected_level + 1) % len(game_levels)
                elif event.key == pygame.K_RETURN: # press the 'Enter' key.
                    if selected_level == 0: # EASY LEVEL
                        game_level = "Easy"
                        game_state = "Play_Easy" # Easy Level Screen: N = 6 (12 cards) and DELAY = 400.
                    elif selected_level == 1: # MEDIUM LEVEL
                        game_level = "Medium"
                        game_state = "Play_Medium" # Medium Level Screen: N = 8 (16 cards) and DELAY = 300.
                    elif selected_level == 2: # HARD LEVEL
                        game_level = "Hard"
                        game_state = "Play_Hard" # Hard Level Screen: N = 10 (20 cards) and DELAY = 200.
                    elif selected_level == 3: 
                        game_state = "Menu" # Home screen (menu)
                    elif selected_level == 4: # Exit game
                        running = False
            elif game_state == "Settings":
                # handle the settings specific input (KEYBOARD INPUT) while in the settings state.
                if event.key == pygame.K_UP: # pointing up arrow.
                    selected_setting = (selected_setting - 1) % len(settings)
                elif event.key == pygame.K_DOWN:
                    selected_setting = (selected_setting + 1) % len(settings)
                elif event.key == pygame.K_RETURN: # press the 'Enter' key.
                    if selected_setting == 0: # RESTART GAME
                        game_state = "Restart Game"
                    elif selected_setting == 1: # Select Level
                        game_state = "Play"
                    elif selected_setting == 2: # Game Menu
                        game_state = "Menu"
                    elif selected_setting == 3: # Exit Game
                        running = False

        elif event.type == pygame.MOUSEBUTTONDOWN: # player hits the mouse button.
            mouse_position = pygame.mouse.get_pos() # get position of the click of the mouse.
            if game_state == "Menu": # MENU SCREEN.
                for i, option in enumerate(menu_options): # handle the menu specific input (MOUSE INPUT).
                    text = menu_font.render(option,True, light_pink)
                    option_rect = text.get_rect(center=(home_screen_width//2, (i+2)*100))
                    if option == "Play Game" and option_rect.collidepoint(mouse_position):
                        selected_option = 0
                        game_state = "Play"
                    elif option == "Settings" and option_rect.collidepoint(mouse_position):
                        selected_option = 1
                        game_state = "Settings"
                    elif option == "Game Rules" and option_rect.collidepoint(mouse_position):
                        selected_option = 2
                        game_state = "Rules"
                    elif option == "Quit" and option_rect.collidepoint(mouse_position):
                        selected_option = 3
                        running = False
            elif game_state == "Play": # GAME SCREEN.
                for i, level in enumerate(game_levels): # handle the game specific input (MOUSE INPUT).
                    text1 = game_font.render(level,True, light_pink) # for the levels.
                    level_rect1 = text1.get_rect(center=(home_screen_width//2, (i+3)*60))
                    text2 = font2.render(level, True, white) # for the "Game Menu" and "Exit Game" options.
                    level_rect2 = text2.get_rect(center=(home_screen_width//2, (i+3)*65))
                    if level == "Easy" and level_rect1.collidepoint(mouse_position):
                        selected_level = 0
                        game_level = "Easy"
                        game_state = "Play_Easy"
                    elif level == "Medium" and level_rect1.collidepoint(mouse_position):
                        selected_level = 1
                        game_level = "Medium"
                        game_state = "Play_Medium"
                    elif level == "Hard" and level_rect1.collidepoint(mouse_position):
                        selected_level = 2
                        game_level = "Hard"
                        game_state = "Play_Hard"
                    elif level == "Game Menu" and level_rect2.collidepoint(mouse_position):
                        selected_level = 3
                        game_state = "Menu" # display the menu screen.
                    elif level == "Exit Game" and level_rect2.collidepoint(mouse_position):
                        selected_level = 4
                        running = False
            
            elif game_state == "Play_Easy":
                for i, card_rect in enumerate(cards1):
                    if not card_up1[i] and card_rect.collidepoint(mouse_position):
                    # if card is faced down and the mouse is on that card.
                        if len(selected_cards) < 2: # only possible to choose 2 cards maximum. 
                            card_up1[i] = True # turn the card face up.
                            selected_cards.append(i)
                if settings_button.click(mouse_position):
                    game_state = "Settings"

            elif game_state == "Play_Medium":
                for i, card_rect in enumerate(cards2):
                    if not card_up2[i] and card_rect.collidepoint(mouse_position):
                    # if card is faced down and the mouse is on that card.
                        if len(selected_cards) < 2: # only possible to choose 2 cards maximum. 
                            card_up2[i] = True # turn the card face up.
                            selected_cards.append(i)
                if settings_button.click(mouse_position):
                    game_state = "Settings"

            elif game_state == "Play_Hard":
                for i, card_rect in enumerate(cards3):
                    if not card_up3[i] and card_rect.collidepoint(mouse_position):
                    # if card is faced down and the mouse is on that card.
                        if len(selected_cards) < 2: # only possible to choose 2 cards maximum. 
                            card_up3[i] = True # turn the card face up.
                            selected_cards.append(i)
                if settings_button.click(mouse_position):
                    game_state = "Settings"
            elif game_state == "Rules":
                if settings_button.click(mouse_position):
                    game_state = "Settings"
            elif game_state == "Settings": # SETTINGS SCREEN.
            # handle the settings specific input (mouse input).
                for i, setting in enumerate(settings): # handle the menu specific input (MOUSE INPUT).
                    text = font1.render(setting,True, light_pink)
                    setting_rect = text.get_rect(center=(home_screen_width//2, (i+2.7)*80))
                    if setting == "Restart Game" and setting_rect.collidepoint(mouse_position):
                        selected_setting = 0
                        game_state = "Restart Game"
                    elif setting == "Select Level" and setting_rect.collidepoint(mouse_position):
                        selected_setting = 1
                        x = 1
                        game_state = "Play"
                    elif setting == "Game Menu" and setting_rect.collidepoint(mouse_position):
                        selected_setting = 2
                        game_state = "Menu"
                    elif setting == "Exit Game" and setting_rect.collidepoint(mouse_position):
                        selected_setting = 3
                        running = False


    # When no event occurs (when open the game):
    if game_state == "Menu":
        display_menu(home_screen,menu_options,selected_option, menu_font, game_font)

    elif game_state == "Play":
        # display game settings: choose the level of the game.
        display_game_levels(home_screen, game_levels, selected_level,font1, game_font, font2)
        x = 1
    elif game_state == "Play_Easy":
        if x == 1:
            card_images1 = cards_game(3,4,6) # rows = 3; columns = 4; N = 6 (12 cards) -> Easy Level.
            cards1 = obtain_pos(3,4,card_images1)
            card_up1 = [False] * len(card_images1) # all cards are face down at first.
            x = 0
        display_game(home_screen, 3, 4, mouse_position)
        for i, card_rect in enumerate(cards1): # if the card was selected --> need to turn it around.
            if card_up1[i]: #this means card was selected.
            # need to turn the card face up.
                display_card(home_screen,i, card_images1,cards1)
        if len(selected_cards) == 2: # two cards have been selected --> compare them.
            card1 = card_images1[selected_cards[0]] # store image of first card selected in 'card1'.
            card2 = card_images1[selected_cards[1]] # store image of second card selected in 'card2'.
            if card1 == card2: # CARDS MATCH.
                matches = matches + 1 # add one match more.
            else: # CARDS DON'T MATCH.
                pygame.display.flip() # to update the screen.
                pygame.time.delay(500) # so the player can see the cards. Easy Level DELAY: 400.
                card_up1[selected_cards[0]] = False # flip the card back.
                card_up1[selected_cards[1]] = False # flip the card back.
            selected_cards = [] # reset the selected cards list.
        if matches == 6: # when all cards have been 
            home_screen.fill(light_pink)
            message = "You won!!!"
            text = menu_font.render(message,True, black)
            # get_rect creates a rectangle from the surface containing this text:
            text_rect = text.get_rect(center=(home_screen_width//2, home_screen_height//2))
            home_screen.blit(text, text_rect) # this is to copy the contents from the 'text' surface into the menu_screen (screen) surface at the rectangle location('text_rect').
            settings_button.draw(home_screen, mouse_position)
            pygame.display.flip() # to update the screen.
            pygame.time.delay(300) # so the player can see the cards. Easy Level DELAY: 400.


    elif game_state == "Play_Medium":
        if x == 1:
            card_images2 = cards_game(4,4,8)
            cards2 = obtain_pos(4,4,card_images2)
            card_up2 = [False] * len(card_images2) # all cards are face down at first.
            x = 0
        display_game(home_screen, 4, 4, mouse_position)
        for i, card_rect in enumerate(cards2): # if the card was selected --> need to turn it around.
            if card_up2[i]: #this means card was selected.
            # need to turn the card face up.
                display_card(home_screen,i, card_images2,cards2)
        if len(selected_cards) == 2: # two cards have been selected --> compare them.
            card1 = card_images2[selected_cards[0]] # store image of first card selected in 'card1'.
            card2 = card_images2[selected_cards[1]] # store image of second card selected in 'card2'.
            if card1 == card2: # CARDS MATCH.
                matches = matches + 1 # add one match more.
            else: # CARDS DON'T MATCH.
                pygame.display.flip() # to update the screen.
                pygame.time.delay(300) # so the player can see the cards. Easy Level DELAY: 400.
                card_up2[selected_cards[0]] = False # flip the card back.
                card_up2[selected_cards[1]] = False # flip the card back.
            selected_cards = [] # reset the selected cards list.        
        if matches == 8: # when all cards have been 
            home_screen.fill(light_pink)
            message = "You won!!!"
            text = menu_font.render(message,True, black)
            # get_rect creates a rectangle from the surface containing this text:
            text_rect = text.get_rect(center=(home_screen_width//2, home_screen_height//2))
            home_screen.blit(text, text_rect) # this is to copy the contents from the 'text' surface into the menu_screen (screen) surface at the rectangle location('text_rect').
            settings_button.draw(home_screen, mouse_position)
 
    elif game_state == "Play_Hard":
        if x == 1:
            card_images3 = cards_game(4,5,10)
            cards3 = obtain_pos(4,5,card_images3)
            card_up3 = [False] * len(card_images3) # all cards are face down at first.
            x = 0
        display_game(home_screen, 4, 5, mouse_position)
        for i, card_rect in enumerate(cards3): # if the card was selected --> need to turn it around.
            if card_up3[i]: #this means card was selected.
            # need to turn the card face up.
                display_card(home_screen,i, card_images3,cards3)
        if len(selected_cards) == 2: # two cards have been selected --> compare them.
            card1 = card_images3[selected_cards[0]] # store image of first card selected in 'card1'.
            card2 = card_images3[selected_cards[1]] # store image of second card selected in 'card2'.
            if card1 == card2: # CARDS MATCH.
                matches = matches + 1 # add one match more.
            else: # CARDS DON'T MATCH.
                pygame.display.flip() # to update the screen.
                pygame.time.delay(200) # so the player can see the cards. Easy Level DELAY: 400.
                card_up3[selected_cards[0]] = False # flip the card back.
                card_up3[selected_cards[1]] = False # flip the card back.
            selected_cards = [] # reset the selected cards list.
        if matches == 10: # when all cards have been 
            home_screen.fill(light_pink)
            message = "You won!!!"
            text = menu_font.render(message,True, black)
            # get_rect creates a rectangle from the surface containing this text:
            text_rect = text.get_rect(center=(home_screen_width//2, home_screen_height//2))
            home_screen.blit(text, text_rect) # this is to copy the contents from the 'text' surface into the menu_screen (screen) surface at the rectangle location('text_rect').
            settings_button.draw(home_screen, mouse_position)

    elif game_state == "Settings":
        display_settings(home_screen, settings, selected_setting, menu_font, game_font)
    elif game_state == "Rules":
        display_rules(home_screen, mouse_position, font1, font3)
    
    elif game_state == "Restart Game":
        home_screen.fill(light_pink)
        matches = 0
        x = 1
        if game_level == "Easy":
            message = "Restarting Easy Level..."
            text = font1.render(message,True, black)
            text_rect = text.get_rect(center=(home_screen_width//2, home_screen_height//2))
            home_screen.blit(text, text_rect) 
            pygame.display.flip() 
            pygame.time.delay(1500)
            card_images1 = cards_game(3,4,6) # rows = 3; columns = 4; N = 6 (12 cards) -> Easy Level.
            cards1 = obtain_pos(3,4,card_images1)
            card_up1 = [False] * len(card_images1) # all cards are face down at first.
            x = 0 
            game_state = "Play_Easy"
        elif game_level == "Medium":
            message = "Restarting Medium Level..."
            text = font1.render(message,True, black)
            text_rect = text.get_rect(center=(home_screen_width//2, home_screen_height//2))
            home_screen.blit(text, text_rect) 
            pygame.display.flip() 
            pygame.time.delay(1500)
            card_images2 = cards_game(4,4,8)
            cards2 = obtain_pos(4,4,card_images2)
            card_up2 = [False] * len(card_images2) # all cards are face down at first.
            x = 0 
            game_state = "Play_Medium"
        elif game_level == "Hard":
            message = "Restarting Hard Level..."
            text = font1.render(message,True, black)
            text_rect = text.get_rect(center=(home_screen_width//2, home_screen_height//2))
            home_screen.blit(text, text_rect) 
            pygame.display.flip() 
            pygame.time.delay(1500)
            card_images3 = cards_game(4,5,10)
            cards3 = obtain_pos(4,5,card_images3)
            card_up3 = [False] * len(card_images3) # all cards are face down at first.
            x = 0
            game_state = "Play_Hard"
        elif game_level == "None":
            game_state = "Play"

    if x == 1: # restart the game with new cards
        matches = 0 

    pygame.display.flip()
pygame.quit()
