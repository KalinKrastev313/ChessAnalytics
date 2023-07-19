from django.urls import path, include
from ChessAnalytics.common import views


urlpatterns = [
    path('', views.HomePageView, name='home'),

]