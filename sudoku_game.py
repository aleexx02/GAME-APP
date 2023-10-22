'''
GABRIELLE MUNSON

SUDOKU GAME

OCTOBER 2023
'''

import pygame
import requests

# determines variables
window_size = (800, 600)
background_color = (148,133,123)
original_number = (0,0,0)
buffer = 5
mistakes = 0

# prepare board and run sudoku
def sudoku_game(window):
    clock = pygame.time.Clock()
    response = requests.get("https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:1){grids{value,solution}}}")
    mess = response.json()
    grid = mess['newboard']['grids'][0]['value']
    solution = mess['newboard']['grids'][0]['solution']
    original_grid = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
    print(solution)
    myfont = pygame.font.SysFont('Calibri', 35)
    mistakes = 0
    # draw the lines of the board
    for i in range(0,10):
        if (i%3 == 0):
            pygame.draw.line(window, (0,0,0), (200 + 50*i, 50), (200 + 50*i,500), 5)
            pygame.draw.line(window, (0,0,0), (200, 50 + 50*i), (650, 50 + 50*i), 5)
        pygame.draw.line(window, (0,0,0), (200 + 50*i, 50), (200 + 50*i,500), 2)
        pygame.draw.line(window, (0,0,0), (200, 50 + 50*i), (650, 50 + 50*i), 2)
    pygame.display.flip()

    # insert the numbers onto the board
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if(0<grid[i][j]<10):
                value = myfont.render(str(grid[i][j]), True, original_number)
                window.blit(value, ((j+4)*50 + 17, (i+1)*50 + 13))
    pygame.display.flip()
    
    playing = True

    while playing:
        pygame.draw.rect(window, background_color, (50, 100, 100, 100))
        ticks = pygame.time.get_ticks()
        seconds = int(ticks / 1000 % 60)
        minutes = int(ticks / 60000 % 24)
        out = '{minutes:02d}:{seconds:02d}'.format(minutes=minutes, seconds=seconds)
        timer = myfont.render(out, True, pygame.Color((0,0,0)))
        window.blit(timer, (60, 110)) 
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                pygame.display.update
                edit(window, (pos[0]//50, pos[1]//50), mistakes, grid, original_grid)
                if solved(grid):
                    completion_time = out
                    complete_game(window, completion_time)
                    playing = False
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                

# check if the number is present in the 3x3 box selected
def is_valid_box(row, col, num, grid):
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False
    return True

# check if the grid created by the user is full/solved
def solved(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return False
    return True

# insert or delete a digit specified by the user
def edit(window, position, mistakes, grid, original_grid):
    i,j = position[1], position[0]
    myfont = pygame.font.SysFont('Calibri', 35)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                pygame.display.update
                edit(window, (pos[0]//50, pos[1]//50), mistakes, grid, original_grid)
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                # ensure the user is selecting a valid box
                if(original_grid[i-1][j-4] != 0):
                    return
                # delete the character in the selected box
                if(event.key == 8): 
                    grid[i-1][j-4] = 0
                    pygame.draw.rect(window, background_color, (position[0]*50 + buffer, position[1]*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
                    pygame.display.update()
                    return
                # insert a digit
                if (0 < event.key - 48 < 10): # check for valid input 1-9
                    if event.key - 48 not in grid[i-1]: # check rows
                        x = 0
                        c_check = []
                        while x < 9:
                            c_check.append(grid[x][j-4])
                            x += 1
                        if event.key - 48 not in c_check: # check columns
                            if is_valid_box(i-1, j-4, event.key - 48, grid): # check 3x3 box
                                pygame.draw.rect(window, background_color, (position[0]*50 + buffer, position[1]*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
                                value = myfont.render(str(event.key - 48), True, (46,60,54))
                                window.blit(value, (position[0]*50+16, position[1]*50+13))
                                grid[i-1][j-4] = event.key - 48
                                pygame.display.update()
                                return
                            # red box will appear over box selected if invalid input
                            else:
                                pygame.draw.rect(window, (255,51,51), (position[0]*50 + 6, position[1]*50 + 6, 50 - 2*buffer, 50 - 2*buffer))
                                pygame.display.update()
                                pygame.time.delay(800)
                                pygame.draw.rect(window, background_color, (position[0]*50 + 6, position[1]*50 + 6, 50 - 2*buffer, 50 - 2*buffer))
                                pygame.display.update()
                                mistakes += 1
                                return
                        else:
                            pygame.draw.rect(window, (255,51,51), (position[0]*50 + 6, position[1]*50 + 6, 50 - 2*buffer, 50 - 2*buffer))
                            pygame.display.update()
                            pygame.time.delay(800)
                            pygame.draw.rect(window, background_color, (position[0]*50 + 6, position[1]*50 + 6, 50 - 2*buffer, 50 - 2*buffer))
                            pygame.display.update()
                            mistakes += 1
                            return
                    else:
                        pygame.draw.rect(window, (255,51,51), (position[0]*50 + 6, position[1]*50 + 6, 50 - 2*buffer, 50 - 2*buffer))
                        pygame.display.update()
                        pygame.time.delay(800)
                        pygame.draw.rect(window, background_color, (position[0]*50 + 6, position[1]*50 + 6, 50 - 2*buffer, 50 - 2*buffer))
                        pygame.display.update()
                        mistakes += 1
                        return
                    
# show completion screen with options
def complete_game(window, time):
    myfont = pygame.font.SysFont('Calibri', 35)
    pygame.time.delay(500)
    win = pygame.image.load("C:\\Users\\munso\\Downloads\\completion_screen.png").convert()
    end_time = myfont.render(time, False, (0, 0, 0))
    window.blit(win, (0, 0))
    window.blit(end_time, (210,210))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 305 < pos[0] < 492:
                    if 297 < pos[1] < 358: # play again button
                        window.fill(background_color)
                        sudoku_game(window)
                        pygame.display.update()
                        return
                        # pygame.draw.rect(window, background_color, pygame.Rect(0, 0, 800, 600))
                    if 380 < pos[1] < 441: # browse games button
                        pass
                    if 464 < pos[1] < 526: # quit button
                        pygame.quit()
                        return
            if event.type == pygame.QUIT:
                pygame.quit()
                return

# initialze and run window       
def main():
    pygame.init()
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("SUDOKU")
    begin = pygame.image.load("C:\\Users\\munso\\Downloads\\main_screen.png").convert()
    window.blit(begin, (0, 0))
    pygame.display.update()
    myfont = pygame.font.SysFont('Calibri', 35)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if 305 < pos[0] < 492 and 297 < pos[1] < 358: # play sudoku
                    window.fill(background_color)
                    sudoku_game(window)
                    pygame.display.flip()
                    return
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
main()