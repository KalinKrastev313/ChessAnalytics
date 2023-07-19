from django.urls import path, include
from ChessAnalytics.accounts import views


urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', views.UserDetailView.as_view(), name='profile details'),
    path('profile/edit/<int:pk>/', views.UserEditView.as_view(), name='profile edit'),
]