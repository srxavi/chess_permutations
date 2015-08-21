import unittest

from chess.pieces import create_piece, King, Queen, Bishop, Rook, Knight

class TestPieces(unittest.TestCase):

    def test_create_pieces(self):
        self.assertEqual(create_piece('k'), King())
        self.assertEqual(create_piece('q'), Queen())
        self.assertEqual(create_piece('b'), Bishop())
        self.assertEqual(create_piece('r'), Rook())
        self.assertEqual(create_piece('n'), Knight())

    def test_place_piece(self):
        king = King()
        king.place(0, 0)
        self.assertTupleEqual((king.x, king.y), (0, 0))

    def test_king_attacks(self):
        king = create_piece('k', 0, 0)
        self.assertTrue(king.is_attacking_position(1, 1))
        self.assertFalse(king.is_attacking_position(2, 2))

    def test_queen_attacks(self):
        queen = create_piece('q', 0, 0)
        for i in range(1, 8):
            self.assertTrue(queen.is_attacking_position(i, i))
            self.assertTrue(queen.is_attacking_position(i, 0))
            self.assertTrue(queen.is_attacking_position(0, i))
            self.assertFalse(queen.is_attacking_position(i, i + 1))

    def test_rook_attacks(self):
        rook = create_piece('r', 0, 0)
        for i in range(1, 8):
            self.assertTrue(rook.is_attacking_position(0, i))
            self.assertTrue(rook.is_attacking_position(i, 0))
            self.assertFalse(rook.is_attacking_position(i, i))

    def test_bishop_attacks(self):
        bishop = create_piece('b', 0, 0)
        for i in range(1, 8):
            self.assertTrue(bishop.is_attacking_position(i, i))
            self.assertFalse(bishop.is_attacking_position(0, i))

    def test_knight_attacks(self):
        knight = create_piece('n', 0, 0)
        self.assertTrue(knight.is_attacking_position(1, 2))
        self.assertTrue(knight.is_attacking_position(2, 1))
        self.assertFalse(knight.is_attacking_position(1, 1))