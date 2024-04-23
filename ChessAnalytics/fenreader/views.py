import json
from django.http import HttpResponse
import matplotlib

import io
import urllib, base64
import matplotlib.pyplot as plt

import chess.pgn
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.http import JsonResponse

from ChessAnalytics.fenreader.forms import ChessAnalyticsFenAddForm, FenEditForm, EngineSettingsForm, PGNCreateForm, PGNEditForm, PGNEngineSettingsForm, BoardSetUpForm
from ChessAnalytics.fenreader.models import FenPosition, EngineLine, PGN, CustomGame
from ChessAnalytics.functions import Position, evaluate_position, \
    get_squares_data_for_a_move_from_line, encode_plot, get_moves_evaluations, \
    UCIValidator
from ChessAnalytics.common_utils import get_fen_from_pgn_at_move_n, create_a_square_from_str, save_a_comment_from_form
from ChessAnalytics.accounts.admin import is_student, is_teacher_or_admin

from ChessAnalytics.comments.forms import CommentForm
from ChessAnalytics.comments.models import FenComment

matplotlib.use('Agg')


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_teacher_or_admin(self.request.user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('no permission')
        return super().handle_no_permission()

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return super().get_login_url()
        else:
            return '/accounts/usertype/'


# def fen_reader(request):
#     FEN = "r1bqkb1r/5p2/p1n4p/3pPp2/np1P4/1Pp1BN2/P1P1B2P/1NKRQ2R b kq - 1 17"
#     position = Position(FEN)
#     squares_data = position.get_squares_data()
#     if request.method == 'GET':
#         context = {
#             "squares_data": squares_data,
#             'fen': FEN,
#             'last_move': 'no'
#         }
#         return render(request, template_name='fen-reader.html', context=context)
#     elif request.method == 'POST':
#         data = json.loads(request.body)
#         comes_from = data.get('comes_from')
#         goes_to = data.get('goes_to')
#         move_uci = comes_from + goes_to
#         print(move_uci)
#         context = {
#             "squares_data": squares_data,
#             'fen': FEN,
#             'last_move': move_uci
#         }
#         board = chess.Board(fen=FEN)
#         move = chess.Move.from_uci(comes_from + goes_to)
#         if board.is_legal(move):
#             board.push(move)
#             is_legal = True
#         else:
#             is_legal = False
#         FEN = board.fen()
#
#         data = {
#             'is_legal': is_legal,
#             'is_promotion': False,
#         }
#
#         json_data = json.dumps(data)
#
#         return JsonResponse(json_data, safe=False)

def load_form_page_or_save_filled_form(form, request, redirect_page_name, template_name):
    if form.is_valid():
        fen = form.save(commit=False)
        fen.user = request.user
        fen.save()
        return redirect(redirect_page_name)

    context = {
        'form': form
    }
    return render(request, template_name=template_name, context=context)


def add_fen(request):
    form = ChessAnalyticsFenAddForm(request.POST or None)
    return load_form_page_or_save_filled_form(form, request, 'all positions', 'fenreader/fen-add.html')


class FenEditView(LoginRequiredMixin, TeacherRequiredMixin, views.UpdateView):
    model = FenPosition
    form_class = FenEditForm
    template_name = 'fenreader/fen-edit.html'
    context_object_name = 'position'

    def get_success_url(self):
        return reverse_lazy('position details', kwargs={'pk': self.object.pk})


class FenDeleteView(LoginRequiredMixin, TeacherRequiredMixin, views.DeleteView):
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


class FenDetailsView(LoginRequiredMixin, views.DetailView):
    model = FenPosition
    template_name = 'fenreader/position-details.html'
    context_object_name = 'position'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        engine_lines = EngineLine.objects.filter(to_position=pk)
        context['engine_lines'] = engine_lines
        context['form'] = EngineSettingsForm()
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        engine_form = EngineSettingsForm(request.POST)
        comment_form = CommentForm(request.POST)

        position_pk = request.POST.get('position_pk')
        user_pk = request.user.pk

        if engine_form.is_valid():
            fen_instance = FenPosition.objects.get(pk=position_pk)
            fen = fen_instance.fen
            best_lines = evaluate_position(request, fen)
            old_lines = EngineLine.objects.filter(to_position=position_pk)
            old_lines.delete()
            rank = 1
            for line in best_lines:
                line_instance = EngineLine(to_position=fen_instance, evaluation=line['eval'],
                                           line=line['line_moves'], rank=rank, is_mate=line['is_mate'])
                line_instance.save()
                rank += 1
            return redirect('position details', pk=position_pk)
        elif comment_form.is_valid():
            save_a_comment_from_form(comment_form, position_pk, user_pk)
            return redirect('position details', pk=position_pk)
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = engine_form
            return self.render_to_response(context)


class PositionLineView(FenDetailsView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        line_rank = self.kwargs.get('line_rank')
        halfmove = self.kwargs.get('halfmove')

        fen_instance = FenPosition.objects.get(pk=pk)
        fen = fen_instance.fen
        line = EngineLine.objects.filter(to_position=pk, rank=line_rank).first().line

        context['squares_data'] = get_squares_data_for_a_move_from_line(fen, line, halfmove)
        return context


class CommentDeleteView(LoginRequiredMixin, TeacherRequiredMixin, views.DeleteView):
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


def add_pgn(request):
    form = PGNCreateForm(request.POST or None)
    return load_form_page_or_save_filled_form(form, request, 'all games', 'fenreader/pgn-add.html')


class PGNTilesView(views.ListView):
    model = PGN
    template_name = 'fenreader/all-games.html'
    paginate_by = 8
    ordering = ['pk']


class PGNDetailsView(views.DetailView):
    model = PGN
    template_name = 'fenreader/game-details.html'
    context_object_name = 'pgn'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        position = Position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        context['form'] = PGNEngineSettingsForm()
        context['squares_data'] = position.get_squares_data()

        moves_evaluations = PGN.objects.get(pk=pk).moves_evaluations
        context['plot_data'] = encode_plot(moves_evaluations) if moves_evaluations else None
        return context

    def post(self, request, *args, **kwargs):
        engine_form = PGNEngineSettingsForm(request.POST)

        pgn_pk = request.POST.get('pgn_pk')

        if engine_form.is_valid():
            pgn_instance = PGN.objects.get(pk=pgn_pk)
            moves_notation = pgn_instance.pgn_moves

            pgn_instance.moves_evaluations = get_moves_evaluations(request, moves_notation)
            pgn_instance.save()

            return redirect('game details', pk=pgn_pk)


class PGNOnMoveDetailsView(PGNDetailsView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        halfmove = self.kwargs.get('halfmove')
        pgn_moves = PGN.objects.get(pk=pk).pgn_moves
        fen = get_fen_from_pgn_at_move_n(pgn_moves, halfmove)
        position = Position(fen)
        context['squares_data'] = position.get_squares_data()

        return context


class PGNInfoEditView(LoginRequiredMixin, TeacherRequiredMixin, views.UpdateView):
    model = PGN
    form_class = PGNEditForm
    template_name = 'fenreader/game-edit.html'
    context_object_name = 'pgn'

    def get_success_url(self):
        return reverse_lazy('game details', kwargs={'pk': self.object.pk})


class PGNDeleteView(LoginRequiredMixin, TeacherRequiredMixin, views.DeleteView):
    model = PGN
    template_name = 'fenreader/game-delete.html'
    success_url = reverse_lazy('all games')
    context_object_name = 'pgn'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


def AnalysisBoardSetUp(request):
    if request.method == 'GET':
        form = BoardSetUpForm
        context = {
            'form': form
        }
        return render(request, template_name='fenreader/board_set_up.html', context=context)
    elif request.method == 'POST':
        set_up_form = BoardSetUpForm(request.POST)
        initial_position = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

        if set_up_form.is_valid():
            if set_up_form.cleaned_data['from_position']:
                initial_position = set_up_form.cleaned_data['from_position']
            custom_game = set_up_form.save(commit=False)
            custom_game.user = request.user
            custom_game.from_position = initial_position
            custom_game.save()
            return redirect('board analyse', pk=custom_game.id)


class AnalysisBoard(views.TemplateView):
    template_name = 'fenreader/analysis-board.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        custom_game_pk = context['pk']
        fen = CustomGame.objects.get(id=custom_game_pk).get_fen_at_halfmove(halfmove=-1)

        position = Position(fen)
        context['squares_data'] = position.get_squares_data()
        return context

    def post(self, request, *args, **kwargs):
        game_pk = kwargs.get('pk')
        game_instance = CustomGame.objects.get(id=game_pk)
        FEN = game_instance.get_fen_at_halfmove(halfmove=-1)
        moves_uci = game_instance.moves_uci
        position = Position(FEN)
        squares_data = position.get_squares_data()
        data = json.loads(request.body)

        comes_from = data.get('comes_from')
        goes_to = data.get('goes_to')
        promotes_to = data.get('promotes_to')

        move_validator = UCIValidator(fen=FEN, comes_from=comes_from, goes_to=goes_to, promotes_to=promotes_to)

        # KK: for castling - it doesn't move the rooks yet

        data = move_validator.validate_move()

        json_data = json.dumps(data)

        print(moves_uci)
        if data['is_legal']:
            if not moves_uci is None:
                moves_uci += f',{comes_from}{goes_to}'
            else:
                moves_uci = comes_from + goes_to
            if data['is_promotion']:
                moves_uci += promotes_to.lower()
            game_instance.moves_uci = moves_uci
            game_instance.save()

        return JsonResponse(json_data, safe=False)


