from abc import ABCMeta, abstractmethod

UNPLACED = -1


class Piece(object):
    __metaclass__ = ABCMeta
    name = ''

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_attacking(self, piece):
        return self.is_attacking_position(piece.x, piece.y)

    @abstractmethod
    def is_attacking_position(self, row, column):
        pass

    def is_placed(self):
        return not (self.x == UNPLACED or self.x == UNPLACED)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{}@({},{})".format(self.name, self.x, self.y)

    def __eq__(self, other):
        return (self.name == other.name and
                self.x == other.x and
                self.y == other.y)


class Rook(Piece):
    name = 'R'

    def is_attacking_position(self, row, column):
        if self.is_placed():
            return (self.x == row) or (self.y == column)


class King(Piece):
    name = 'K'

    @property
    def moves(self):
        x, y = self.x, self.y
        return frozenset([
            (x, y + 1), (x, y - 1), (x + 1, y), (x + 1, y + 1),
            (x + 1, y - 1), (x - 1, y), (x - 1, y + 1), (x - 1, y - 1)])

    def is_attacking_position(self, row, column):
        if self.is_placed():
            return (row, column) in self.moves


class Queen(Piece):
    name = 'Q'

    def is_attacking_position(self, row, column):
        if self.is_placed():
            return row == self.x or column == self.y or abs(
                row - self.x) == abs(column - self.y)


class Bishop(Piece):
    name = 'B'

    def is_attacking_position(self, row, column):
        if self.is_placed():
            return abs(row - self.x) == abs(column == self.y)


class Knight(Piece):
    name = 'N'

    @property
    def moves(self):
        x, y = self.x, self.y
        return frozenset([
            (x + 1, y - 2), (x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 2),
            (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1), (x - 1, y - 2)])

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
        x = int(pos_x)
        y = int(pos_y)
    except ValueError:
        raise ValueError('Coordinates must be integers')

    if isinstance(piece, basestring):
        try:
            return PIECES.get(piece.lower())(x, y)
        except KeyError:
            raise ValueError('Non-existent type of piece')
    elif isinstance(piece, Piece):
        return type(piece)(x, y)
    else:
        raise ValueError('A piece must be either a string or a Piece')
