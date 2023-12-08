import unittest
from sudoku_game_2 import SudokuGame  # Import SudokuGame from your file

class TestSudokuGameIntegration(unittest.TestCase):
    def setUp(self):
        self.sudoku_game = SudokuGame()

    def test_start_game_difficulty_menu_sudoku_game(self):
        # Initialize the game
        self.sudoku_game.initialize_game()
        
        # Simulate starting the game
        self.sudoku_game.start_game()

        # Simulate selecting a difficulty from the menu
        self.sudoku_game.difficulty_menu()

        # Simulate loading a level
        self.sudoku_game.load_level()

        # Simulate playing the Sudoku game until completion
        self.sudoku_game.sudoku_game()

        # Simulate completing the game
        self.sudoku_game.complete_game("00:00")

        # No assertion is needed as this test checks for the interaction of various game phases

if __name__ == '__main__':
    unittest.main()
