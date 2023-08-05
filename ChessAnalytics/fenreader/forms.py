from django import forms
from ChessAnalytics.fenreader.models import FenPosition

STOCKFISH_DIRECTORY = "asdsasd"
ENGINE_CHOICES = {
    'Stockfish': STOCKFISH_DIRECTORY
}


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


class EngineSettingsForm(forms.Form):
    # engine = forms.ChoiceField(choices=ENGINE_CHOICES)
    depth = forms.IntegerField()
    # memory = forms.IntegerField(initial=32)
