import unittest
import pygame
import Crossword
from Crossword import print_pics
from Crossword import draw_text

class TestCrossword(unittest.TestCase):

    def test_draw_word1(self):
        test1 = 'Fantastic Four'
        output = Crossword.print_pics(test1)
        self.assertEqual(output, True)

    def test_draw_word2(self):
        test2 = 'Cars'
        output2 = Crossword.print_pics(test2)
        self.assertEqual(output2, True)

class IntegrationTest(unittest.TestCase):

    def test_input(self):
        test1 = 'Fantastic Four'
        output = Crossword.print_pics(test1)
        self.assertEqual(output, True)

        test2 = 'Cars'
        output2 = Crossword.print_pics(test2)
        self.assertEqual(output2, True)

        run = True
        output3 = run
        self.assertEqual(output3, True)


if __name__ == '__main__':
    unittest.main()
