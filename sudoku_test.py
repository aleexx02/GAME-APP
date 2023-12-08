import unittest
import pygame
from unittest.mock import patch, MagicMock
from sudoku_game_2 import SudokuGame

class TestSudokuGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.sudoku_game = SudokuGame()

    def tearDown(self):
        pygame.quit()

    def test_init_game(self):
        pygame.display.set_mode((800,600))
        self.sudoku_game.initialize_game()
        with patch('builtins.print') as mocked_print:
            self.sudoku_game.initialize_game()
            mocked_print.assert_called_with('Initial screen loaded')

    def test_solved(self):
        grid =[[3, 6, 7, 2, 1, 8, 9, 5, 4],
                 [4, 5, 1, 7, 9, 3, 8, 6, 2],
                 [2, 8, 9, 6, 5, 4, 7, 3, 1],
                 [1, 9, 6, 8, 4, 5, 2, 7, 3],
                 [5, 4, 2, 3, 7, 1, 6, 8, 9],
                 [7, 3, 8, 9, 6, 2, 1, 4, 5], 
                 [8, 1, 4, 5, 2, 7, 3, 9, 6],
                 [6, 2, 3, 4, 8, 9, 5, 1, 7],
                 [9, 7, 5, 1, 3, 6, 4, 2, 8]]
        output = SudokuGame.solved(SudokuGame, grid)  
        self.assertEqual(output, True)

    def test_med_diff(self):
        # Test difficulty_menu method for different difficulty levels
        pygame.display.set_mode((800,600))
        self.sudoku_game.initialize_game()
        with patch('builtins.input'):
            self.sudoku_game.difficulty_menu()
            self.assertEqual(self.sudoku_game.diff, "Medium")

    def test_load_level(self):
        pygame.display.set_mode((800,600))
        self.sudoku_game.initialize_game()
        with patch('builtins.print') as mocked_print:
            self.sudoku_game.difficulty_menu()
            mocked_print.assert_called_with('Level loading')

    def test_sudoku_game(self):
        pygame.display.set_mode((800,600))
        self.sudoku_game.initialize_game()
        with patch('builtins.print') as mocked_print:
            self.sudoku_game.difficulty_menu()
            mocked_print.assert_called_with('Board edited')

    def test_mouse_button_click(self):
        # Set up initial conditions for the test
        position = (250, 100)  # Sample position
        mistakes = 0
        grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]]  # Sample grid
        original_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0]]  # Sample original grid
        solution = [[3, 4, 2, 9, 6, 7, 1, 8, 5],
                    [6, 5, 1, 2, 4, 8, 3, 9, 7],
                    [9, 8, 7, 1, 5, 3, 4, 2, 6],
                    [5, 7, 6, 3, 2, 9, 8, 4, 1],
                    [8, 3, 9, 6, 1, 4, 7, 5, 2],
                    [1, 2, 4, 7, 8, 5, 6, 3, 9],
                    [7, 6, 3, 4, 9, 2, 5, 1, 8],
                    [2, 1, 5, 8, 3, 6, 9, 7, 4],
                    [4, 9, 8, 5, 7, 1, 2, 6, 3]]  # Sample solution

        # Simulate a mouse button click event
        new_grid, new_mistakes = self.sudoku_game.edit(position, mistakes, grid, original_grid, solution, "MOUSE_BUTTON_CLICK")

        expected_grid = [[3, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0]]  # Sample original grid
        # Perform assertions based on the expected behavior
        # Add assertions to verify the changes in the grid and mistakes
        self.assertEqual(new_grid, expected_grid)

    def test_unused_nums(self):
        # Simulate a grid where the input number is not present 9 times
        test_grid = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 8]  # The input number is present 8 times
        ]
        input_number = 8  # Example input number

        # Call the used_nums method with the test grid and input number
        result = self.sudoku_game.used_nums(test_grid, input_number)

        # Assert that the result should be False when the input number is not present 9 times
        self.assertFalse(result)

    def test_used_nums(self):
        # Simulate a grid where the input number is not present 9 times
        test_grid = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 8]  # The input number is present 8 times
        ]
        input_number = 5  # Example input number

        # Call the used_nums method with the test grid and input number
        result = self.sudoku_game.used_nums(test_grid, input_number)

        # Assert that the result should be False when the input number is not present 9 times
        self.assertTrue(result)
    
    def test_start_game(self):
        pygame.display.set_mode((800,600))
        self.sudoku_game.initialize_game()
        output = self.sudoku_game.start_game()
        self.assertTrue(output)


    """def test_key_down(self):
        # Set up initial conditions for the test
        position = (1, 0)  # Sample position
        mistakes = 0
        grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Sample grid
        original_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Sample original grid
        solution = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # Sample solution

        # Simulate a key down event (for example, the user presses the '1' key)
        new_grid, new_mistakes = self.sudoku_game.edit(position, mistakes, grid, original_grid, solution, "KEY_DOWN", event_key=49)

        # Perform assertions based on the expected behavior
        # Add assertions to verify the changes in the grid and mistakes
        self.assertEqual(new_grid, expected_grid)"""


    """def test_complete(self):
        pygame.display.set_mode((800, 600))
        self.sudoku_game.initialize_game()
        with patch('builtins.print') as mocked_print:
            self.sudoku_game.complete_game()
            mocked_print.assert_called_with('Played again')"""

    '''def test_start_game(self):
        pygame.display.set_mode((800,600))
        self.sudoku_game.initialize_game()
        with patch('builtins.print') as mocked_print:
            self.sudoku_game.start_game()
            mocked_print.assert_called_with('Game started')'''

    '''def test_complete_game(self):
        pygame.display.set_mode((800, 600))
        self.sudoku_game.initialize_game()'''

    
    '''def test_edit_function(self):
        sudoku = SudokuGame()
        sudoku_grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]]
        
        expected_grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 1, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]]
        # Simulate user input for editing a cell (e.g., entering '1' at position (100, 250))
        with patch('builtins.input', side_effect=["1"]):
            sudoku.edit((100, 250), 0, sudoku_grid, sudoku_grid, expected_grid)

        self.assertEqual(sudoku.grid, expected_grid)
        '''

if __name__ == '__main__':
    unittest.main()
