import pygame
import sudoku_game as s
import GUI as cw
import minesweeper as m
import memory_match as mc


window_size = (800, 600)
background_color = (148,133,123)
game_state = "MAIN_MENU"
pygame.init()
pygame.font.init()

def main():
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("BRAIN GAMES")
    begin = pygame.image.load("C:\\Users\\munso\\CIS\\main_screen_file.png").convert()
    window.blit(begin, (0, 0))
    pygame.display.update()
    myfont = pygame.font.SysFont('Calibri', 35)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if 299 < pos[0] < 501:
                    if 199 < pos[1] < 261: # play minesweeper
                        window.fill(background_color)
                        m.minesweeper_menu()
                        pygame.display.flip()
                        return
                    if 288 < pos[1] < 344: # play memory match
                        window.fill(background_color)
                        mc.start_memory_game()
                        pygame.display.flip()
                        return
                    if 375 < pos[1] < 434:
                        window.fill(background_color)
                        s.sudoku_game(window)
                        pygame.display.flip()
                        return
                    if 466 < pos[1] < 522:
                        window.fill(background_color)
                        cw.run_crossword(window)
                        pygame.display.flip()
                        return
            if event.type == pygame.QUIT:
                pygame.quit()
                return
    
        
main()