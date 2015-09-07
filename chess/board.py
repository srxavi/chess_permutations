from __future__ import print_function

import copy

from chess.pieces import create_piece


class Board(object):
    """
    Class that models a board as a set of columns and rows with a list of
    placed pieces.
    """
    def __init__(self, rows, columns, pieces=None):
        self.rows = rows
        self.columns = columns
        self.pieces = pieces or []

    def get_row_column(self, offset):
        """Get the row and the column given an offset."""
        return divmod(offset, self.columns)

    def get_offset(self, row, column):
        """Return an offset given a row and a column."""
        return row * self.columns + column

    def get_piece_offsets(self):
        """Return all the used offsets in the board."""
        return [self.get_offset(piece.row, piece.column) for piece in
                self.pieces if piece.is_placed()]

    def is_safe(self, piece):
        """Check if a piece is save in a given position."""
        for placed in self.pieces:
            if placed.is_attacking(piece) or piece.is_attacking(placed):
                return False
        return True

    def __str__(self):
        data = [['.' for _ in range(self.columns)] for _ in range(self.rows)]
        for piece in self.pieces:
            data[piece.x][piece.y] = '{}'.format(piece)
        return '\n'.join(
            [''.join(['{}'.format(item) for item in row]) for row in data])

    def place_piece(self, piece, offset):
        """
        Place a piece in the next available position starting from the offset.
        """
        if offset >= self.rows * self.columns:
            raise ValueError("Out of Bounds")
        for next_offset in range(offset, self.rows * self.columns):
            row, column = self.get_row_column(next_offset)
            if self.is_safe(create_piece(piece.name, row, column)):
                piece.row, piece.column = row, column
                self.pieces.append(piece)
                return next_offset
        raise ValueError("Out of Bounds")

    def remove_piece(self, piece):
        """
        Remove a piece from the board.
        """
        self.pieces.remove(piece)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (self.rows == other.rows and
                self.columns == other.columns and
                self.pieces == other.pieces)

    def __copy__(self):
        return Board(self.rows, self.columns, list(self.pieces))


def place_pieces(board_list, board, pieces, index=0, offset=0):
    """
    Backtracking algorithm to place a list of pieces in the board.

    :param board_list: list of found boards
    :param board: current board
    :param pieces: list of pieces
    :param index: current piece index
    :param offset: current starting offset
    :return:
    """
    if index == len(pieces):
        board_list.append(board)
    else:
        current_offset = offset
        piece = create_piece(pieces[index])
        while current_offset < (board.rows * board.columns):
            try:
                used_offset = board.place_piece(piece, current_offset)
            except ValueError:
                break
            place_pieces(board_list, copy.deepcopy(board), pieces, index + 1,
                         used_offset + 1)
            board.remove_piece(piece)
            current_offset = used_offset + 1


def build_boards(rows, columns, permutation):
    """

    :param permutation: :type list
    :return:
    """
    boards = []
    board = Board(rows, columns)
    place_pieces(boards, board, permutation, 0, 0)
    return set(boards)


def build_permutations(permutations, initial, final=None):
    """
    Create all the possible permutations of a list of pieces.
    :type permutations: list
    :type final: list
    :type initial: list
    """
    if not final:
        final = []
    if not initial:
        if final not in permutations:
            permutations.append(final)
    else:
        for position, _ in enumerate(initial):
            initial_copy = list(initial)
            final_copy = list(final)
            final_copy.append(initial_copy.pop(position))
            build_permutations(permutations, initial_copy, final_copy)


def build_board_set(rows, columns, list_of_pieces):
    """
    Build all the possible boards.
    :param rows:
    :param columns:
    :param list_of_pieces:
    :return:
    """
    permutations = []
    board_set = set()
    build_permutations(permutations, list_of_pieces)
    for permutation in permutations:
        boards = build_boards(rows, columns, permutation)
        board_set.update(boards)
    return board_set
