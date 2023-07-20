from django.db import models
from ChessAnalytics.accounts.models import ChessAnalyticsUser
from django.core.validators import RegexValidator
from ChessAnalytics.functions import Position


fen_regex = "[\d/pnbrqkPNBRQK]+ [wb] [QKqk\-]{1,4} [\-a-h1-8]{1,2} [\d]{1,2} [\d]{1,2}"


class FenPosition(models.Model):
    user = models.ForeignKey(to=ChessAnalyticsUser, on_delete=models.CASCADE)
    fen = models.CharField(
        blank=False,
        validators=[RegexValidator(fen_regex)])
    evaluation = models.FloatField(blank=True, null=True)
    is_a_puzzle = models.BooleanField(blank=True, null=True)

    def squares_dict(self):
        position = Position(self.fen)
        squares_dict = position.get_squares_dict()
        return squares_dict

    def is_white_to_move(self):
        position = Position(self.fen)
        return position.is_white_to_move()
