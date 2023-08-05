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


class EngineSettingsForm(forms.Form):
    engine = forms.CharField(initial="Stockfish")
    depth = forms.IntegerField()
    # memory = forms.IntegerField(initial=32)
