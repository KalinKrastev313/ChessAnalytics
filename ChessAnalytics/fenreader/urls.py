from django.urls import path, include
from ChessAnalytics.fenreader import views


urlpatterns = [
    path('', views.fen_reader, name="fen reader"),
    path('add-fen/', views.add_fen, name='add fen'),
    path('positions-collection/', views.FenTilesView.as_view(), name='all positions'),
    path('position/<int:pk>', views.FenDetailsView.as_view(), name='position details')

]
