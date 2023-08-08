from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from ChessAnalytics.fenreader.forms import ChessAnalyticsAddForm, FenEditForm, EngineSettingsForm
from ChessAnalytics.fenreader.models import FenPosition
from ChessAnalytics.functions import Position, evaluate_position

from ChessAnalytics.comments.forms import CommentForm
from ChessAnalytics.comments.models import FenComment


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


# @login_required(login_url='login')
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


class FenDetailsView(LoginRequiredMixin, views.DetailView):
    model = FenPosition
    template_name = 'fenreader/position-details.html'
    context_object_name = 'position'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EngineSettingsForm()
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = EngineSettingsForm(request.POST)
        comment_form = CommentForm(request.POST)

        position_pk = request.POST.get('position_pk')
        user_pk = request.user.pk
        # user_pk = request.POST.get('user_pk')

        if form.is_valid():

            fen_instance = FenPosition.objects.get(pk=position_pk)
            fen = fen_instance.fen
            fen_instance.evaluation = evaluate_position(request, fen)
            fen_instance.save()
            return redirect('position details', pk=position_pk)
        elif comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.to_position_id = position_pk
            new_comment.to_user_id = user_pk
            new_comment.save()
            return redirect('position details', pk=position_pk)
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class CommentDeleteView(views.DeleteView):
    model = FenComment
    template_name = 'fenreader/comment-delete.html'
    context_object_name = 'position'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        fen_comment = self.get_object()
        fen_position_pk = fen_comment.to_position.pk
        return reverse_lazy('position details', kwargs={'pk': fen_position_pk})
