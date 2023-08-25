from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect

from ChessAnalytics.accounts.models import ChessAnalyticsUser
from ChessAnalytics.accounts.forms import ChessAnalyticsUserCreateForm, LoginForm, ChessAnalyticsUserEditForm, ChessAnalyticsUserPreferencesForm
from django import forms


class UserRegisterView(views.CreateView):
    model = ChessAnalyticsUser
    form_class = ChessAnalyticsUserCreateForm
    template_name = 'accounts/register-user.html'
    success_url = reverse_lazy('login')


class UserLoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login-page.html'
    next_page = reverse_lazy('home')


class UserLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('home')


class UserEditView(views.UpdateView):
    model = ChessAnalyticsUser
    form_class = ChessAnalyticsUserEditForm
    template_name = 'accounts/profile-edit.html'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.pk})


class UserDetailView(views.DetailView):
    model = ChessAnalyticsUser
    template_name = 'accounts/profile-details.html'
    context_object_name = 'profile_details'


def no_permission_view(request):
    return render(request, template_name='accounts/no-permission.html')


class UserPreferences(UserEditView):
    form_class = ChessAnalyticsUserPreferencesForm
    template_name = 'accounts/profile-preferences.html'
