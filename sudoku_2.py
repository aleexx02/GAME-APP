'''
GABRIELLE MUNSON

SUDOKU GAME

OCTOBER 2023
'''

import pygame
import requests


class SudokuGame:
    def __init__(self):
        self.window_size = (800, 600)
        self.background_color = (148, 133, 123)
        self.original_number = (0, 0, 0)
        self.buffer = 5
        self.mistakes = 0
        self.highlight = pygame.Color(255, 254, 113, 150)
        self.transparent_yellow = pygame.Color(255, 254, 113, 50)
        self.clock = pygame.time.Clock()
        self.window = None
        self.diff = None
        self.difficulty = None

    def diff_menu(self):
        begin = pygame.image.load("C:\\Users\\munso\\CIS\\Brain Game Files"
                                  "\\Difficulty_screen.png").convert()
        self.window.blit(begin, (0, 0))
        pygame.display.update()
        myfont = pygame.font.SysFont('Calibri', 35)

        while True:
            pygame.init()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if 299 < pos[0] < 501:
                        if 199 < pos[1] < 261:  # easy
                            self.diff = "Easy"
                            self.window.fill(self.background_color)
                            text = myfont.render(
                                'Please be patient while the game loads...',
                                True, (0, 0, 0))
                            textRect = text.get_rect()
                            textRect.center = (800 // 2, 600 // 2)
                            self.window.blit(text, textRect)
                            pygame.display.flip()
                            self.window.fill(self.background_color)
                            self.sudoku_game()
                        if 288 < pos[1] < 344:  # medium
                            self.diff = "Medium"
                            self.window.fill(self.background_color)
                            text = myfont.render(
                                'Please be patient while the game loads...',
                                True, (0, 0, 0))
                            textRect = text.get_rect()
                            textRect.center = (800 // 2, 600 // 2)
                            self.window.blit(text, textRect)
                            pygame.display.flip()
                            self.window.fill(self.background_color)
                            self.sudoku_game()
                        if 375 < pos[1] < 434:  # hard
                            self.diff = "Hard"
                            self.window.fill(self.background_color)
                            text = myfont.render(
                                'Please be patient while the game loads...',
                                True, (0, 0, 0))
                            textRect = text.get_rect()
                            textRect.center = (800 // 2, 600 // 2)
                            self.window.blit(text, textRect)
                            pygame.display.flip()
                            self.window.fill(self.background_color)
                            self.sudoku_game()
                    return False

    def sudoku_game(self):
        pygame.init()
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        while self.diff != self.difficulty:
            response = requests.get("https://sudoku-api.vercel.app/api/"
                                    "dosuku?query={newboard(limit:1){grids"
                                    "{value,solution,difficulty}}}")
            mess = response.json()
            grid = mess['newboard']['grids'][0]['value']
            solution = mess['newboard']['grids'][0]['solution']
            self.difficulty = mess['newboard']['grids'][0]['difficulty']
            original_grid = [[grid[x][y] for y in range(len(grid[0]))]
                             for x in range(len(grid))]
        print(solution)
        myfont = pygame.font.SysFont('Calibri', 35)
        diff_font = pygame.font.SysFont('Calibri', 20)
        mistakes = 0
        # draw the lines of the board
        for i in range(0, 10):
            if (i % 3 == 0):
                pygame.draw.line(
                    self.window,
                    (0, 0, 0), (200 + 50*i, 50), (200 + 50*i, 500), 5)
                pygame.draw.line(
                    self.window,
                    (0, 0, 0), (200, 50 + 50*i), (650, 50 + 50*i), 5)
            pygame.draw.line(
                self.window, (0, 0, 0), (200 + 50*i, 50), (200 + 50*i, 500), 2)
            pygame.draw.line(
                self.window, (0, 0, 0), (200, 50 + 50*i), (650, 50 + 50*i), 2)
        # display difficulty level
        diff_text = diff_font.render('Difficulty: '+ self.difficulty, True, self.original_number)
        self.window.blit(diff_text, (27, 50))
        pygame.display.flip()

        # insert the numbers onto the board
        for i in range(0, len(grid[0])):
            for j in range(0, len(grid[0])):
                if(0 < grid[i][j] < 10):
                    value = myfont.render(
                        str(grid[i][j]), True, self.original_number)
                    self.window.blit(
                        value, ((j + 4)*50 + 17, (i + 1)*50 + 13))
        pygame.display.flip()

        x = 215
        bottom_nums = pygame.font.SysFont('Calibri', 35, True)

        for n in numbers:
            num = bottom_nums.render(str(n), True, self.original_number)
            self.window.blit(num, (x, 530))
            x += 50

        playing = True

        while playing:
            pygame.draw.rect(
                self.window, self.background_color, (50, 100, 100, 100))
            ticks = pygame.time.get_ticks()
            seconds = int(ticks / 1000 % 60)
            minutes = int(ticks / 60000 % 24)
            out = '{minutes:02d}:{seconds:02d}'.format(
                minutes=minutes, seconds=seconds)
            timer = myfont.render(out, True, pygame.Color((0, 0, 0)))
            self.window.blit(timer, (60, 110))
            pygame.display.flip()
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    pygame.display.update
                    self.edit(self.window, (pos[0]//50, pos[1]//50),
                              mistakes, grid, original_grid, solution)
                    if self.solved(grid):
                        completion_time = out
                        self.complete_game(self.window, completion_time)
                        playing = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

    def solved(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return False
        return True

    def used_nums(self, grid, input):
        total = 0
        bottom_nums = pygame.font.SysFont('Calibri', 35, True)
        num_location = {1: (215, 530), 2: (265, 530), 3: (315, 530),
                        4: (365, 530), 5: (415, 530), 6: (465, 530),
                        7: (515, 530), 8: (565, 530), 9: (615, 530)}
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] == input:
                    total += 1
                j += 1
            i += 1
        if total == 9:
            # cover number displayed on gui with a light gray number
            dim_num = bottom_nums.render(str(input), True, (129, 133, 137))
            self.window.blit(dim_num, num_location[input])
            return
        else:
            return

    def edit(self, position):
        i, j = position[1], position[0]
        myfont = pygame.font.SysFont('Calibri', 35)

        while True:
            pygame.draw.rect(self.window, self.background_color,
                             (50, 100, 100, 100))
            ticks = pygame.time.get_ticks()
            seconds = int(ticks / 1000 % 60)
            minutes = int(ticks / 60000 % 24)
            out = '{minutes:02d}:{seconds:02d}'.format(minutes=minutes,
                                                       seconds=seconds)
            timer = myfont.render(out, True, pygame.Color((0, 0, 0)))
            self.window.blit(timer, (60, 110))
            pygame.display.flip()
            self.clock.tick(60)
            try:
                if self.grid[i-1][j-4] == 0:
                    # highlight selected box
                    pygame.draw.rect(
                        self.window, self.highlight,
                        (position[0]*50 + 3, position[1]*50 + 3,
                         45.75, 46.25))
                    pygame.display.update()
                pygame.init()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if self.grid[i-1][j-4] == 0:
                            pygame.draw.rect(
                                self.window, self.background_color,
                                (position[0]*50 + 3, position[1]*50 + 3,
                                 45.75, 46.25))
                        pos = pygame.mouse.get_pos()
                        pygame.display.update
                        self.edit(self.window, (pos[0]//50, pos[1]//50),
                                  mistakes, self.grid, self.original_grid,
                                  self.solution)
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        if self.grid[i-1][j-4] == 0:
                            pygame.draw.rect(
                                self.window, self.background_color,
                                (position[0]*50 + 3, position[1]*50 + 3,
                                 45.75, 46.25))
                            pygame.display.update()
                        # ensure the user is selecting a valid box
                        if(self.original_grid[i-1][j-4] != 0):
                            return
                        # delete the character in the selected box
                        if(event.key == 8):
                            self.grid[i-1][j-4] = 0
                            pygame.draw.rect(
                                self.window, self.background_color,
                                (position[0]*50 + self.buffer, position[1]*50 +
                                 self.buffer, 50 - 2*self.buffer, 50 -
                                 2*self.buffer))
                            pygame.display.update()
                            return
                        # insert a digit
                        # check for valid input 1-9
                        if (0 < event.key - 48 < 10):
                            # compare input with solution
                            if event.key - 48 == self.solution[i-1][j-4]:
                                pygame.draw.rect(
                                    self.window, self.background_color,
                                    (position[0]*50 + self.buffer,
                                     position[1]*50 + self.buffer, 50 -
                                     2*self.buffer, 50 - 2*self.buffer))
                                value = myfont.render(str(event.key - 48),
                                                      True, (46, 60, 54))
                                self.window.blit(value, (position[0]*50 + 16,
                                                         position[1]*50 + 13))
                                self.grid[i-1][j-4] = event.key - 48
                                self.used_nums(
                                    self.grid, event.key-48, self.window)
                                pygame.display.update()
                                return
                            # red box will appear over box
                            # selected if invalid input
                            else:
                                pygame.draw.rect(
                                    self.window, (255, 51, 51),
                                    (position[0]*50 + 6, position[1]*50 + 6,
                                     50 - 2*self.buffer, 50 - 2*self.buffer))
                                pygame.display.update()
                                pygame.time.delay(800)
                                pygame.draw.rect(
                                    self.window, self.background_color,
                                    (position[0]*50 + 6, position[1]*50 + 6,
                                     50 - 2*self.buffer, 50 - 2*self.buffer))
                                pygame.display.update()
                                mistakes += 1
                                return
            except:
                pass

    def complete_game(self, time):
        myfont = pygame.font.SysFont('Calibri', 35)
        pygame.time.delay(500)
        win = pygame.image.load(
            "C:\\Users\\munso\\Downloads\\completion_screen.png").convert()
        end_time = myfont.render(time, False, (0, 0, 0))
        self.window.blit(win, (0, 0))
        self.window.blit(end_time, (210, 210))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if 305 < pos[0] < 492:
                        if 297 < pos[1] < 358:  # play again button
                            self.window.fill(self.background_color)
                            self.sudoku_game(self.window)
                            pygame.display.update()
                            return
                        if 380 < pos[1] < 441:  # browse games button
                            pass
                        if 464 < pos[1] < 526:  # quit button
                            pygame.quit()
                            return
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

    def run(self):
        pygame.init()
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("SUDOKU")
        begin = pygame.image.load(
            "C:\\Users\\munso\\Downloads\\main_screen.png").convert()
        self.window.blit(begin, (0, 0))
        pygame.display.update()
        myfont = pygame.font.SysFont('Calibri', 35)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    # play sudoku
                    if 305 < pos[0] < 492 and 297 < pos[1] < 358:
                        self.window.fill(self.background_color)
                        self.diff_menu()
                        pygame.init()
                        pygame.display.flip()
                        return
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
'''
if __name__ == "__main__":
    sudoku = SudokuGame()
    sudoku.run()
'''
