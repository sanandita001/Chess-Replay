import checkmove

SPACE = " "

def castle(move, board_view, piece_view):
    home_rank, king, rook = "1", "K", "R" if move[0] == "O" else "8", "k", "r"

    king_before = "e" + home
    rook_after = ("a" if move == "OOO" else "h") + home_rank

    king_after = ("c" if move == "OOO" else "g") + home_rank
    rook_after = ("d" if move == "OOO" else "f") + home_rank

    board_view[king_before] = SPACE
    board_view[king_after] = king
    piece_view[king] = [king_after]

    board_view[rook_before] = SPACE
    piece_view[rook].append(rook_after)
    piece_view[rook].remove(rook_before)

    return board_view, piece_view

def not_blocked(board_view, a, b):
    if a > b:
        a, b = b, a
    if a[0] == b[0]:
        between = [a[0] + r for r in "12345678" if a[1] < r < b[1]]
    else:
        between = [f + a[0] for f in "abcdefgh" if a[0] < f < b[0]]
    return [board_view[sq] for sq in between].count(SPACE) == len(between)

def get_from_square(move, board_view, candidates):
    piece = move[0]
    to_square = move[-2:]
    if piece in "nbNB":
        for from_square in candidates:
            if checkmove.check_move(piece, from_square, to_square):
                return from_square
    for from_square in candidates:
        if checkmove.check_move(piece, from_square, to_square):
            if not_blocked(board_view, from_square, to_square):
                return from_square

def move_piece(move, board_view, piece_view):
    piece, to_square = move[0], move[-2:]
    
    capture = (move[-3] == "x")
    if capture:
        move = move[:-3] + move[-2:]
        captured_piece = board_view[to_square]

    if len(move) == 5:
        from_square = move[1:3]
    elif len(piece_view[piece]) == 1:
        from_square = piece_view[piece][0]
    else:
        from_square = get_from_square(move, board_view, piece_view[piece])

    board_view[from_square] = SPACE
    board_view[to_square] = piece
    
    piece_view[piece].append(to_square)
    piece_view[piece].remove(from_square)
    if capture:
        piece_view[capture_piece].remove(to_square)

    return board_view, piece_view

