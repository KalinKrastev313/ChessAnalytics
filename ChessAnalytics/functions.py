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
        self.squares_dict = {}

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

    def add_square_to_squares_dict(self, row, col, occupied_by=False):
        square_name = self.get_square_name(row, col)
        self.squares_dict[square_name] = {}
        self.squares_dict[square_name]['name'] = square_name
        self.squares_dict[square_name]['color'] = "square " + determine_square_color(8 - row, col)
        self.squares_dict[square_name]['occupied_by'] = occupied_by

    def fill_squares_dict_with_rows_info(self, rows_info):
        for row in range(8):
            current_col = 1
            for char in rows_info[row]:
                if char.isdigit():
                    for square in range(int(char)):
                        self.add_square_to_squares_dict(row, current_col)
                        current_col += 1
                else:
                    self.add_square_to_squares_dict(row, current_col, occupied_by=pieces_image_directories[char])
                    current_col += 1

    def get_squares_dict(self):
        rows_info = self.get_rows()
        self.fill_squares_dict_with_rows_info(rows_info)

        return self.squares_dict


def convert_fen_to_square_dict(fen):
    squares = fen.split()[0]
    squares_dict = {}
    rows_info = squares.split("/")
    for row in range(8):
        current_col = 1
        for char in rows_info[row]:
            if char.isdigit():
                for square in range(int(char)):
                    square_name = chr(current_col + 96) + str(8 - row)
                    squares_dict[square_name] = {}
                    squares_dict[square_name]['name'] = square_name
                    squares_dict[square_name]['color'] = "square " + determine_square_color(8 - row, current_col)
                    squares_dict[square_name]['occupied_by'] = False

                    current_col += 1

            else:
                square_name = chr(current_col + 96) + str(8 - row)
                squares_dict[square_name] = {}
                squares_dict[square_name]['name'] = square_name
                squares_dict[square_name]['color'] = "square " + determine_square_color(8 - row, current_col)
                squares_dict[square_name]['occupied_by'] = pieces_image_directories[char]
                current_col += 1

    return squares_dict
