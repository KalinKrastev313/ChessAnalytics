from django.contrib.auth.decorators import login_required, permission_required

from django.urls import path, include
from ChessAnalytics.fenreader import views


urlpatterns = [
    path('', views.fen_reader, name="fen reader"),
    path('add-fen/', views.add_fen, name='add fen'),
    path('positions-collection/', login_required(views.FenTilesView.as_view()), name='all positions'),
    path('puzzles-collection/', login_required(views.PuzzlesTilesView.as_view()), name='all puzzles'),
    path('position/<int:pk>/', views.FenDetailsView.as_view(), name='position details'),
    path('position/edit/<int:pk>/', views.FenEditView.as_view(), name='position edit'),
    path('position/delete/<int:pk>/', views.FenDeleteView.as_view(), name='position delete'),
    path('position/<int:pk>/line/<int:line_rank>/halfmove/<int:halfmove>/', views.PositionLineView.as_view(), name="position line"),
    path('position/comment/delete/<int:pk>/',
         views.CommentDeleteView.as_view(), name='comment delete'),
    path('evaluate-position/', views.evaluate_position, name='position evaluate'),
    path('add-pgn/', views.add_pgn, name='add pgn'),
    path('games-collection/', login_required(views.PGNTilesView.as_view()), name='all games'),
    path('game/<int:pk>/', views.PGNDetailsView.as_view(), name='game details'),
    path('game/<int:pk>/halfmove/<int:halfmove>/', views.PGNOnMoveDetailsView.as_view(), name='game move'),
    path('game/edit/<int:pk>/', views.PGNInfoEditView.as_view(), name='game edit'),
    path('game/delete/<int:pk>/', views.PGNDeleteView.as_view(), name='game delete')

]
