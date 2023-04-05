from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    elo = models.IntegerField(default=1000)
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    games_lost = models.IntegerField(default=0)
    games_draw = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.elo}"


class Game(models.Model):
    class Status(models.TextChoices):
        MATCHMAKING = 'MM', 'Matchmaking'
        CODE_JOIN = 'CJ', 'Code join',
        START = 'ST', 'Start game'
        IN_PROGRESS = 'IP', 'In progress'
        ENDED = 'ED', 'Ended'

    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.MATCHMAKING)
    join_code = models.CharField(max_length=10, default=None, null=True)
    white = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, related_name="white")
    black = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, related_name="black")
    winner = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, default=None)
    white_timer = models.IntegerField(default=900)
    black_timer = models.IntegerField(default=900)
    fen = models.CharField(max_length=200, default=None, null=True)
    event_server_url = models.CharField(
        max_length=100, default=None, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.white} vs {self.black}"
