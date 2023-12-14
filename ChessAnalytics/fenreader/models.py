from django.db import models
from ChessAnalytics.accounts.models import ChessAnalyticsUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator, MaxLengthValidator
from ChessAnalytics.functions import Position, coordinate_to_algebraic_notation, get_fen_from_pgn_at_move_n, \
    turn_line_to_moves_info, get_fen_at_halfmove_from_uci_moves_lst

import chess

fen_regex = "[\d/pnbrqkPNBRQK]+ [wb] [QKqk\-]{1,4} [\-a-h1-8]{1,2} [\d]{1,2} [\d]{1,2}"


class FenPosition(models.Model):
    user = models.ForeignKey(to=ChessAnalyticsUser, on_delete=models.CASCADE)
    fen = models.CharField(
        blank=False,
        validators=[RegexValidator(fen_regex)])
    # evaluation = models.FloatField(blank=True, null=True)
    white_player = models.CharField(blank=True, null=True)
    white_rating = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(800), MaxValueValidator(4000)])
    black_player = models.CharField(blank=True, null=True)
    black_rating = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(800), MaxValueValidator(4000)])
    tournament = models.CharField(blank=True, null=True)
    is_a_puzzle = models.BooleanField(blank=True, null=True)

    def squares_data(self):
        position = Position(self.fen)
        squares_data = position.get_squares_data()
        return squares_data

    def is_white_to_move(self):
        position = Position(self.fen)
        return position.is_white_to_move()


class EngineLine(models.Model):
    to_position = models.ForeignKey(to=FenPosition, on_delete=models.CASCADE)
    evaluation = models.IntegerField(blank=False, null=False)
    line = models.CharField(blank=False, null=False)
    is_mate = models.BooleanField(blank=True, default=False)
    rank = models.PositiveIntegerField(default=1)

    def line_moves(self):
        fen = FenPosition.objects.get(pk=self.to_position_id).fen
        line = self.line

        moves = turn_line_to_moves_info(fen=fen, line=line)

        return moves

    # def rank(self):
    #     all_lines_for_current_position = EngineLine.objects.filter(to_position=self.to_position)
    #     counter = 1
    #     for line in all_lines_for_current_position:
    #         if line.pk == self.pk:
    #             return counter
    #         counter += 1


class PGN(models.Model):
    user = models.ForeignKey(to=ChessAnalyticsUser, on_delete=models.CASCADE)
    pgn_moves = models.CharField(blank=False, )
    white_player = models.CharField(blank=True, null=True)
    white_rating = models.IntegerField(blank=True, null=True,
                                       validators=[MinValueValidator(800), MaxValueValidator(4000)])
    black_player = models.CharField(blank=True, null=True)
    black_rating = models.IntegerField(blank=True, null=True,
                                       validators=[MinValueValidator(800), MaxValueValidator(4000)])
    tournament = models.CharField(blank=True, null=True)
    time_control = models.CharField(blank=True, null=True)
    ECO = models.CharField(blank=True, null=True)
    moves_evaluations = models.TextField(blank=True, null=True)

    def squares_data(self):
        fen = get_fen_from_pgn_at_move_n(self.pgn_moves, 10)
        position = Position(fen)
        squares_data = position.get_squares_data()
        return squares_data

    def get_moves_info(self):
        lst = self.pgn_moves.split()
        result = []
        halfmove = 1
        for i in range(0, len(lst), 3):
            try:
                if lst[i+1]:
                    result.append({'notation': f'{lst[i]} {lst[i+1]}',
                                   'halfmove': halfmove})

                if lst[i+2]:
                    result.append({'notation': f'{lst[i+2]}',
                                   'halfmove': halfmove + 1})

            except:
                pass

            halfmove += 2

        return result


class CustomGame(models.Model):
    user = models.ForeignKey(to=ChessAnalyticsUser, on_delete=models.CASCADE)
    from_position = models.CharField(
        blank=True,
        null=True,
        validators=[RegexValidator(fen_regex)])
    moves_uci = models.CharField(blank=True, null=True)

    def get_fen_at_halfmove(self, halfmove=-1):
        moves_uci_lst = self.moves_uci.split(',') if self.moves_uci else []
        fen = get_fen_at_halfmove_from_uci_moves_lst(initial_fen=self.from_position,
                                                     moves_uci_lst=moves_uci_lst,
                                                     halfmove=halfmove)
        return fen
