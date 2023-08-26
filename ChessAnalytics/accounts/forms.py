from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from ChessAnalytics.accounts.models import ChessAnalyticsUser
from django import forms

from ChessAnalytics.functions import get_folder_names


class ChessAnalyticsUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ChessAnalyticsUser
        fields = ('username', 'email')


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'placeholder': 'Username'
    }))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'placeholder': 'Password',
        })
    )


class ChessAnalyticsUserEditForm(forms.ModelForm):
    class Meta():
        model = ChessAnalyticsUser
        fields = ('username', 'first_name', 'last_name', 'email', 'rating', 'date_of_birth', 'gender')
        exclude = ('password',)
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'rating': 'FIDE Rating',
            'date_of_birth': 'Date of Birth',
            'gender': 'Gender'
        }
        widgets = {
            'date_of_birth': forms.SelectDateWidget(years=range(1900, 2023)),
        }


class ChessAnalyticsUserPreferencesForm(forms.ModelForm):
    PIECE_SETS_CHOICES = []
    for piece_set in get_folder_names('static/pieces/'):
        PIECE_SETS_CHOICES.append((piece_set, piece_set))

    piece_preference = forms.ChoiceField(choices=PIECE_SETS_CHOICES, widget=forms.Select)

    class Meta():
        model = ChessAnalyticsUser
        fields = ('piece_preference',)
