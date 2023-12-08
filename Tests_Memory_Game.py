import pygame
import pytest
import unittest
from unittest.mock import Mock, patch
from Memory_Card_Match_Brain_Game import Button_Image, display_menu, display_rules, display_game_levels, cards_game, display_game, obtain_pos, display_card, display_settings 

pygame.init()
pygame.font.init()
menu_font = pygame.font.SysFont("Elephant", 43) # define the font size of menu
game_font = pygame.font.SysFont("Californian FB", 35)
font1 = pygame.font.SysFont("Bahnschrift", 40)
font2 = pygame.font.SysFont("Bahnschrift", 35)
font3 = pygame.font.SysFont("Bahnschrift", 20)

class TestsGame(unittest.TestCase):
    def setUp(self):
        self.screen = pygame.Surface((600, 600)) # create a surface for testing the functions.
    # Button Test:
    def test_Button_Click_Inside(self):
        button = Button_Image(20,20,10,10,"settings_button.jpg")
        mouse_pos_in_button = (25,25) # this position lies within the button.
        result1 = button.click(mouse_pos_in_button)
        self.assertTrue(result1) # output should be True since we clicked the button.

    def test_Button_Click_Outside(self):
        button = Button_Image(20,20,10,10,"settings_button.jpg")
        mouse_pos_out_button = (50,50) # this position is outside the button.
        result2 = button.click(mouse_pos_out_button)
        self.assertFalse(result2) # output should be False since we didn't click the button.

    # display_menu function Test:
    def test_display_menu(self):
        menu_options = ["Play Game", "Settings", "Game Rules", "Quit"]
        selected_option = 1
        display_menu(self.screen, menu_options, selected_option, menu_font, game_font)
        expected_background_color = (255, 182, 193) # light pink background.
        expected_text_color = (0,0,0) # black color text.
        background_color = self.screen.get_at((self.screen.get_width()//2, 0)) # actual background color.
        # Position (336, 311) is the position of black text in the menu screen.
        text_color = self.screen.get_at((336,311)) # actual text color.
        self.assertEqual(background_color, expected_background_color)
        self.assertEqual(text_color, expected_text_color)
    
    def test_display_game_levels1(self):
        game_levels = ["Easy", "Medium", "Hard", "Game Menu", "Exit Game"]
        selected_level = 1  # Level = "Medium" --> color of text should be black.
        display_game_levels(self.screen, game_levels, selected_level, font1, game_font, font2)
        expected_text_color = (0, 0, 0)  # Black color.
        # Position (301, 235) is the position of black text in the game_level screen.
        actual_text_color = self.screen.get_at((301,235))
        self.assertEqual(actual_text_color, expected_text_color)
        
    def test_display_game_levels2(self):
        game_levels = ["Easy", "Medium", "Hard", "Game Menu", "Exit Game"]
        selected_level = 3  # Level = "Game Menu" --> color of text should be pink.
        display_game_levels(self.screen, game_levels, selected_level,font1, game_font, font2)
        expected_text_color = (255, 20, 150)  # Pink color.
        # Position (318, 388) is the position of pink text in the game_level screen.
        actual_text_color = self.screen.get_at((318,388))
        self.assertEqual(actual_text_color, expected_text_color)
        
    def test_cards_game(self):
        N = 9
        actual_result = cards_game(3, 3, N) # 3 rows, 3 columns and 9 cards.
        expected_result_length = N*2 # 18 cards in total.
        self.assertEqual(len(actual_result), expected_result_length)

    def test_display_game_EasyLevel(self):
        mouse_pos = pygame.mouse.get_pos()
        expected_settings_button = Button_Image(560,20,10,10,"settings_button.jpg")
        display_game(self.screen, 3, 4, mouse_pos)
        mouse_button = (565, 20)
        mouse_not_button = (580,20)
        # test if the settings button is in the right position:
        self.assertTrue(expected_settings_button.click(mouse_button))
        self.assertFalse(expected_settings_button.click(mouse_not_button))

    def test_obtain_pos_EasyLevel(self):
        N = 6
        card_images = cards_game(3, 4, N) # cards for Easy Level
        actual_rects = obtain_pos(3, 4, card_images) # actual list of rectangles.
        # Check the number of rectangles generated:
        self.assertEqual(len(actual_rects), N*2)
        # Check if the rectangles are at the expected positions:
        index = 0 # to keep track of which rectangle we are taking from the actual_rects list.
        # the for loops is to compare the actual_rect positions with the expected positions.
        for x in range(4):
            for y in range(3):
                actual_card_rect = actual_rects[index]
                index = index + 1
                # grid_width = 550 and grid_height = 600
                expected_position = (x * (550//4), y * (600//3))
                self.assertEqual(actual_card_rect.topleft,expected_position)
    
    
    def test_display_card(self):
        N = 6
        card_images = cards_game(3, 4, N) # cards for Easy Level
        card_rects = obtain_pos(3, 4, card_images) # actual list of rectangles.
        card_index = 0
        display_card(self.screen,card_index, card_images, card_rects)
        expected_card_rect = card_rects[card_index]
        actual_card_rect = card_images[card_index].get_rect()
        actual_card_rect.topleft = (0, 0)  # The top-left corner is the default position.
        self.assertEqual(actual_card_rect.topleft, expected_card_rect.topleft)
        

    def test_display_settings(self):
        settings = ["Restart Game", "Select Level", "Game Menu", "Exit Game"]
        selected_setting = 0
        display_settings(self.screen, settings, selected_setting, menu_font, game_font)
        expected_background_color = (255, 182, 193) # light pink background.
        expected_text_color = (0,0,0) # black color text.
        background_color = self.screen.get_at((self.screen.get_width()//2, 0)) # actual background color.
        # Position (335, 221) is the position of black text in the menu screen.
        text_color = self.screen.get_at((335,221)) # actual text color.
        self.assertEqual(background_color, expected_background_color)
        self.assertEqual(text_color, expected_text_color)
        



if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        pygame.quit()
