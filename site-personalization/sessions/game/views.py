from django.shortcuts import render, HttpResponse, redirect
from .models import PlayerGameInfo, Player, Game
import string
import random


def render_home(request, context):
    return render(
        request,
        'home.html', context
    )


def player_id_check(request):
    # print('player_id_check')
    if 'player_id' not in request.session:
        player = Player()
        player.save()
        request.session['player_id'] = player.id

    return Player.objects.get(id=request.session['player_id'])


def game_check(request, player):
    # print('game_check')

    game_set = Game.objects.filter(is_open=True)
    if game_set:
        return Game.objects.get(is_open=True)
    else:
        magic_number = random.randint(1, 10)
        game = Game()
        game.magic_number = magic_number
        game.save()
        request.session['game_id'] = game.id
        player_game_info_creation(player, game, True)
        return game


def player_game_info_creation(player, game, is_author):
    # print('player_game_info_creation')

    player_game_info = PlayerGameInfo(player=player,
                          game=game,
                          is_author=is_author,
                          )
    player_game_info.save()


def answer_attempt(request):
    # print('answer_attempt')
    answer = request.POST.get('answer')
    player = player_id_check(request)
    game = game_check(request, player)
    player_game_info = PlayerGameInfo.objects.get(game=game, is_author=False)

    if bool(answer):

        player_game_info.attempts += 1
        player_game_info.save()

        return int(answer)


def show_home(request):
    print('show_home')
    context = {}
    player = player_id_check(request)

    has_opened_games = Game.objects.filter(is_open=True)

    if not has_opened_games:
        # Нет открытой Игры и Игрок без game_id
        if 'game_id' not in request.session:
            # Создать Игру
            game_check(request, player)
    else:
        open_game = Game.objects.get(is_open=True)
        players = PlayerGameInfo.objects.filter(game=open_game.id)\
            .values_list('player', flat=True)
        player_count = len(players)

        # Добавление второго Игрока в игру
        if 'game_id' not in request.session:

            # Если зашел третий Игрок, а два игрока уже в Игре
            if player_count == 2:
                return HttpResponse('Ожидайте начало нового раунда')

            game = has_opened_games.get(is_open=True)
            request.session['game_id'] = game.id
            player_game_info_creation(player, game, False)

    current_game = Game.objects.get(id=request.session['game_id'])
    player_game_info = PlayerGameInfo.objects.get(
         game_id=request.session['game_id'], player=player)

    if player_game_info.is_author:

        if not current_game.is_open:

            player_game_info = PlayerGameInfo.objects.get(
                game_id=request.session['game_id'], is_author=False)

            del request.session['game_id']
            context['is_guessed'] = 'Ваше число угадано, всего попыток {}' \
                .format(player_game_info.attempts)

        else:
            context['message'] = 'Идет игра. Ваше число угадывается'

        context['hide_magic_number'] = 'hidden'
        context['hide_answer'] = 'hidden'
        return render_home(request, context)

    if not player_game_info.is_author:

        print('not author')
        player_game_info = PlayerGameInfo.objects.get(
            game_id=request.session['game_id'], is_author=False)

        if current_game.is_open:

            answer = answer_attempt(request)
            player_game_info.refresh_from_db()

            if not answer or answer != current_game.magic_number:
                print('Loose')
                context['hide_magic_number'] = 'hidden'
                context['answer_fail'] = 'Попробуй еще раз, ' \
                                         'попытка №{}' \
                    .format(player_game_info.attempts + 1)
                return render_home(request, context)

            else:
                print('Win')

                del request.session['game_id']
                current_game.is_open = False
                current_game.save()

                context['hide_answer'] = 'hidden'
                context['answer_win'] = 'Вы победили'
                context['begin_again'] = ''
                return render_home(request, context)