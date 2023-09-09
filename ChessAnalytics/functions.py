import io
import urllib, base64
import matplotlib.pyplot as plt
import os
from django.conf import settings

import chess.engine
import chess.pgn
from ChessAnalytics.settings import ENGINE_DIRECTORIES


def determine_square_color(row, col):
    if (row % 2 == 1 and col % 2 == 0) or (row % 2 == 0 and col % 2 == 1):
        return "white"
    else:
        return "black"


pieces_image_directories = {
    'k': 'king-black.png',
    'q': 'queen-black.png',
    'r': 'rook-black.png',
    'n': 'knight-black.png',
    'b': 'bishop-black.png',
    'p': 'pawn-black.png',
    'K': 'king-white.png',
    'Q': 'queen-white.png',
    'R': 'rook-white.png',
    'N': 'knight-white.png',
    'B': 'bishop-white.png',
    'P': 'pawn-white.png',
}


class Position:
    def __init__(self, fen):
        self.fen = fen
        self.squares_data = []

    def get_squares_description_from_fen(self):
        squares = self.fen.split()[0]
        return squares

    def get_rows(self):
        return self.get_squares_description_from_fen().split("/")

    @staticmethod
    def get_square_name(row, col):
        return chr(col + 96) + str(8 - row)

    @staticmethod
    def determine_square_color(row, col):
        if (row % 2 == 1 and col % 2 == 0) or (row % 2 == 0 and col % 2 == 1):
            return "white"
        else:
            return "black"

    def is_white_to_move(self):
        side_to_move = self.fen.split()[1]
        if side_to_move == "w":
            return True
        else:
            return False

    def add_square_to_squares_data(self, row, col, occupied_by=False):
        square_name = self.get_square_name(row, col)
        square_data = {
            'name': square_name,
            'color': 'square ' + determine_square_color(8 - row, col),
            'occupied_by': occupied_by
        }
        self.squares_data.append(square_data)

    def fill_squares_dict_with_rows_info(self, rows_info):
        for row in range(8):
            current_col = 1
            for char in rows_info[row]:
                if char.isdigit():
                    for square in range(int(char)):
                        self.add_square_to_squares_data(row, current_col)
                        current_col += 1
                else:
                    self.add_square_to_squares_data(row, current_col, occupied_by=pieces_image_directories[char])
                    current_col += 1

    # def get_squares_dict(self):
    #     rows_info = self.get_rows()
    #     self.fill_squares_dict_with_rows_info(rows_info)
    #
    #     return self.squares_dict
    def get_squares_data(self):
        rows_info = self.get_rows()
        self.fill_squares_dict_with_rows_info(rows_info)

        return self.squares_data


class PositionEvaluator:
    def __init__(self, fen, depth, requested_lines, engine_name='Stockfish'):
        self.fen = fen
        self.depth = depth
        self.lines = requested_lines
        self.engine_name = engine_name
        self.info = None

    def render_engine(self):
        engine_path = ENGINE_DIRECTORIES[self.engine_name]
        return chess.engine.SimpleEngine.popen_uci(engine_path)

    # def evaluate_position(self):
    #     return get_engine_evaluation(fen=self.fen, engine_name=self.engine_name, depth=self.depth, lines=self.lines)

    def get_engine_evaluation(self, cpu=None, memory=None, ):
        engine = self.render_engine()
        board = chess.Board(fen=self.fen)
        self.info = engine.analyse(board, chess.engine.Limit(depth=self.depth, ), multipv=self.lines)
        return self.extract_lines_from_engine_info()

    def extract_lines_from_engine_info(self):
        best_lines = []
        for line in self.info:
            move_line_objects = line['pv']
            main_line = self.turn_move_objects_to_string(move_line_objects)

            if not line['score'].is_mate():
                evaluation = line['score'].white().score()
                is_mate = False
            else:
                evaluation = line['score'].white().mate()
                is_mate = True

            best_lines.append({'eval': evaluation, 'line_moves': main_line, 'is_mate': is_mate})

        return best_lines

    @staticmethod
    def turn_move_objects_to_string(move_line_objects):
        main_line = []
        for m in move_line_objects:
            main_line.append(m.uci())
        return ','.join(main_line)


def evaluate_position(request, fen):
    if request.method == 'POST':
        engine_name = "Stockfish"
        depth = request.POST.get('depth')
        lines = request.POST.get('lines')
        position_evaluator = PositionEvaluator(fen=fen, depth=depth, requested_lines=lines, engine_name=engine_name)
        best_lines = position_evaluator.get_engine_evaluation()
        # return concat_engine_lines(best_lines)
        return best_lines
    # else:
    #     return HttpResponse('Invalid request method')


