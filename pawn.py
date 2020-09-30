import re

SPACE = " "
WHITE, BLACK = "P", "p"
can_move_from = {WHITE: {"3": ["2"], "4": ["2", "3"], "5": ["4"], "6": ["5"], "7": ["6"]},\
                 BLACK: {"6": ["7"], "5": ["7", "6"], "4": ["5"], "3": ["4"], "2": ["3"]} }

can_capture_from = {WHITE: {"3":"2", "4":"3", "5":"4", "6":"5", "7":"6", "8":"7"},\
                    BLACK: {"6":"7", "5":"6", "4":"5", "3":"4", "2":"3", "1":"2"}}

enpassant_captured = {WHITE: "5", BLACK: "4"}
promoted_from = {WHITE: "7", BLACK: "2"}

def is_regular_pawn_move(move):
    return re.fullmatch("[Pp][a-h][2-7]", move) is not None

def is_capture(move):
    return re.fullmatch("[Pp][a-h]x?[a-h][2-7]?)", move) is not None

def is_promotion(move):
    return re.match("[Pp][a-h]([18]|x[a-h][18])", move) is not None

def is_enpassant(move):
    return move.endswith("ep")

def move_pawn(move, board_view, piece_view):
    pawn, to_square = move[0], move[1:]
    to_file, to_rank = to_square[0], to_square[1]
    for move_from in can_move_from[pawn][to_rank]:
        from_square = to_file + move_from
        if board_view[from_square] == pawn:
            board_view[from_square] = SPACE
            board_view[to_square] = pawn
            piece_view[pawn].remove(from_square)
            piece_view[pawn].append(to_square)

            return board_view, piece_view

def capture(move, board_view, piece_view):
    move = move.replace("x", "")
    pawn, from_file, to_square = move[0], move[1], move[2:]
    captured_piece = board_view[to_square]
    board_view[to_square] = pawn

    to_rank = to_square[1]
    from_square = from_file + can_capture_from[pawn][to_rank]

    board_view[from_square] = SPACE
    piece_view[captured_piece].remove(to_square)

    return board_view, piece_view

def promote(move, board_view, piece_view):
    if "x" in move:
        #Move like gxf8=Q or gxf8Q
        pawn, from_file, promoted_at, promoted_to = move[0], move[1], move[3:5], move[-1]
        captured_piece = board_view[promoted_at]
        piece_view[captured_piece].remove(promoted_at)
    else:
        #Move like f8Q or f8=Q
        pawn, from_file, promoted_at, promoted_to = move[0], move[1], move[1:3], move[-1]
   
   board_view[promoted_at] = promoted_to
   piece_view[promoted_to].append(promoted_to)

   from_square = from_file + promoted_from[pawn]
   piece_view[pawn].remove(from_square)

   return board_view, piece_view

def make_enpassant(move, board_view, piece_view):
    move = move.replace("x","")
    pawn, from_file, to_square = move[0], move[1], move[2:4]
    to_file = to_square[0]

    from_square = from_file + enpassant_capture[pawn]
    captured_pawn_square = to_file + enpassant_captured[pawn]

    board_view[to_square] = pawn
    board_view[from_square] = SPACE
    board_view[captured_pawn_square] = SPACE

    piece_view[pawn].remove(from_square)
    piece_view[pawn].append(to_square)
    piece_view[pawn.swapcase()].remove(captured_pawn_square)

    return board_view, piece_view

def make_pawn_move(move, board_view, piece_view):
    if is_regular_pawn_move(move):
        return move_pawn(move, board_view, piece_view)
    if is_capture(move):
        return capture(move, board_view, piece_view)
    if is_promotion(move):
        return promote(move, board_view, piece_view)
    if is_enpassant(move):
        return make_enpassant(move, board_view, piece_view)

