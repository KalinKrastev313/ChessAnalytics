from django import forms
from ChessAnalytics.comments.models import FenComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = FenComment
        fields = ('content',)
