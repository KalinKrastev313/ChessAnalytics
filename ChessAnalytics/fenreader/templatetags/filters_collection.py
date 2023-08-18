from django import template

register = template.Library()


@register.filter
def to_move_number(value, is_white_to_move):
    if is_white_to_move is True:
        if value % 2 == 0 or value == 0:
            return ""
        else:
            return f'{(value // 2) + 1}. '
    else:
        if value == 1:
            return "1 ... "
        elif value % 2 == 0:
            return f'  {value // 2 + 1}. '
        else:
            return ''


@register.filter
def mate_format(value):
    return f"Mate in {int(value)} |"


@register.filter
def centipawns_to_float(value):
    return f"{(value / 100):.2f}"

