'''
GABRIELLE MUNSON

SUDOKU GAME 2.0
ACTUALLY UPDATED ONE

CIS 350
OCTOBER 2023
'''

import pygame
import requests


class SudokuGame:
    def __init__(self):
        pygame.init()
        # define attributes
        self.window_size = (800, 600)
        self.bgc = (148, 133, 123)
        self.black = (0, 0, 0)
        self.buffer = 5
        self.mistakes = 0
        self.highlight = pygame.Color(255, 254, 113, 150)
        self.transparent_yellow = pygame.Color(255, 254, 113, 50)
        self.clock = pygame.time.Clock()
        self.diff = ''
        self.myfont = pygame.font.SysFont('Calibri', 35, False, False)
        self.diff_font = pygame.font.SysFont('Calibri', 20)

    def initialize_game(self):
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("SUDOKU")
        self.load_initial_screen()
        pygame.display.update()
        print('Initial screen loaded')

    def load_initial_screen(self):
        begin = pygame.image.load(
            "C:\\Users\\munso\\Downloads\\main_screen.png")
        self.window.blit(begin, (0, 0))

    def start_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if 305 < pos[0] < 492 and 297 < pos[1] < 358:
                        # Play Sudoku
                        self.window.fill(self.bgc)
                        self.difficulty_menu()
                        pygame.init()
                        pygame.display.flip()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

    def difficulty_menu(self):
        difficulty_selection = pygame.image.load(
            "C:\\Users\\munso\\CIS\\Brain Game Files\\Difficulty_screen.png")
        self.window.blit(difficulty_selection, (0, 0))
        pygame.display.update()
        myfont = pygame.font.SysFont('Calibri', 35)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if 299 < pos[0] < 501:
                        if 199 < pos[1] < 261:  # easy
                            self.diff = "Easy"
                            self.load_level()
                            return
                        if 288 < pos[1] < 344:  # medium
                            self.diff = "Medium"
                            self.load_level()
                            return
                        if 375 < pos[1] < 434:  # hard
                            self.diff = "Hard"
                            self.load_level()
                            return

    def load_level(self):
        self.window.fill(self.bgc)
        text = self.myfont.render('Please be patient while the game loads...',
                                  True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (800 // 2, 600 // 2)
        self.window.blit(text, textRect)
        pygame.display.flip()
        print('Level loading')
        self.window.fill(self.bgc)
        self.sudoku_game()

    def sudoku_game(self):
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        difficulty = None
        while self.diff != difficulty:
            try:
                response = requests.get(
                    "https://sudoku-api.vercel.app/api/dosuku?query={newboard"
                    "(limit:1){grids{value, solution, difficulty}}}")
                mess = response.json()
                grid = mess['newboard']['grids'][0]['value']
                self.solution = mess['newboard']['grids'][0]['solution']
                difficulty = mess['newboard']['grids'][0]['difficulty']
                original_grid = [[grid[x][y] for y in range(len(grid[0]))]
                                 for x in range(len(grid))]
            except:
                difficulty = None

        # draw the lines of the board
        print(self.solution)
        for i in range(0, 10):
            if (i % 3 == 0):
                pygame.draw.line(self.window, (0, 0, 0),
                                 (200 + 50*i, 50), (200 + 50*i, 500), 5)
                pygame.draw.line(self.window, (0, 0, 0),
                                 (200, 50 + 50*i), (650, 50 + 50*i), 5)
            pygame.draw.line(self.window, (0, 0, 0),
                             (200 + 50*i, 50), (200 + 50*i, 500), 2)
            pygame.draw.line(self.window, (0, 0, 0),
                             (200, 50 + 50*i), (650, 50 + 50*i), 2)
        # display difficulty level
        diff_text = self.diff_font.render(
            'Difficulty: ' + self.diff, True, self.black)
        self.window.blit(diff_text, (27, 50))
        pygame.display.flip()

        # insert the numbers onto the board
        for i in range(0, len(grid[0])):
            for j in range(0, len(grid[0])):
                if (0 < grid[i][j] < 10):
                    value = self.myfont.render(
                        str(grid[i][j]), True, self.black)
                    self.window.blit(
                        value, ((j+4) * 50 + 17, (i+1) * 50 + 13))
        pygame.display.flip()

        x = 215
        bottom_nums = pygame.font.SysFont('Calibri', 35, True)

        for n in numbers:
            num = bottom_nums.render(str(n), True, self.black)
            self.window.blit(num, (x, 530))
            x += 50

        playing = True

        while playing:
            pygame.draw.rect(self.window, self.bgc, (50, 100, 100, 100))
            ticks = pygame.time.get_ticks()
            seconds = int(ticks / 1000 % 60)
            minutes = int(ticks / 60000 % 24)
            out = '{minutes:02d}:{seconds:02d}'.format(
                minutes=minutes, seconds=seconds)
            timer = self.myfont.render(out, True, pygame.Color((0, 0, 0)))
            self.window.blit(timer, (60, 110))
            pygame.display.flip()
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    pygame.display.update
                    self.edit((pos[0]//50, pos[1]//50), self.mistakes, grid,
                              original_grid, self.solution)
                    if self.solved(grid):
                        completion_time = out
                        self.complete_game(completion_time)
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

    def complete_game(self, time):
        pygame.time.delay(500)
        win = pygame.image.load(
            "C:\\Users\\munso\\Downloads\\completion_screen.png"
        ).convert()
        end_time = self.myfont.render(time, False, (0, 0, 0))
        self.window.blit(win, (0, 0))
        self.window.blit(end_time, (210, 210))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if 305 < pos[0] < 492:
                        if 297 < pos[1] < 358:  # play again button
                            self.window.fill(self.bgc)
                            self.sudoku_game()
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

    def edit(self, position, mistakes, grid, original_grid, solution):
        i, j = position[1], position[0]

        while True:
            pygame.draw.rect(self.window, self.bgc, (50, 100, 100, 100))
            ticks = pygame.time.get_ticks()
            seconds = int(ticks / 1000 % 60)
            minutes = int(ticks / 60000 % 24)
            out = '{minutes:02d}:{seconds:02d}'.format(
                minutes=minutes, seconds=seconds)
            timer = self.myfont.render(out, True, pygame.Color((0, 0, 0)))
            self.window.blit(timer, (60, 110))
            pygame.display.flip()
            self.clock.tick(60)
            if grid[i-1][j-4] == 0:
                # highlight selected box
                pygame.draw.rect(self.window, self.highlight, (
                    position[0] * 50 + 3, position[1] * 50 + 3, 45.75, 46.25))
                pygame.display.update()
            pygame.init()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if grid[i-1][j-4] == 0:
                        pygame.draw.rect(self.window, self.bgc, (
                            position[0] * 50 + 3, position[1] * 50 + 3,
                            45.75, 46.25))
                    pos = pygame.mouse.get_pos()
                    pygame.display.update
                    self.edit((pos[0]//50, pos[1]//50), mistakes, grid,
                              original_grid, solution)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if grid[i-1][j-4] == 0:
                        pygame.draw.rect(self.window, self.bgc, (
                            position[0] * 50 + 3, position[1] * 50 + 3,
                            45.75, 46.25))
                        pygame.display.update()
                    # ensure the user is selecting a valid box
                    if (original_grid[i-1][j-4] != 0):
                        pass
                    # delete the character in the selected box
                    if (event.key == 8):
                        grid[i-1][j-4] = 0
                        pygame.draw.rect(self.window, self.bgc, (
                            position[0] * 50 + self.buffer, position[1] * 50 +
                            self.buffer, 50 - 2 * self.buffer,
                            50 - 2 * self.buffer))
                        pygame.display.update()
                        pass
                    # insert a digit
                    if (0 < event.key - 48 < 10):  # check for valid input 1-9
                        # compare input with solution
                        if event.key - 48 == solution[i-1][j-4]:
                            pygame.draw.rect(self.window, self.bgc, (
                                position[0] * 50 + self.buffer, position[1] *
                                50 + self.buffer, 50 - 2 * self.buffer, 50 -
                                2 * self.buffer))
                            value = self.myfont.render(str(event.key - 48),
                                                       True, (46, 60, 54))
                            self.window.blit(value, (position[0] * 50+16,
                                                     position[1] * 50+13))
                            grid[i-1][j-4] = event.key - 48
                            self.used_nums(grid, event.key-48)
                            pygame.display.update()
                            pass
                        # red box will appear over box if incorrect
                        else:
                            pygame.draw.rect(self.window, (255, 51, 51), (
                                position[0] * 50 + 6, position[1] * 50 + 6,
                                50 - 2 * self.buffer, 50 - 2 * self.buffer))
                            pygame.display.update()
                            pygame.time.delay(800)
                            pygame.draw.rect(self.window, self.bgc, (
                                position[0] * 50 + 6, position[1] * 50 + 6,
                                50 - 2 * self.buffer, 50 - 2 * self.buffer))
                            pygame.display.update()
                            mistakes += 1
                            pass

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
            dim_num = bottom_nums.render(str(input), True, (150, 150, 150))
            self.window.blit(dim_num, num_location[input])
            return
        else:
            return


# Usage example
def main():
    sudoku_game = SudokuGame()
    sudoku_game.initialize_game()
    sudoku_game.start_game()
