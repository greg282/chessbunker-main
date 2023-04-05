from django.urls import path

from . import views

urlpatterns = [
    path("player/login/", views.login_user, name="login"),
    path("player/logout/", views.logout_user, name="logout"),
    path("player/ranking/", views.ranking, name="ranking"),
    path('player/', views.PlayerAPI.as_view(), name="player"),
    path('game/', views.GameAPI.as_view(), name="game"),
]
