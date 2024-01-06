from django.urls import path
from hoopsTacToeApp import views
from .views import *

urlpatterns = [
    path("", views.land, name="land"),
    path("game/", views.init_game, name='init_game'),
    path("button_click/<int:buttonNumber>/", button_click, name='button_click'),
    path("get_players_data/", get_players_data, name='get_players_data'),
    path("check_player/", check_player, name='check_player'),
    path("check_game/", check_game_over, name='check_game_over'),
    path("init_game/", init_game, name='init_game')
]
