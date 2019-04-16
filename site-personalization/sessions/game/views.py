from django.shortcuts import render, HttpResponse, redirect
from .models import PlayerGameInfo, Player, Game
import string, random, django


def show_home(request):

    context = {}

    if not request.session.exists(request.session.session_key):
        request.session.create()

    session_id = request.session.session_key

    # Поиск открытой игры
    game_id = PlayerGameInfo.objects.filter(game_status=True)

    # Проверка, просмотрены ли результаты игры загадавшим игроком
    game_number_is_guessed = PlayerGameInfo.objects.filter(is_guessed=True)

    # Загадавший проверяет результат(ск-ко потребовалось попыток)
    if game_number_is_guessed:
        context = {}
        for game in game_number_is_guessed:

            if game.player_id.player_id == session_id:

                context['hide_magic_number'] = 'hidden'
                context['hide_answer'] = 'hidden'
                context['is_guessed'] = 'Ваше число угадано, всего попыток {}'\
                    .format(game.attempts)
                game.is_guessed = False
                game.save()

                return render(
                    request,
                    'home.html', context
                )

    # Если идет игра
    if game_id:

        game_id = PlayerGameInfo.objects.get(game_status=True)

        # Проверка Игрока №1
        if game_id.player_id.player_id == session_id:
            return render(
                request,
                'home.html', {'hide_answer': 'hidden',
                              'hide_magic_number': 'hidden',
                              'message': 'Идет игра. Ваше число угадывается'}
                )

        # Проверка Игрока2, когда идет игра
        # Игрок2 не default player
        players = Player.objects.filter(player_id=session_id)
        if game_id.guess.player_id != 'default':

            # Игрок2 есть в БД
            for player in players:

                if player.player_id == session_id:

                    context['hide_magic_number'] = 'hidden'

                    # Попытка угадать
                    answer = request.POST.get('answer')

                    # Ответ '' или None равен False просто обновит страницу
                    if bool(answer) is False:
                        return render(
                            request,
                            'home.html', context
                        )
                    else:
                        game_id.attempts += 1

                        if game_id.magic_number == int(answer):

                            # Успешная попытка - Число отгадано
                            game_id.game_status = False
                            game_id.is_guessed = True
                            game_id.save()

                            context['hide_answer'] = 'hidden'
                            context['answer_win'] = 'Вы победили'
                            context['begin_again'] = ''
                            return render(
                                request,
                                'home.html', context
                            )
                        else:
                            # Неуспешная попытка
                            context['answer_fail'] = 'Попробуй еще раз, ' \
                                                     'попытка №{}'\
                                .format(game_id.attempts)
                            game_id.save()

                            return render(
                                request,
                                'home.html', context
                            )
            else:
                # Заглушка для "лишних" пользователей
                return HttpResponse('Ожидайте начало нового раунда')


            """В случае отсутствия Игрок2 в игре, когда player2 == 'default',
            то добавить Игрок2 в игру
            """
        else:

            # Игрок2 есть в БД

            if len(players) != 0:
                player_id = Player.objects.get(player_id=session_id)
                game_id = PlayerGameInfo.objects.get(game_status=True)
                PlayerGameInfo.objects.filter(game_status=True)\
                    .update(guess=player_id.id)
                game_id.save
                Player.objects.get(player_id='default').delete()

            # Игрок2 отсутствует в БД
            else:
                player = Player.objects.get(player_id='default')
                player_id = request.session.session_key
                player.player_id = player_id
                player.save()

            return redirect(
                'show_home'
            )


    if not game_id:
        # Если игра не началась, то Дефолтная страница до начала игры
        if request.method == 'GET':
            context['hide_answer'] = 'hidden'
            return render(
                request,
                'home.html', context
            )

        # Инициализация игры, передача загаданного числа
        if request.POST.get('magic_number'):
            magic_number = request.POST.get('magic_number')
            # Передано загаданное число
            # if magic_number:

            if len(Player.objects.values('player_id')
                           .filter(player_id=session_id)) == 0:
                player = Player(player_id=session_id)
                player.save()

            players = Player.objects.filter(player_id=session_id)
            for player in players:

                if player.player_id != session_id:
                    player = Player(player_id=session_id)
                    player.save()
            guess = Player(player_id='default')
            guess.save()

            game_id = ''.join(random.choices(string.ascii_lowercase +
                                             string.digits, k=30))
            game = Game(game_id=game_id)
            game.save()
            player_id = Player.objects.get(player_id=request.session.session_key)
            game_id = Game.objects.get(game_id=game_id)
            begin_date = django.utils.timezone.now()
            player_game_info = PlayerGameInfo(player_id=player_id,
                                              game_id=game_id,
                                              game_status=True,
                                              magic_number=magic_number,
                                              attempts=0, guess=guess,
                                              begin_date=begin_date,
                                              is_guessed=False)
            player_game_info.save()
            return redirect(
                'show_home',
            )

        """Не передано загаданное число, то показать
        Дефолтная страница до начала игры
        """
        context['hide_answer'] = 'hidden'
        return render(
            request,
            'home.html', context
        )
