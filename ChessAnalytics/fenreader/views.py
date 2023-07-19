from django.shortcuts import render, redirect
from django.views.generic import ListView

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


class FenTilesView(ListView):
    model = FenPosition
    template_name = 'fenreader/all-positions.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     counter = 1
    #     for data in FenPosition.objects.all():
    #         position = Position(data.fen)
    #         squares_dict = position.get_squares_dict()
    #         context[f'pos{counter}']['squares_dict'] = squares_dict
    #         counter += 1
    #     return context

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     for data in queryset:
    #         position = Position(data.fen)
    #         queryset[f'squares_dict{data.pk}'] = position.get_squares_dict()
    #
    #     return queryset




    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context = {}
    #     for fen_data in self.object_list:
    #         position = Position(fen_data.fen)
    #         position_identifier = fen_data.pk
    #         context[position_identifier] = position.get_squares_dict()
    #
    #     # context["now"] = timezone.now()
    #     return context
