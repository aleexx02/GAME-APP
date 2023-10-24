"""
Natalie Rodriguez
CIS 350
Main Menu

"""

import pygame
import sys
import os
import random
import mine
import Memory_Card

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 65
NUM_MINES = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (248, 200, 220)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Menu")

font = pygame.font.Font(None, 36)

game_state = "MAIN_MENU"

# Function to display the menu
def display_menu(screen, screen_width, screen_height):
   # Load the background image
   background_image = pygame.image.load("bg.jpg")
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
            ("Play Minesweeper", mine.minesweeper_menu),
            ("Play Memory Match", Memory_Card.start_memory_game),
            # Add other games here
            # ("Play Game 3", game3_function),
            # ("Play Game 4", game4_function),
            # ("Play Game 5", game5_function)
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