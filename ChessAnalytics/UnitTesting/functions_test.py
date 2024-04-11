from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

import chess.engine

from ChessAnalytics.functions import Position, PositionEvaluator


class PositionTest(TestCase):
    def setUp(self) -> None:
        fen = 'rnbqkb1r/pp2pppp/2p2n2/3P4/2P5/8/PP1P1PPP/RNBQKBNR w KQkq - 0 4'
        self.position = Position(fen)
        self.expected_squares_dict = [{'name': 'a8', 'color': 'square white', 'occupied_by': 'rook-black.png'},
                                      {'name': 'b8', 'color': 'square black', 'occupied_by': 'knight-black.png'},
                                      {'name': 'c8', 'color': 'square white', 'occupied_by': 'bishop-black.png'},
                                      {'name': 'd8', 'color': 'square black', 'occupied_by': 'queen-black.png'},
                                      {'name': 'e8', 'color': 'square white', 'occupied_by': 'king-black.png'},
                                      {'name': 'f8', 'color': 'square black', 'occupied_by': 'bishop-black.png'},
                                      {'name': 'g8', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'h8', 'color': 'square black', 'occupied_by': 'rook-black.png'},
                                      {'name': 'a7', 'color': 'square black', 'occupied_by': 'pawn-black.png'},
                                      {'name': 'b7', 'color': 'square white', 'occupied_by': 'pawn-black.png'},
                                      {'name': 'c7', 'color': 'square black', 'occupied_by': False},
                                      {'name': 'd7', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'e7', 'color': 'square black', 'occupied_by': 'pawn-black.png'},
                                      {'name': 'f7', 'color': 'square white', 'occupied_by': 'pawn-black.png'},
                                      {'name': 'g7', 'color': 'square black', 'occupied_by': 'pawn-black.png'},
                                      {'name': 'h7', 'color': 'square white', 'occupied_by': 'pawn-black.png'},
                                      {'name': 'a6', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'b6', 'color': 'square black', 'occupied_by': False},
                                      {'name': 'c6', 'color': 'square white', 'occupied_by': 'pawn-black.png'},
                                      {'name': 'd6', 'color': 'square black', 'occupied_by': False},
                                      {'name': 'e6', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'f6', 'color': 'square black', 'occupied_by': 'knight-black.png'},
                                      {'name': 'g6', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'h6', 'color': 'square black', 'occupied_by': False},
                                      {'name': 'a5', 'color': 'square black', 'occupied_by': False},
                                      {'name': 'b5', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'c5', 'color': 'square black', 'occupied_by': False},
                                      {'name': 'd5', 'color': 'square white', 'occupied_by': 'pawn-white.png'},
                                      {'name': 'e5', 'color': 'square black', 'occupied_by': False},
                                      {'name': 'f5', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'g5', 'color': 'square black', 'occupied_by': False},
                                      {'name': 'h5', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'a4', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'b4', 'color': 'square black', 'occupied_by': False},
                                      {'name': 'c4', 'color': 'square white', 'occupied_by': 'pawn-white.png'},
                                      {'name': 'd4', 'color': 'square black', 'occupied_by': False},
                                      {'name': 'e4', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'f4', 'color': 'square black', 'occupied_by': False},
                                      {'name': 'g4', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'h4', 'color': 'square black', 'occupied_by': False},
                                      {'name': 'a3', 'color': 'square black', 'occupied_by': False},
                                      {'name': 'b3', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'c3', 'color': 'square black', 'occupied_by': False},
                                      {'name': 'd3', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'e3', 'color': 'square black', 'occupied_by': False},
                                      {'name': 'f3', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'g3', 'color': 'square black', 'occupied_by': False},
                                      {'name': 'h3', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'a2', 'color': 'square white', 'occupied_by': 'pawn-white.png'},
                                      {'name': 'b2', 'color': 'square black', 'occupied_by': 'pawn-white.png'},
                                      {'name': 'c2', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'd2', 'color': 'square black', 'occupied_by': 'pawn-white.png'},
                                      {'name': 'e2', 'color': 'square white', 'occupied_by': False},
                                      {'name': 'f2', 'color': 'square black', 'occupied_by': 'pawn-white.png'},
                                      {'name': 'g2', 'color': 'square white', 'occupied_by': 'pawn-white.png'},
                                      {'name': 'h2', 'color': 'square black', 'occupied_by': 'pawn-white.png'},
                                      {'name': 'a1', 'color': 'square black', 'occupied_by': 'rook-white.png'},
                                      {'name': 'b1', 'color': 'square white', 'occupied_by': 'knight-white.png'},
                                      {'name': 'c1', 'color': 'square black', 'occupied_by': 'bishop-white.png'},
                                      {'name': 'd1', 'color': 'square white', 'occupied_by': 'queen-white.png'},
                                      {'name': 'e1', 'color': 'square black', 'occupied_by': 'king-white.png'},
                                      {'name': 'f1', 'color': 'square white', 'occupied_by': 'bishop-white.png'},
                                      {'name': 'g1', 'color': 'square black', 'occupied_by': 'knight-white.png'},
                                      {'name': 'h1', 'color': 'square white', 'occupied_by': 'rook-white.png'}]

    def test_get_squares_description_from_fen(self):
        actual = self.position.get_squares_description_from_fen()
        expected = 'rnbqkb1r/pp2pppp/2p2n2/3P4/2P5/8/PP1P1PPP/RNBQKBNR'
        self.assertEquals(actual, expected)

    def test_get_rows(self):
        actual = self.position.get_rows()
        expected = ['rnbqkb1r', 'pp2pppp', '2p2n2', '3P4', '2P5', '8', 'PP1P1PPP', 'RNBQKBNR']
        self.assertEquals(actual, expected)

    def test_get_square_name(self):
        actual = self.position.get_square_name(1, 3)
        expected = 'c7'
        self.assertEquals(actual, expected)

    def test_determine_square_color_when_square_white(self):
        actual = self.position.determine_square_color(5, 6)
        self.assertEquals(actual, 'white')
        self.assertEquals(self.position.get_square_name(5, 6), 'f3')
        actual = self.position.determine_square_color(6, 7)
        self.assertEquals(actual, 'white')

    def test_determine_square_color_when_square_black(self):
        actual = self.position.determine_square_color(6, 6)
        self.assertEquals(actual, 'black')
        actual = self.position.determine_square_color(5, 7)
        self.assertEquals(actual, 'black')

    def test_is_white_to_move_when_white_to_move(self):
        actual = self.position.is_white_to_move()
        self.assertEquals(actual, True)

    def test_is_white_to_move_when_black_to_move(self):
        actual = Position(fen='rnbqkb1r/pp2pppp/2P2n2/8/2P5/8/PP1P1PPP/RNBQKBNR b KQkq - 0 4').is_white_to_move()
        self.assertEquals(actual, False)

    def test_add_square_to_squares_data_when_unoccupied(self):
        self.position.add_square_to_squares_data(row=5, col=6)
        actual = self.position.squares_data
        expected = [{
            'name': 'f3',
            'color': 'square white',
            'occupied_by': False
        }]
        self.assertEquals(actual, expected)

    def test_add_square_to_squares_data_when_occupied_by_black_knight(self):
        self.position.add_square_to_squares_data(row=5, col=6, occupied_by='black_knight')
        actual = self.position.squares_data
        expected = [{
            'name': 'f3',
            'color': 'square white',
            'occupied_by': 'black_knight'
        }]
        self.assertEquals(actual, expected)

    def test_fil_squares_dict_with_rows_info(self):
        self.position.fill_squares_dict_with_rows_info(self.position.get_rows())
        self.assertEquals(self.position.squares_data, self.expected_squares_dict)

    def test_get_squares_data(self):
        actual = self.position.get_squares_data()
        self.assertEquals(actual, self.expected_squares_dict)


