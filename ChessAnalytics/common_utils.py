import io

import chess.pgn


def get_fen_from_pgn_at_move_n(pgn_moves, n):
    # n is in halfmoves
    pgn = io.StringIO(pgn_moves)
    game = chess.pgn.read_game(pgn)
    board = game.board()
    counter = 1
    for move in game.mainline_moves():
        board.push(move)
        if counter == n:
            break
        counter += 1

    return board.fen()


def turn_line_to_moves_info(fen, line):
    moves = []
    halfmoves = 1
    board = chess.Board(fen=fen)

    for move in line.split(','):
        algebraic_notation = board.san(chess.Move.from_uci(move))

        m = {'notation': move, 'halfmove': halfmoves, 'algebraic_notation': algebraic_notation}
        moves.append(m)
        halfmoves += 1
        board.push(chess.Move.from_uci(move))
    return moves


def create_a_square_from_str(comes_from):
    # files and ranks should start from 0 index and this is why we derive from them.
    file = ord(comes_from[0]) - 97
    rank = int(comes_from[1]) - 1
    square = chess.square(file_index=file, rank_index=rank)
    return square


def get_fen_at_halfmove_from_uci_moves_lst(initial_fen: str, moves_uci_lst: list[str], halfmove: int):
    board = chess.Board(fen=initial_fen)
    moves_uci_lst_len = len(moves_uci_lst)
    # Instead of error handling, goes to the last move
    if halfmove not in range(-moves_uci_lst_len, moves_uci_lst_len + 1):
        halfmove = moves_uci_lst_len
    halfmove_abs = halfmove
    if halfmove < 0:
        halfmove_abs = moves_uci_lst_len - abs(halfmove) + 1

    if moves_uci_lst_len > 0:
        for move_index in range(halfmove_abs):
            board.push(chess.Move.from_uci(moves_uci_lst[move_index]))

    return board.fen()


def coordinate_to_algebraic_notation(board: chess.Board, coordinate_notation: str):
    piece_type = board.piece_type_at(chess.parse_square(coordinate_notation[:2]))
    return f"{(chess.piece_symbol(piece_type)).upper()}{coordinate_notation[2:]}"


def save_a_comment_from_form(comment_form, position_pk: int, user_pk: int):
    new_comment = comment_form.save(commit=False)
    new_comment.to_position_id = position_pk
    new_comment.to_user_id = user_pk
    new_comment.save()
