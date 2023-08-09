import chess.engine
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


def render_engine(engine_name):
    engine_path = ENGINE_DIRECTORIES[engine_name]
    return chess.engine.SimpleEngine.popen_uci(engine_path)
    # return chess.engine.SimpleEngine.popen_uci(r"C:\Users\User\Documents\PythonWeb\ChessAnalytics\chessEngines\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")


def get_engine_evaluation(fen, engine_name, depth, lines=1, cpu=None, memory=None,):
    engine = render_engine(engine_name)
    board = chess.Board(fen=fen)
    info = engine.analyse(board, chess.engine.Limit(depth=depth,), multipv=lines)
    best_lines = []
    for line in info:
        evaluation = line['score'].white().score()
        main_line_objects = line['pv']
        main_line = ""
        for m in main_line_objects:
            main_line += m.uci()

        best_lines.append({'eval': (float(evaluation / 100)), 'line_moves': main_line})
    return best_lines


def evaluate_position(request, fen):
    if request.method == 'POST':
        engine_name = "Stockfish"
        depth = request.POST.get('depth')
        lines = request.POST.get('lines')
        best_lines = get_engine_evaluation(fen=fen, engine_name=engine_name, depth=depth, lines=lines)
        best_lines_concat = []
        for line in best_lines:
            best_lines_concat.append(str(line['eval']) + "/" + line["line_moves"])
        return "|".join(best_lines_concat)
    # else:
    #     return HttpResponse('Invalid request method')


def coordinate_to_algebraic_notation(board, coordinate_notation):
    piece_type = board.piece_type_at(chess.parse_square(coordinate_notation[:2]))
    return f"{(chess.piece_symbol(piece_type)).upper()}{coordinate_notation[2:]}"


