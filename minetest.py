import unittest
import minesweeper


class TestMineGeneration(unittest.TestCase):
    def setUp(self):
        minesweeper.mines = set()

    def initialize_grid(self, size):
        minesweeper.grid = [[0 for _ in range(size)] for _ in range(size)]
        minesweeper.revealed = [[False for _ in range(size)] for _ in range(size)]

    def test_mine_count_easy(self):
        self.initialize_grid(9)  # 9x9 grid for Easy
        minesweeper.selected_level = 'Easy'
        minesweeper.generate_mines()
        self.assertEqual(sum(row.count(-1) for row in minesweeper.grid), 10)

    def test_mine_count_medium(self):
        self.initialize_grid(16)  # 16x16 grid for Medium
        minesweeper.SELECTED_LEVEL = 'Medium'
        minesweeper.generate_mines()
        self.assertEqual(sum(row.count(-1) for row in minesweeper.grid), 40)

    def test_mine_count_hard(self):
        self.initialize_grid(30)
        minesweeper.SELECTED_LEVEL= 'Hard'
        minesweeper.generate_mines()
        self.assertEqual(sum(row.count(-1) for row in minesweeper.grid), 99)


class TestWinCondition(unittest.TestCase):
    def setUp(self):
        pass

    def test_win_condition(self):
        minesweeper.grid = [
            [-1, 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]
        minesweeper.revealed = [
            [False, True, True],
            [True, True, True],
            [True, True, True]
        ]
        minesweeper.mines = {(0, 0)} 

        self.assertTrue(minesweeper.has_player_won())

class TestGameOverCondition(unittest.TestCase):
    def setUp(self):
        pass

    def test_game_over_on_mine_reveal(self):
        minesweeper.grid = [
            [-1, 1, 1],
            [1, 2, 1],
            [0, 1, 1]
        ]
        minesweeper.revealed = [
            [False, False, False],
            [False, False, False],
            [False, False, False]
        ]
        minesweeper.mines = {(0, 0)}
        game_over = minesweeper.handle_tile_click(0, 0)

        self.assertTrue(game_over)

if __name__ == "__main__":
    unittest.main()
