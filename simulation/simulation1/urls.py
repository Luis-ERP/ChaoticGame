from django.urls import path
from .views import *

urlpatterns = [
    path('', stats),
    path('game/player/new', create_player),
    path('game/player/<str:id_player>/delete', create_player),
    path('game/player/<str:id_player>/buycard', create_player),
    path('game/player/<str:id_player>/sellcard', create_player),
    path('game/player/<str:id_player>/addcash', create_player),
    path('game/player/<str:id_player>/retreivecash', create_player),
    path('game/player/<str:id_player>/play', create_player),
]
