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
            jump clean_game
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

label clean_game:
    hide character
    hide table
    hide newspaper
    hide background
    hide screen states

    $ clean_weapon_task = Task(
        "clean_weapon",
        100,
        5,
        False
    )

    $ clean_weapon = CleanWeapon(clean_weapon_task, (400, 250, 450, 500))
    call screen clean_weapon_screen(clean_weapon)

    if _return == 'exit':

        $ result = clean_weapon.result
        if result == 'bad':
            e '[game.current_day.current_client.comments["bad"]]'

            menu:
                "Вернуться к прилавку":
                    $ game.apply_task_result(clean_weapon_task, result)
                    jump next_client
                "Попробовать снова":
                    jump clean_game

        if result == 'medium':
            e '[game.current_day.current_client.comments["medium"]]'

            menu:
                "Вернуться к прилавку":
                    $ game.apply_task_result(clean_weapon_task, result)
                    jump next_client

            
        if result == 'good':

            e '[game.current_day.current_client.comments["good"]]'

            menu: 
                "Вернуться к прилавку":
                    $ game.apply_task_result(clean_weapon_task, result)
                    jump next_client

    return
