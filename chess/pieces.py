"""
Piece definitions.
"""
from abc import ABCMeta, abstractmethod

UNPLACED = -1


class Piece(object):
    """
    Base model for the pieces.
    """
    __metaclass__ = ABCMeta
    name = ''

    def __init__(self, row=UNPLACED, column=UNPLACED):
        self.row = row
        self.column = column

    @abstractmethod
    def is_attacking_position(self, row, column):
        """
        Abstract method that needs to be defined to check if a piece is
        attacking the given position.
        """
        pass

    def is_attacking(self, piece):
        """
        Check if we are attacking the other piece and viceversa.
        """
        return self.is_attacking_position(piece.row, piece.column)

    def is_placed(self):
        """Check if the piece is placed"""
        return not (self.row == UNPLACED or self.row == UNPLACED)

    def place(self, row, column):
        """Place the piece in the given position."""
        self.row, self.column = row, column

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{}@({},{})".format(self.name, self.row, self.column)

    def __eq__(self, other):
        return (self.name == other.name and
                self.row == other.row and
                self.column == other.column)


class Rook(Piece):
    """
    Model for the rook.
    """
    name = 'R'

    def is_attacking_position(self, row, column):
        if self.is_placed():
            return (self.row == row) or (self.column == column)


class King(Piece):
    """
    Model for the king.
    """
    name = 'K'

    @property
    def moves(self):
        """Places where the piece can move to."""
        row, column = self.row, self.column
        return frozenset([
            (row, column), (row, column + 1), (row, column - 1),
            (row + 1, column), (row + 1, column + 1), (row + 1, column - 1),
            (row - 1, column), (row - 1, column + 1), (row - 1, column - 1)])

    def is_attacking_position(self, row, column):
        if self.is_placed():
            return (row, column) in self.moves


class Queen(Piece):
    """
    Model for the queen.
    """
    name = 'Q'

    def is_attacking_position(self, row, column):
        if self.is_placed():
            return row == self.row or column == self.column or abs(
                row - self.row) == abs(column - self.column)


class Bishop(Piece):
    """
    Model for the bishop.
    """
    name = 'B'

    def is_attacking_position(self, row, column):
        if self.is_placed():
            return abs(row - self.row) == abs(column - self.column)


class Knight(Piece):
    """
    Model for the knight.
    """
    name = 'N'

    @property
    def moves(self):
        """Places where the piece can move to."""
        row, column = self.row, self.column
        return frozenset([
            (row, column), (row + 1, column - 2), (row + 2, column - 1),
            (row + 2, column + 1), (row + 1, column + 2),
            (row - 1, column + 2), (row - 2, column + 1),
            (row - 2, column - 1), (row - 1, column - 2)])

    def is_attacking_position(self, row, column):
        if self.is_placed():
            return (row, column) in self.moves


PIECES = {
    'k': King,
    'q': Queen,
    'n': Knight,
    'r': Rook,
    'b': Bishop
}


def create_piece(piece, pos_x=UNPLACED, pos_y=UNPLACED):
    """
    Return a piece of the correct type in the current position.
    :param piece: Piece identifier
    :param pos_x: X coordinate
    :param pos_y: Y coordinate
    :return: An instance of the current piece
    """
    try:
        row = int(pos_x)
        column = int(pos_y)
    except ValueError:
        raise ValueError('Coordinates must be integers')

    if isinstance(piece, basestring):
        try:
            return PIECES.get(piece.lower())(row, column)
        except KeyError:
            raise ValueError('Non-existent type of piece')
    elif isinstance(piece, Piece):
        return type(piece)(row, column)
    else:
        raise ValueError('A piece must be either a string or a Piece')
