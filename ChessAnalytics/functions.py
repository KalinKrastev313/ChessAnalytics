import io
import urllib, base64
import matplotlib.pyplot as plt

import chess.engine
import chess.pgn
from ChessAnalytics.settings import ENGINE_DIRECTORIES


def determine_square_color(row, col):
    if (row % 2 == 1 and col % 2 == 0) or (row % 2 == 0 and col % 2 == 1):
        return "white"
    else:
        return "black"


pieces_image_directories = {
    'k': '/static/pieces/king-black.png',
    'q': '/static/pieces/queen-black.png',
    'r': '/static/pieces/rook-black.png',
    'n': '/static/pieces/knight-black.png',
    'b': '/static/pieces/bishop-black.png',
    'p': '/static/pieces/pawn-black.png',
    'K': '/static/pieces/king-white.png',
    'Q': '/static/pieces/queen-white.png',
    'R': '/static/pieces/rook-white.png',
    'N': '/static/pieces/knight-white.png',
    'B': '/static/pieces/bishop-white.png',
    'P': '/static/pieces/pawn-white.png',
}


class Position:
    def __init__(self, fen):
        self.fen = fen
        # self.squares_dict = {}
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

    # def add_square_to_squares_dict(self, row, col, occupied_by=False):
    #     square_name = self.get_square_name(row, col)
    #     self.squares_dict[square_name] = {}
    #     self.squares_dict[square_name]['name'] = square_name
    #     self.squares_dict[square_name]['color'] = "square " + determine_square_color(8 - row, col)
    #     self.squares_dict[square_name]['occupied_by'] = occupied_by

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

            # if evaluation.is_digit():

            # else:
            #     best_lines.append({'eval': line['score'], 'line_moves': main_line})
        return best_lines

    @staticmethod
    def turn_move_objects_to_string(move_line_objects):
        main_line = ""
        for m in move_line_objects:
            main_line += m.uci() + ','
        return main_line


# def render_engine(engine_name):
#     engine_path = ENGINE_DIRECTORIES[engine_name]
#     return chess.engine.SimpleEngine.popen_uci(engine_path)
#     # return chess.engine.SimpleEngine.popen_uci(r"C:\Users\User\Documents\PythonWeb\ChessAnalytics\chessEngines\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")
#
#
# def turn_move_objects_to_string(move_line_objects):
#     main_line = ""
#     for m in move_line_objects:
#         main_line += m.uci() + ','
#     return main_line
#
#
# def extract_lines_from_engine_info(info):
#     best_lines = []
#     for line in info:
#         evaluation = line['score'].white().score()
#         move_line_objects = line['pv']
#         main_line = turn_move_objects_to_string(move_line_objects)
#         best_lines.append({'eval': (float(evaluation / 100)), 'line_moves': main_line})
#     return best_lines


# def get_engine_evaluation(fen, engine_name, depth, lines=1, cpu=None, memory=None,):
#     engine = render_engine(engine_name)
#     board = chess.Board(fen=fen)
#     info = engine.analyse(board, chess.engine.Limit(depth=depth,), multipv=lines)
#     return extract_lines_from_engine_info(info)


# def concat_engine_lines(engine_lines):
#     engine_lines_concat = []
#     for line in engine_lines:
#         engine_lines_concat.append(str(line['eval']) + "/" + line["line_moves"])
#     return "|".join(engine_lines_concat)


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


# def get_squares_data_for_a_move_from_line(fen, lines, line_index, halfmove):
#     needed_line = ((lines.split('|')[line_index]).split('/'))[1]
#     moves_list = [needed_line[i:i+4] for i in range(0, len(needed_line) - 1, 4)]
#     board = chess.Board(fen=fen)
#     for move_index in range(halfmove):
#         board.push(chess.Move.from_uci(moves_list[move_index]))
#
#     position = Position(board.fen())
#     squares_data = position.get_squares_data()
#     return squares_data

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
    # moves_eval_lst.pop()
    # moves_eval_lst = moves_evaluations.split('/')
    # moves_eval_lst.pop()
    # moves_eval_lst = list(map(int, moves_eval_lst))
    corrected_scores = []
    for ev in moves_eval_lst:
        if ev in range(-300, 300):
            corrected_scores.append(ev / 100)
        elif ev > 300:
            corrected_scores.append(3)
        else:
            corrected_scores.append(-3)
    plt.plot(corrected_scores)
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
