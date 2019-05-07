from django.db import models


class Player(models.Model):
    player = models.CharField(max_length=50)


class Game(models.Model):
    game = models.CharField(max_length=50)
    begin_date = models.DateTimeField(auto_now_add=True)
    magic_number = models.IntegerField()
    game_status = models.BooleanField()


class PlayerGameInfo(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    guess = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='guess_player')
    is_guessed = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    attempts = models.IntegerField()



