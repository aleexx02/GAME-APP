import pygame
import sudoku_game as s
import minesweeper as ms
import memory_match as mm
import GUI as cw

window_size = (800, 600)
background_color = (148, 133, 123)


def main_window():
    pygame.init()
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("BRAIN GAMES")
    begin = pygame.image.load("C:\\Users\\munso\\Downloads\\main.png")
    window.blit(begin, (0, 0))
    pygame.display.update()
    myfont = pygame.font.SysFont('Calibri', 35)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if 299 < pos[0] < 501:
                    if 199 < pos[1] < 261:  # play minesweeper
                        window.fill(background_color)
                        ms.run_minesweeper()
                        pygame.display.flip()
                        return
                    if 288 < pos[1] < 344:  # play memory match
                        window.fill(background_color)
                        mm.run_memory_match()
                        pygame.display.flip()
                        return
                    if 375 < pos[1] < 434:
                        window.fill(background_color)
                        s.sudoku_game(window)
                        pygame.display.flip()
                        return
                    if 466 < pos[1] < 522:
                        window.fill(background_color)
                        s.sudoku_game(window)
                        pygame.display.flip()
                        return
            if event.type == pygame.QUIT:
                pygame.quit()
                return
