from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from ChessAnalytics.fenreader.forms import ChessAnalyticsFenAddForm, FenEditForm, EngineSettingsForm
from ChessAnalytics.fenreader.models import FenPosition
from ChessAnalytics.functions import Position, evaluate_position, get_squares_data_for_a_move_from_line
from ChessAnalytics.accounts.admin import is_student, is_teacher

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
    form = ChessAnalyticsFenAddForm(request.POST or None)
    if form.is_valid():
        fen = form.save(commit=False)
        fen.user = request.user
        fen.save()
        return redirect('all positions')

    context = {
        'form': form
    }
    return render(request, template_name='fenreader/fen-add.html', context=context)


# @user_passes_test(is_teacher)
class FenEditView(LoginRequiredMixin, UserPassesTestMixin, views.UpdateView):
    model = FenPosition
    form_class = FenEditForm
    template_name = 'fenreader/fen-edit.html'
    context_object_name = 'position'

    # @user_passes_test(is_teacher, login_url='login')
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return is_teacher(self.request.user)

    def get_login_url(self):
        if not self.request.user.is_authenticated():
            return super(FenEditView, self).get_login_url()
        else:
            return '/accounts/usertype/'

    def get_success_url(self):
        return reverse_lazy('position details', kwargs={'pk': self.object.pk})


# @user_passes_test(is_teacher)
class FenDeleteView(LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    model = FenPosition
    template_name = 'fenreader/fen-delete.html'
    success_url = reverse_lazy('all positions')
    context_object_name = 'position'

    def test_func(self):
        return is_teacher(self.request.user)

    def get_login_url(self):
        if not self.request.user.is_authenticated():
            return super(FenDeleteView, self).get_login_url()
        else:
            return '/accounts/usertype/'

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
        engine_form = EngineSettingsForm(request.POST)
        comment_form = CommentForm(request.POST)

        position_pk = request.POST.get('position_pk')
        user_pk = request.user.pk
        # user_pk = request.POST.get('user_pk')

        if engine_form.is_valid():
            fen_instance = FenPosition.objects.get(pk=position_pk)
            fen = fen_instance.fen
            fen_instance.best_lines = evaluate_position(request, fen)
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
            context['form'] = engine_form
            return self.render_to_response(context)


class PositionLineView(FenDetailsView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        # We subtract one from the line index, so that user can see in the link lines ranks starting from 1, but we work with indexes starting from 0
        line_index = self.kwargs.get('line') - 1
        halfmove = self.kwargs.get('halfmove')
        fen_instance = FenPosition.objects.get(pk=pk)
        fen = fen_instance.fen
        lines = fen_instance.best_lines

        squares_data = get_squares_data_for_a_move_from_line(fen, lines, line_index, halfmove)
        context['squares_data'] = squares_data
        return context


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



