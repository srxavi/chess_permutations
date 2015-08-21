from __future__ import print_function

import copy

from pip.util import get_terminal_size

from pieces import create_piece


class Board(object):
    def __init__(self, rows, columns, pieces=None):
        self.rows = rows
        self.columns = columns
        self.pieces = pieces or []

    def get_row_column(self, offset):
        return divmod(offset, self.columns)

    def get_offset(self, row, column):
        return row * self.columns + column

    def get_piece_offsets(self):
        return map(lambda x: self.get_offset(x.x, x.y),
                   filter(lambda x: x.is_placed(), self.pieces))

    def is_safe(self, piece):
        for p in self.pieces:
            if p.is_attacking(piece) or piece.is_attacking(p):
                return False
        return True

    def __str__(self):
        data = [['.' for _ in range(self.columns)] for _ in range(self.rows)]
        for piece in self.pieces:
            data[piece.x][piece.y] = '{}'.format(piece)
        return '\n'.join(
            [''.join(['{}'.format(item) for item in row]) for row in data])

    def place_piece(self, piece, offset):
        if offset >= self.rows * self.columns:
            raise ValueError("Out of Bounds")
        for next_offset in range(offset, self.rows * self.columns):
            row, column = self.get_row_column(next_offset)
            if self.is_safe(create_piece(piece.name, row, column)):
                piece.x, piece.y = row, column
                self.pieces.append(piece)
                return next_offset
        raise ValueError("Out of Bounds")

    def remove_piece(self, piece):
        self.pieces.remove(piece)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (self.rows == other.rows and
                self.columns == other.columns and
                self.pieces == other.pieces)

    def __copy__(self):
        return Board(self.rows, self.columns, list(self.pieces))


class BoardPermutation(object):
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns

    def build_boards(self, list_of_piece_names):
        permutations = []
        board_list = set()
        build_permutations(permutations, [], list_of_piece_names)
        for pos, permutation in enumerate(permutations):
            boards = self.build_board(permutation)
            board_list.update(set(boards))
        return board_list

def place_pieces(board_list, board, pieces, index=0, offset=0):
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
            place_pieces(board_list, copy.deepcopy(board), pieces, index+1,
                              used_offset+1)
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
    permutations = []
    board_set = set()
    build_permutations(permutations, list_of_pieces)
    for permutation in permutations:
        boards = build_boards(rows, columns, permutation)
        board_set.update(boards)
    return board_set