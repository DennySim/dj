from django.db import models


class Player(models.Model):
    pass
    # player = models.CharField(max_length=50)
    # is_author = models.BooleanField(default=False)


class Game(models.Model):
    # game = models.CharField(max_length=50)
    begin_date = models.DateTimeField(auto_now_add=True)
    # magic_number = models.IntegerField()
    is_open = models.BooleanField(default=True)

    magic_number = models.IntegerField(default=None)


class PlayerGameInfo(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_game')
    # guess_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='guess_player')
    # is_guessed = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)
    is_author = models.BooleanField(default=False)



