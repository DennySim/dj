from django.db import models


class Player(models.Model):
    player_id = models.CharField(max_length=50)
    pass


class Game(models.Model):
    game_id = models.CharField(max_length=50)
    pass


class PlayerGameInfo(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    attempts = models.IntegerField()
    magic_number = models.IntegerField()
    game_status = models.BooleanField()
    guess = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='guess_player')
    is_guessed = models.BooleanField(default=False)
    begin_date = models.DateTimeField()
    pass
