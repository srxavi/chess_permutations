import unittest

from chess.board import Board, BoardPermutation
from chess.pieces import create_piece


class TestBoard(unittest.TestCase):

    def test_get_offset(self):
        board = Board(3, 3)
        self.assertTupleEqual(board.get_row_column(4), (1, 1))

    def test_get_row_column(self):
        board = Board(3, 3)
        self.assertEqual(board.get_offset(2, 2), 8)

    def test_place_pieces(self):
        k1 = create_piece('k')
        k2 = create_piece('k')
        board = Board(3, 3)
        self.assertEqual(board.place_piece(k1, 0), 0)
        self.assertEqual(board.place_piece(k2, 0), 2)

    def test_is_safe(self):
        k1 = create_piece('k')
        q1 = create_piece('q', 1, 2)
        board = Board(3, 3)
        board.place_piece(k1, 0)
        self.assertTrue(board.is_safe(q1))


class TestBoardPermutation(unittest.TestCase):

    def test_build_permutations(self):
        permutations = []
        bp = BoardPermutation(3, 3)
        bp.build_permutations(permutations, [], ['r', 'q', 'k', 'n', 'b'])
        self.assertEqual(len(permutations), 120)

    def test_build_boards(self):
        bp = BoardPermutation(3, 3)
        boards = bp.build_boards(['k', 'k', 'r'])
        self.assertEqual(len(boards), 4)


