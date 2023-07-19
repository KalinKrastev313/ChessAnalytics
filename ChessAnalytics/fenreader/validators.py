from django.core.exceptions import ValidationError

fen_regex = "[\d/pnbrqkPNBRQK]+ [wb] [QKqk\-]{1,4} [\-abcdefgh12345678]{1,2} [\d]{1,2} [\d]{1,2}"


def validate_fen(value):
    value = str(value)
    if not value.split() == 6:
        raise ValidationError("This is not a full FEN")
    if not value.split()[0].split("/") == 8:
        raise ValidationError("This is not a full FEN")

