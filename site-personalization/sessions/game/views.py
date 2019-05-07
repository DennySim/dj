from django.shortcuts import render, HttpResponse, redirect
from .models import PlayerGameInfo, Player, Game
import string
import random


def render_home(request, context):
    return render(
        request,
        'home.html', context
    )


def show_home(request):

    context = {}

    if not request.session.exists(request.session.session_key):
        request.session.create()

    session_id = request.session.session_key

    # Поиск открытой игры
    game_id = Game.objects.filter(game_status=True)

    # Проверка, просмотрены ли результаты игры загадавшим игроком
    game_number_is_guessed = PlayerGameInfo.objects.filter(is_guessed=True)

    # Загадавший проверяет результат(ск-ко потребовалось попыток)
    if game_number_is_guessed:

        context = {}
        for game in game_number_is_guessed:

            play_game = PlayerGameInfo.objects.get(game_id=game.game_id)
            # play_game = PlayerGameInfo.objects.get(game__game=game.game.game)  # Тоже рабочий вариант

            if play_game.player.player == session_id:

                context['hide_magic_number'] = 'hidden'
                context['hide_answer'] = 'hidden'
                context['is_guessed'] = 'Ваше число угадано, всего попыток {}'\
                    .format(play_game.attempts)

                play_game.is_guessed = False
                play_game.save()

                return render_home(request, context)

    # Если идет игра
    if game_id:
        def game_on(game_id):

            game_id = game_id.get(game_status=True)
            play_game = PlayerGameInfo.objects.get(game=game_id)
            # Проверка Игрока №1
            if play_game.player.player == session_id:
                context['hide_magic_number'] = 'hidden'
                context['hide_answer'] = 'hidden'
                context['message'] = 'Идет игра. Ваше число угадывается'

                return render_home(request, context)

            # Проверка Игрока2, когда идет игра
            # Игрок2 не default player
            players = Player.objects.filter(player=session_id)
            if play_game.guess.player != 'default':

                # Игрок2 есть в БД
                for player in players:
                    if player.player == session_id:
                        context['hide_magic_number'] = 'hidden'

                        # Попытка угадать
                        answer = request.POST.get('answer')

                        # Ответ '' или None равен False просто обновит страницу
                        if bool(answer) is False:
                            return render_home(request, context)
                        else:
                            play_game.attempts += 1
                            play_game.save()

                            if game_id.magic_number == int(answer):

                                # Успешная попытка - Число отгадано
                                game_id.game_status = False
                                game_id.save()

                                play_game.is_guessed = True
                                play_game.save()

                                context['hide_answer'] = 'hidden'
                                context['answer_win'] = 'Вы победили'
                                context['begin_again'] = ''
                                return render_home(request, context)

                            else:
                                # Неуспешная попытка
                                context['answer_fail'] = 'Попробуй еще раз, ' \
                                                         'попытка №{}'\
                                            .format(play_game.attempts + 1)

                                play_game.save()
                                return render_home(request, context)

                    # Игрок2 отсутствует в БД
                    else:
                        # Заглушка для "лишних" пользователей
                        return HttpResponse('Ожидайте начало нового раунда')

                """В случае отсутствия Игрок2 в игре, когда player2 == 'default',
                то добавить Игрок2 в игру
                """
            else:

                # Игрок2 есть в БД

                if len(players) != 0:
                    player = Player.objects.get(player=session_id)
                    PlayerGameInfo.objects.filter(game__game_status=True)\
                        .update(guess=player.id)
                    Player.objects.get(player='default').delete()

                # Игрока2 нет в БД
                else:
                    player = Player.objects.get(player='default')
                    player.player = request.session.session_key
                    player.save()

                return redirect(
                    'show_home'
                )
        return game_on(game_id)

    # Если не идет игра
    if not game_id:
        def game_off():

            # Если игра не началась, то Дефолтная страница до начала игры
            if request.method == 'GET':
                context['hide_answer'] = 'hidden'
                return render_home(request, context)

            # Инициализация игры, передача загаданного числа
            if request.POST.get('magic_number'):
                magic_number = request.POST.get('magic_number')
                # Передано загаданное число

                # Если нет игрока в БД
                if len(Player.objects.values('player')
                               .filter(player=session_id)) == 0:
                    player = Player(player=session_id)
                    player.save()

                guess = Player(player='default')
                guess.save()

                game_id = ''.join(random.choices(string.ascii_lowercase +
                                                 string.digits, k=30))
                game = Game(game=game_id,
                            magic_number=magic_number,
                            game_status=True
                            )
                game.save()

                # Должно быть инстансом Player для записи в модель PlayerGameInfo
                player_id = Player.objects.get(player=request.session.session_key)
                game_id = Game.objects.get(game=game_id)

                player_game_info = PlayerGameInfo(player=player_id,
                                                  game=game_id,
                                                  is_guessed=False,
                                                  attempts=0,
                                                  guess=guess,
                                                  )
                player_game_info.save()
                return redirect(
                    'show_home',
                )
            else:

                """Не передано загаданное число, то показать
                Дефолтная страница до начала игры
                """
            context['hide_answer'] = 'hidden'
            return render_home(request, context)
        return game_off()




