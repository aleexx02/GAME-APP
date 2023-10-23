import pygame
pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
screen = pygame.display.set_mode([SCREEN_HEIGHT, SCREEN_WIDTH])
pygame.display.set_caption("Crossword Puzzle!")

#button class
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
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

