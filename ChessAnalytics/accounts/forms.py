from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from ChessAnalytics.accounts.models import ChessAnalyticsUser
from django import forms


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

