transform client_size:
    xysize (2000, 1800)
    fit "contain"
    xalign 0.5

define e = Character(
    'game.current_day.current_client.name',
    dynamic = True, #позволяет вычислять имя персонажа перед репликой
    color = "#000000"
)
image background = im.Scale("background.webp", 1920, 1080)
image table = im.Scale('table.png', 1920, 1080)
image newspaper = im.Scale('newspaper.png', 1920, 1080)

default game_data = None
default game = None
default player = None

label start:

    $ game_data = GameData()
    $ game_data.load()
    $ player = Player("Герой")
    $ game = Game(player, game_data.clients)
    'Добро пожаловать в игру!'

    jump new_day

label close_market:
    scene background
    'Вы проиграли. Ваша репутация слишком низкая.'
    return

label new_day:
    scene background
    $ game.start_day()

    'Начался день [game.day_number]'

    jump client_interaction 

label finish_day:
    scene background
    $ game.finish_day()

    'День [game.day_number] завершен.'

    jump new_day

label client_interaction:
    scene background
    show expression game.current_day.current_client.image as character at client_size
    show table
    show newspaper
    show screen states

    e '[game.current_day.current_client.phrase]'

    menu:
        "Помочь":
            jump start_task
        "Отказать":
            e '[game.current_day.current_client.reject]'
            jump next_client

label next_client:
    $ game.current_day.finish_client()

    if player.reputation < -5:
        jump close_market

    if game.current_day.is_finished:
        jump finish_day
    else:
        jump client_interaction

label start_task:
    hide character
    hide table
    hide newspaper
    hide background
    hide screen states

    $ task = game.current_day.current_client.tasks[0]

    $ minigame = MiniGameFactory.create_minigame(task)

    $ screen_name = task.minigame_type + '_screen'
    $ result_screen = renpy.call_screen(screen_name, minigame)

    if result_screen == 'exit':

        $ result = minigame.result
        if result == 'bad':
            e '[game.current_day.current_client.get_comment("bad")]'

            menu:
                "Вернуться к прилавку":
                    $ game.apply_task_result(task, result)
                    jump next_client
                "Попробовать снова":
                    jump start_task

        if result == 'medium':
            e '[game.current_day.current_client.get_comment("medium")]'

            menu:
                "Вернуться к прилавку":
                    $ game.apply_task_result(task, result)
                    jump next_client

            
        if result == 'good':

            e '[game.current_day.current_client.get_comment("good")]'

            menu: 
                "Вернуться к прилавку":
                    $ game.apply_task_result(task, result)
                    jump next_client

    return
