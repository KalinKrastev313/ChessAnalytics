from django import forms
from ChessAnalytics.fenreader.models import FenPosition, PGN, CustomGame


class ChessAnalyticsFenAddForm(forms.ModelForm):
    class Meta():
        model = FenPosition
        fields = ('fen', 'white_player', 'white_rating', 'black_player', 'black_rating', 'tournament', 'is_a_puzzle')
        labels = {
            'fen': 'FEN',
            'is_a_puzzle': 'This position is a puzzle',
        }
        widgets = {
            'fen': forms.TextInput(),
            'white_player': forms.TextInput(),
            'black_player': forms.TextInput,
            'tournament': forms.TextInput,
            'is_a_puzzle': forms.CheckboxInput()
        }


class FenEditForm(forms.ModelForm):
    class Meta():
        model = FenPosition
        fields = ('white_player', 'white_rating', 'black_player', 'black_rating', 'tournament')
        exclude = ('fen', 'is_a_puzzle')
        labels = {
            'white_player': 'White Player',
            'white_rating': 'White Rating',
            'black_player': 'Black Player',
            'black_rating': 'Black Rating'
        }


class EngineSettingsForm(forms.Form):
    engine = forms.CharField(initial="Stockfish")
    depth = forms.IntegerField()
    lines = forms.IntegerField(initial=1)
    # memory = forms.IntegerField(initial=32)


class LiChessExporterForm(forms.Form):
    account = forms.CharField(initial="RankleMasterOfPranks")
    games_count = forms.IntegerField(initial=1)


class PGNCreateForm(forms.ModelForm):
    class Meta():
        model = PGN
        fields = ('pgn_moves', 'white_player', 'white_rating',
                  'black_player', 'black_rating', 'tournament',
                  'time_control', 'ECO')
        # widgets = {
        #     'pgn_moves': forms.Textarea(l),
        # }


class PGNEditForm(forms.ModelForm):
    class Meta():
        model = PGN
        fields = ('white_player', 'white_rating', 'black_player', 'black_rating', 'tournament', 'time_control', 'ECO')
        exclude = ('pgn_moves',)
        labels = {
            'white_player': 'White Player Name',
            'white_rating': 'White Rating',
            'black_player': 'Black Player',
            'black_rating': 'Black Rating',
            'tournament': 'Tournament',
            'time_control': 'Time Control',
            'ECO': 'Opening Code (ECO)',
        }


class PGNEngineSettingsForm(forms.Form):
    engine = forms.CharField(initial="Stockfish")
    depth = forms.IntegerField()


class BoardSetUpForm(forms.ModelForm):
    class Meta:
        model = CustomGame
        fields = ('from_position', )