class PositionEvaluatorTest(TestCase):
    def setUp(self) -> None:
        self.fen = 'r1bqk1nr/pppp1ppp/2n5/b7/2BpP3/2P2N2/P4PPP/RNBQ1RK1 b kq - 1 7'
        self.depth = 10
        self.requested_lines = 1
        self.evaluator = PositionEvaluator(self.fen, self.depth, self.requested_lines)

    def test_render_engine(self):
        actual_engine = self.evaluator.render_engine()
        self.assertEquals(type(actual_engine), chess.engine.SimpleEngine)
        actual_engine.close()

    def test_get_engine_evaluation_when_not_mate(self):
        test_score = chess.engine.PovScore(chess.engine.Cp(80), True)
        test_line_info = [{'pv': [chess.Move.from_uci('e2e4'), chess.Move.from_uci('e7e5')], 'score': test_score}]
        expected_lines = [{'eval': 80, 'line_moves': 'e2e4,e7e5', 'is_mate': False}]
        self._test_run_get_engine_evaluation_and_assert(test_line_info, expected_lines)

    def test_get_engine_evaluation_when_is_mate(self):
        test_score = chess.engine.PovScore(chess.engine.Mate(2), True)
        test_line_info = [{'pv': [chess.Move.from_uci('e2e4'), chess.Move.from_uci('e7e5')], 'score': test_score}]
        expected_lines = [{'eval': 2, 'line_moves': 'e2e4,e7e5', 'is_mate': True}]
        self._test_run_get_engine_evaluation_and_assert(test_line_info, expected_lines)

    def test_get_engine_evaluation_when_is_mate_given(self):
        test_score = chess.engine.PovScore(chess.engine.MateGiven, True)
        test_line_info = [{'pv': [chess.Move.from_uci('e2e4'), chess.Move.from_uci('e7e5')], 'score': test_score}]
        expected_lines = [{'eval': 0, 'line_moves': 'e2e4,e7e5', 'is_mate': True}]
        self._test_run_get_engine_evaluation_and_assert(test_line_info, expected_lines)

    def _test_run_get_engine_evaluation_and_assert(self, test_line_info, expected_lines):
        with patch.object(chess.engine.SimpleEngine, 'analyse', return_value=test_line_info) as r:
            actual_lines = self.evaluator.get_engine_evaluation()

        self.evaluator.close_engine()
        self.assertEquals(actual_lines, expected_lines)

    def test_extract_lines_from_engine_info(self):
        self.evaluator.info = [{'pv': [chess.Move.from_uci('e2e4'), chess.Move.from_uci('e7e5')],
                                'score': chess.engine.PovScore(chess.engine.Cp(80), True)},
                               {'pv': [chess.Move.from_uci('d2d4'), chess.Move.from_uci('d7d5')],
                                'score': chess.engine.Mate(5)}]
        actual_best_lines = self.evaluator.extract_lines_from_engine_info()
        expected_best_lines = [{'eval': 80,
                                'line_moves': 'e2e4,e7e5',
                                'is_mate': False},
                               {'eval': 5,
                                'line_moves': 'd2d4,d7d5',
                                'is_mate': True}
                               ]
        self.assertEquals(actual_best_lines, expected_best_lines)

    def test_turn_move_objects_to_string(self):
        move_objects = [chess.Move.from_uci('e2e4'), chess.Move.from_uci('e7e5')]
        actual_move_string = self.evaluator.turn_move_objects_to_string(move_objects)
        self.assertEquals(actual_move_string, 'e2e4,e7e5')
