from django.db import models
from django.contrib.postgres.fields import ArrayField
from decouple import config

class Token(models.Model): 
    token = models.CharField(max_length=config('TK', cast=int))
    created_at = models.DateTimeField(auto_now_add=True)

class User(models.Model):
    first_name = models.CharField(verbose_name="first name", max_length=config('CHAR', cast=int))
    last_name = models.CharField(verbose_name="last name", max_length=config('CHAR', cast=int))
    username = models.CharField(max_length=config('CHAR', cast=int), unique=True, null=True)
    password = models.CharField(max_length=config('CHAR', cast=int), unique=True, null=True)
    token = models.OneToOneField(Token, on_delete=models.CASCADE, primary_key=True)
    win_streak = models.IntegerField(verbose_name="win streak", null=True, default=0)
    best_streak = models.IntegerField(verbose_name="best streak", null=True, default=0)
    wins = models.IntegerField(verbose_name="wins", null=True, default=0)
    losses = models.IntegerField(verbose_name="losses", null=True, default=0)
    in_game = models.BooleanField(verbose_name="in game", default=False)
    in_queue = models.BooleanField(verbose_name=" in queue", default=False)
    logged_in = models.BooleanField(verbose_name="logged in", default=False)
    in_create_game = models.BooleanField(verbose_name="in create game", default=False)
    cg_Id = models.CharField(verbose_name="current game id", max_length=config('GID', cast=int), null=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)

    def __unicode__(self):
        return self.username

class Game(models.Model):
    first = models.CharField(verbose_name="first player", max_length=config('CHAR', cast=int))
    second = models.CharField(verbose_name="second player", max_length=config('CHAR', cast=int))
    winner = models.CharField(verbose_name="winner", max_length=config('CHAR', cast=int), null=True)
    winner_streak = models.IntegerField(verbose_name="winner streak", null=True)
    fPoints = models.IntegerField(verbose_name="first points", null=True)
    sPoints = models.IntegerField(verbose_name="second points", null=True)
    gameId = models.CharField(verbose_name="game id", max_length=config('GID', cast=int), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CommentOrBug(models.Model):
    message = models.CharField(verbose_name="CommentOrBug", max_length=150)
    user = models.CharField(verbose_name="username", max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    





