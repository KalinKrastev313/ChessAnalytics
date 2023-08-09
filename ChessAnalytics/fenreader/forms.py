from django import forms
from ChessAnalytics.fenreader.models import FenPosition


class ChessAnalyticsAddForm(forms.ModelForm):
    class Meta():
        model = FenPosition
        fields = ('fen', 'is_a_puzzle')
        labels = {
            'fen': 'FEN',
            'is_a_puzzle': 'This position is a puzzle',
        }
        widgets = {
            'fen': forms.TextInput(),
            'is_a_puzzle': forms.CheckboxInput()
        }


class FenEditForm(forms.ModelForm):
    class Meta():
        model = FenPosition
        fields = ('white_player', 'white_rating', 'black_player', 'black_rating', 'tournament')
        exclude = ('fen', 'is_a_puzzle')
        labels = {
            'white_player': 'White Player Name',
            'white_rating': 'White Rating',
            'black_player': 'Black Player Rating',
            'black_rating': 'Black Rating'
        }


class EngineSettingsForm(forms.Form):
    engine = forms.CharField(initial="Stockfish")
    depth = forms.IntegerField()
    lines = forms.IntegerField(initial=1)
    # memory = forms.IntegerField(initial=32)