def coordinate_to_algebraic_notation(board, coordinate_notation):
    piece_type = board.piece_type_at(chess.parse_square(coordinate_notation[:2]))
    return f"{(chess.piece_symbol(piece_type)).upper()}{coordinate_notation[2:]}"


def get_squares_data_for_a_move_from_line(fen, line, halfmove):
    moves_list = line.split(',')
    board = chess.Board(fen=fen)
    for move_index in range(halfmove):
        board.push(chess.Move.from_uci(moves_list[move_index]))

    position = Position(board.fen())
    squares_data = position.get_squares_data()
    return squares_data


def get_fen_at_move_n(pgn_moves, n):
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


def encode_plot(moves_evaluations):
    moves_eval_lst = list(map(int, moves_evaluations.split('/')))
    corrected_scores = []
    for ev in moves_eval_lst:
        if ev in range(-300, 300):
            corrected_scores.append(ev / 100)
        elif ev > 300:
            corrected_scores.append(3)
        else:
            corrected_scores.append(-3)
    plt.plot(corrected_scores)

    plt.xlabel("Move Number")
    plt.ylabel("Evaluation")
    # my_dpi = 97
    # plt.figure(figsize=(250 / my_dpi, 250 / my_dpi), dpi=my_dpi)
    plt.axhline(0, color='black', linewidth=.5)

    fig = plt.gcf()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    plt.close(fig)
    buf.close()
    return uri


def get_moves_evaluations(request, moves_notation):
    if request.method == 'POST':
        engine_name = "Stockfish"
        depth = request.POST.get('depth')
        game = chess.pgn.read_game(io.StringIO(moves_notation))
        board = game.board()
        evals = []
        for move in game.mainline_moves():
            engine = chess.engine.SimpleEngine.popen_uci(ENGINE_DIRECTORIES[engine_name])
            info = engine.analyse(board, chess.engine.Limit(depth=depth, ))
            if not info['score'].is_mate():
                evals.append(info['score'].white().score())
            else:
                evals.append(10000)
            board.push(move)

        evals.pop()
        return '/'.join([str(ev) for ev in evals])


def get_folder_names(directory_path):
    folder_names = []
    full_path = os.path.join(settings.BASE_DIR, directory_path)
    for item in os.listdir(full_path):
        item_path = os.path.join(full_path, item)
        if os.path.isdir(item_path):
            folder_names.append(item)
    return folder_names


# PIECES_HTML_SYMBOLS = {
#     'K': 9812,
#     'Q': 9813,
#     'R': 9814,
#     'B': 9815,
#     'N': 9816,
#     'P': 9817,
# }
# def algebraic_to_symbol_notation(algebraic_move):
#     piece_symbols = {
#         chess.PAWN: '♙♟',
#         chess.KNIGHT: '♘♞',
#         chess.BISHOP: '♗♝',
#         chess.ROOK: '♖♜',
#         chess.QUEEN: '♕♛',
#         chess.KING: '♔♚'
#     }
#
#     for piece, symbols in piece_symbols.items():
#         symbol_move = algebraic_move.replace(piece.symbol(), symbols[board.piece_at(move.from_square).color])
#
#     return symbol_move


def turn_line_to_moves_info(fen, line):
    moves = []
    halfmoves = 1
    board = chess.Board(fen=fen)

    for move in line.split(','):
        algebraic_notation = board.san(chess.Move.from_uci(move))
        # piece_color = board.piece_at()

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


class UCIValidator:
    def __init__(self, fen, comes_from, goes_to, promotes_to):
        self.fen = fen
        self.comes_from = comes_from
        self.goes_to = goes_to
        self.promotes_to = promotes_to
        self.is_legal = False
        self.is_promotion = False
        self.piece_color = True

    @property
    def promotes_to(self):
        return self._promotes_to.lower()

    @promotes_to.setter
    def promotes_to(self, value):
        if value:
            self._promotes_to = value
        else:
            self._promotes_to = ''

    def get_move_uci(self):
        return self.comes_from + self.goes_to + self.promotes_to

    def validate_move(self):
        board = chess.Board(fen=self.fen)
        move = chess.Move.from_uci(self.get_move_uci())
        self.is_legal = board.is_legal(move)
        square_comes_from = create_a_square_from_str(comes_from=self.comes_from)
        piece = board.piece_at(square=square_comes_from)
        self.piece_color = piece.color
        self.is_promotion = self.check_if_is_promotion(piece=piece, square=square_comes_from)
        return {
            'is_legal': self.is_legal,
            'is_promotion': self.is_promotion,
            # Piece color is bool value, where 'white' is True
            'piece_color': self.piece_color
        }

    @staticmethod
    def check_if_is_promotion(piece, square):
        if (str(piece) == 'P' and chess.square_rank(square) + 1 == 7) or (
                str(piece) == 'p' and chess.square_rank(square) + 1 == 2):
            return True

