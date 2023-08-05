from django.urls import path, include
from ChessAnalytics.fenreader import views


urlpatterns = [
    path('', views.fen_reader, name="fen reader"),
    path('add-fen/', views.add_fen, name='add fen'),
    path('positions-collection/', views.FenTilesView.as_view(), name='all positions'),
    path('puzzles-collection/', views.PuzzlesTilesView.as_view(), name='all puzzles'),
    path('position/<int:pk>', views.FenDetailsView.as_view(), name='position details'),
    path('evaluate-position', views.evaluate_position, name='position evaluate')

]
