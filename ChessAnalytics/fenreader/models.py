from django.db import models
from ChessAnalytics.accounts.models import ChessAnalyticsUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator, MaxLengthValidator
from ChessAnalytics.functions import Position


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
    best_line = models.CharField(blank=True, null=True, validators=[MaxLengthValidator(300)])

    def evaluation(self):
        if self.best_line:
            return self.best_line.split("/")[0]
        else:
            return None

    # def squares_dict(self):
    #     position = Position(self.fen)
    #     squares_dict = position.get_squares_dict()
    #     return squares_dict

    def squares_data(self):
        position = Position(self.fen)
        squares_data = position.get_squares_data()
        return squares_data

    def is_white_to_move(self):
        position = Position(self.fen)
        return position.is_white_to_move()
