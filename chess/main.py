import argparse
from time import time

from progressbar import ProgressBar, AdaptiveETA, Bar

from chess.board import build_boards, build_permutations
from chess.processing import parmap


def build_board_permutations(rows, columns, used_pieces, nprocs):
    """
    Build all the board permutations in parallel.

    :param rows:
    :param columns:
    :param used_pieces:
    :param nprocs:
    :return:
    """
    permutations = build_permutations(used_pieces)

    progress_bar = ProgressBar(maxval=len(permutations),
                               widgets=[Bar(), AdaptiveETA()]).start()
    board_set = set()
    parallel_args = [(rows, columns, perm) for perm in permutations]
    built_boards = parmap(build_boards, parallel_args, nprocs, progress_bar)
    for board in built_boards:
        board_set.update(board)
    progress_bar.finish()
    return board_set


def main():
    """
    Main function.

    :return:
    """
    parameters = argparse.ArgumentParser(description="Chess problem")
    parameters.add_argument("--rows", "-r", type=int, default=7,
                            help="Number of rows in the board")
    parameters.add_argument("--columns", "-c", type=int, default=7,
                            help="Number of columns in the board")
    parameters.add_argument("--pieces", "-p", default="kkqqbbn",
                            help="List of pieces in the board (kkbbr)")
    parameters.add_argument("--workers", "-w", type=int, default=1,
                            help="Number of parallel workers")
    args = parameters.parse_args()
    pieces = list(args.pieces)
    init = time()
    boards = build_board_permutations(args.rows, args.columns, pieces,
                                      args.workers)
    now = time() - init
    print("There are a total of %s possibilities and it took %s "
          "seconds to find them" % (len(boards), now))


if __name__ == "__main__":
    main()
