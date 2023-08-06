
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views import generic as views

from ChessAnalytics.fenreader.models import FenPosition
from ChessAnalytics.functions import Position, evaluate_position
from ChessAnalytics.fenreader.forms import ChessAnalyticsAddForm, FenEditForm, EngineSettingsForm


def fen_reader(request):
    FEN = "r1bqkb1r/5p2/p1n4p/3pPp2/np1P4/1Pp1BN2/P1P1B2P/1NKRQ2R b kq - 1 17"
    position = Position(FEN)
    squares_data = position.get_squares_data()
    context = {
        "squares_data": squares_data,
        'fen': FEN
    }
    return render(request, template_name='fen-reader.html', context=context)


def add_fen(request):
    form = ChessAnalyticsAddForm(request.POST or None)
    if form.is_valid():
        fen = form.save(commit=False)
        fen.user = request.user
        fen.save()
        return redirect('all positions')

    context = {
        'form': form
    }
    return render(request, template_name='fenreader/fen-add.html', context=context)


class FenEditView(views.UpdateView):
    model = FenPosition
    form_class = FenEditForm
    template_name = 'fenreader/fen-edit.html'
    context_object_name = 'position'

    def get_success_url(self):
        return reverse_lazy('position details', kwargs={'pk': self.object.pk})


class FenDeleteView(views.DeleteView):
    model = FenPosition
    template_name = 'fenreader/fen-delete.html'
    success_url = reverse_lazy('all positions')
    context_object_name = 'position'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class FenTilesView(views.ListView):
    model = FenPosition
    template_name = 'fenreader/all-positions.html'
    paginate_by = 8
    ordering = ['pk']


class PuzzlesTilesView(FenTilesView):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_a_puzzle=True)

        return queryset


class FenDetailsView(views.DetailView):
    model = FenPosition
    template_name = 'fenreader/position-details.html'
    context_object_name = 'position'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EngineSettingsForm()

        return context

    def post(self, request, *args, **kwargs):
        form = EngineSettingsForm(request.POST)

        if form.is_valid():
            pk = request.POST.get('pk')
            fen_instance = FenPosition.objects.get(pk=pk)
            fen = fen_instance.fen
            fen_instance.evaluation = evaluate_position(request, fen)
            fen_instance.save()
            return redirect('position details', pk=pk)
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


