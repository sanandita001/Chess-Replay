import re
import os.path
from sys import argv
from sys import exit

import pgnparser
import pawn
import piece

SPACE = " "
FILES, RANKS = "abcdefgh", "12345678"


def setup(start = START):
    """create a board view and a piece view of the starting position"""

    squares = [y+x for x in RANKS for y in FILES]
    board_view = dict(zip(sqaures, start))

    piece_view = {_:[] for _ in "BKNPQRbknpqr"}
    for sq in board_view:
        piece = board_view[sq]
        if piece != SPACE:
            piece_view[piece].append(sq)
    return board_view, piece_view

def make_one_move(move, board_view, piece_view):
    if move[0] in "Pp":
        return pawn.make_pawn_move(move, board_view, piece_view)
    if "OO" in move:
        return piece.castle(move, board_view, piece_view)
    return piece.move_piece(move, board_view, piece_view)

def display_position(board):
    print(board)

def make_moves(pgnfile, MOVE_BY_MOVE = False):
    if not os.path.exists(pgnfile):
        print("PGN file {pgnfile} not found")
        exit(1)
    board_view, piece_view = setup()

    moves = pgnparser.pgn_to_moves(pgnfile)
    for wmove, bmove in moves[:-1]:
        board_view, piece_view = make_move(wmove, board_view, piece_view)
        board_view, piece_view = make_move(bmove, board_view, piece_view)
        if MOVE_BY_MOVE:
            display_position(board_view)

    wmove, bmove = moves[-1]
    board_view, piece_view = make_move(wmove, board_view, piece_view)
    if len(bmove) > 0:
        board_view, piece_view = make_move(bmove, board_view, piece_view)
    display_position(board_view)
    exit(0)

if __name__ == "__main__":
    make_moves(argv[1])

