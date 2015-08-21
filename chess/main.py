import argparse
from time import time

from progressbar import ProgressBar, AdaptiveETA, Bar

from board import build_boards, build_permutations
from processing import parmap


def build_board_permutations(rows, columns, pieces, nprocs):
    permutations = []
    build_permutations(permutations, pieces)

    pb = ProgressBar(maxval=len(permutations),
                     widgets=[Bar(), AdaptiveETA()]).start()
    board_set = set()
    parallel_args = [(rows, columns, perm) for perm in permutations]
    boards = parmap(build_boards, parallel_args, nprocs, pb)
    for board in boards:
        board_set.update(board)
    pb.finish()
    return board_set


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Chess problem")
    p.add_argument("--rows", "-r", type=int, default=7,
                   help="Number of rows in the board")
    p.add_argument("--columns", "-c", type=int, default=7,
                   help="Number of columns in the board")
    p.add_argument("--pieces", "-p", default="kkqqbbn",
                   help="List of pieces in the board (kkbbr)")
    p.add_argument("--workers", "-w", type=int, default=1,
                   help="Number of parallel workers")
    args = p.parse_args()
    pieces = list(args.pieces)
    init = time()
    boards = build_board_permutations(args.rows, args.columns, pieces,
                                      args.workers)
    now = time() - init
    print("There are a total of %s possibilities and it took %s "
          "seconds to find them" % (len(boards), now))
