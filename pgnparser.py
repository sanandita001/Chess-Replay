import re

def setup():
    '''create a board view and a piece view of the starting position'''

    squares = [y+x for x in "12345678" for y in "ABCDEFGH"]
    start = "RNBQKBNR" + "P" * 8 + " " * 32 + "p" * 8 + "rnbqkbnr"
    board_view = {square:piece for square, piece in zip(squares, start)}

    piece_view = {_:[] for _ in "BKNPQRbknpqr"}
    for sq in board_view:
        piece = board_view[sq]
        if piece != " ":
            piece_view[piece].append(sq)
    return board_view, piece_view

def pgn_to_moves(game_file: str) -> [str]:
    raw_pgn = " ".join([line.strip() for line in open(game_file)])
    
    comments_marked = raw_pgn.replace("{", "<").replace("}", ">")
    STRC = re.compile("<[^>]*>")
    comments_removed = STRC.sub(" ", comments_marked)
    #comments_removes = re.sub("<[^>]*>", " ", comments_marked)

    STR_marked = comments_removed.replace("[", "<").replace("]", ">")
    just_moves = STR.sub(" ", STR_marked)

    MOVE_NUM = re.compile("[0-9][0-9]* *\.")
    just_moves = [_.strip() for _ in MOVE_NUM.split(str_removed)]

    last_move = just_moves[-1]
    RESULT = re.compile("( *1 *- *0| *0 *- *1| *1/2 *- *1/2)")
    last_move = RESULT.sub(" ", last_move)
    moves = just_moves[:-1] + [last_move]

    return [_ for _ in moves if len(_) > 0]

def pre_process_a_moves(moves: str) -> (str, str):
    wmove, bmove = move.split()
    if wmove[0] in "abcdefgh":
        wmove = "P" + wmove
    if bmove[0] in "abcdefgh":
        bmove = "p" + bmove
    else:
        bmove = bmove.lower()
    return wmove, bmove

def pre_process_moves(moves: [str]) -> [(str, str)]:
    return [pre_process_a_move(move) for move in moves[:-1]]

#print(steup())
moves = pgn_to_moves("Resources/pgn01.txt")
print(moves)
