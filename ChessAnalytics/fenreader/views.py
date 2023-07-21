from django.shortcuts import render, redirect
from django.views import generic as views

from ChessAnalytics.fenreader.models import FenPosition
from ChessAnalytics.functions import convert_fen_to_square_dict, Position
from ChessAnalytics.fenreader.forms import ChessAnalyticsAddForm


def fen_reader(request):
    FEN = "r1bqkb1r/5p2/p1n4p/3pPp2/np1P4/1Pp1BN2/P1P1B2P/1NKRQ2R b kq - 1 17"
    position = Position(FEN)
    squares_dict = position.get_squares_dict()
    context = {
        "squares": squares_dict,
        'fen': FEN
    }
    return render(request, template_name='fen-reader.html', context=context)


def add_fen(request):
    form = ChessAnalyticsAddForm(request.POST or None)
    if form.is_valid():
        fen = form.save(commit=False)
        fen.user = request.user
        fen.save()
        redirect('all positions')

    context = {
        'form': form
    }
    return render(request, template_name='fenreader/add-fen.html', context=context)


class FenTilesView(views.ListView):
    model = FenPosition
    template_name = 'fenreader/all-positions.html'
    paginate_by = 8


class FenDetailsView(views.DetailView):
    model = FenPosition
    template_name = 'fenreader/position-details.html'
    context_object_name = 'position'
