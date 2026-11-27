transform client_size:
    xysize (2000, 1800)
    fit "contain"
    xalign 0.5

define e = Character(
    'current_interaction_character.name',
    dynamic=True,
    color="#000000",
    screen='dialogs'
)

image background = im.Scale("background.webp", 1920, 1080)
image table = im.Scale("table.png", 1920, 1080)

default game_data = None
default game = None
default player = None

#НОВОЕ: переменные для задания и мини-игры
default task = None
default minigame = None
default result = None
default result_screen = None
default screen_name = None

#История
default story_manager = None
default story_event_completed = {}
default today_events = []

default current_interaction_character = None
default is_story_encounter = False
default story_flags = {}
default current_story_comments = {}
default current_story_event = None



label start:

    $ game_data = GameData()
    $ game_data.load()

    $ player = Player("Герой")
    $ game = Game(player, game_data.clients)

    $ story_manager = StoryManager(
        STORY_CHARACTERS,
        STORY_EVENTS
    )

    jump new_day


label close_market:

    scene background

    'Вы проиграли. Ваша репутация слишком низкая.'

    return


label new_day:

    scene background
    hide screen newspaper_screen

    $ day_started = game.start_day()

    if not day_started:
        jump close_market

    window hide
    'Начался день [game.day_number]'
    window hide

    call run_story_events

    jump client_interaction

label run_story_events:

    $ today_events = story_manager.get_events(
        game.day_number,
        story_event_completed
    )

    while today_events:
        $ current_story_event = today_events.pop(0)

        $ current_interaction_character = story_manager.characters[
            current_story_event.character_id
        ]

        $ current_story_comments = current_story_event.comments
        $ is_story_encounter = True

        # Временная отладка
        $ print("EVENT:", current_story_event.event_id)
        $ print("EVENT COMMENTS:", current_story_event.comments)
        $ print("CURRENT COMMENTS:", current_story_comments)

        call expression current_story_event.label

        $ story_manager.complete_event(
            current_story_event,
            story_event_completed
        )

        $ current_story_comments = {}
        $ current_story_event = None
        $ current_interaction_character = None
        $ is_story_encounter = False

    return

label finish_day:

    scene background
    hide screen newspaper_screen

    $ game.finish_day()

    'День [game.day_number] завершен.'

    $ print("DAY REPORT:", game.last_day_report)

    jump new_day


label client_interaction:

    $ is_story_encounter = False
    $ current_interaction_character = game.current_day.current_client

    scene background

    show expression current_interaction_character.image as character at client_size
    show table
    show screen newspaper_screen
    show screen states

    e '[current_interaction_character.phrase]'

    menu:

        "Помочь":
            $ task = current_interaction_character.tasks[0]
            jump start_task

        "Отказать":
            e '[current_interaction_character.reject]'
            $ game.current_day.statistics.add_refused_client()
            jump next_client


label next_client:

    $ game.current_day.finish_client()

    #вместо самостоятельной проверки репутации
    if not game.can_start_day():
        jump close_market

    #ИЗМЕНЕНО: теперь день проверяется через DayState
    if game.current_day.state == DayState.FINISHED:
        jump finish_day

    jump client_interaction


label start_task:
    hide character
    hide table
    hide screen newspaper_screen
    hide background
    hide screen states
    
    $ minigame = MiniGameFactory.create_minigame(task)

    if minigame is None:
        jump client_interaction

    $ screen_name = task.minigame_type + '_screen'

    $ result_screen = renpy.call_screen(screen_name, minigame)

    if result_screen == 'exit':

        #ИЗМЕНЕНО: результат теперь Enum, а не строка
        $ result = minigame.result

        jump task_result

    #если экран вернул что-то другое, возвращаемся к клиенту
    jump client_interaction


#НОВОЕ: отдельный label для обработки результатов, чтобы не дублировать одинаковую логику
label task_result:
    scene background

    show expression current_interaction_character.image as character at client_size
    show table
    show screen newspaper_screen
    show screen states

    if result == MiniGameResult.BAD:

        e '[get_interaction_comment(current_interaction_character, "bad", current_story_comments)]'

        menu:

            "Вернуться":

                $ game.apply_task_result(
                    task,
                    result,
                    not is_story_encounter
                )

                if is_story_encounter:
                    $ story_manager.apply_result(
                        current_story_event.event_id,
                        result,
                        story_flags
                    )
                    jump finish_story_encounter

                jump next_client

            "Попробовать снова":

                jump start_task


    elif result == MiniGameResult.MEDIUM:

        e '[get_interaction_comment(current_interaction_character, "medium", current_story_comments)]'

        menu:

            "Вернуться":

                $ game.apply_task_result(
                    task,
                    result,
                    not is_story_encounter
                )

                if is_story_encounter:
                    $ story_manager.apply_result(
                        current_story_event.event_id,
                        result,
                        story_flags
                    )
                    jump finish_story_encounter

                jump next_client


    elif result == MiniGameResult.GOOD:

        e '[get_interaction_comment(current_interaction_character, "good", current_story_comments)]'

        menu:

            "Вернуться":

                $ game.apply_task_result(
                    task,
                    result,
                    not is_story_encounter
                )

                if is_story_encounter:
                    $ story_manager.apply_result(
                        current_story_event.event_id,
                        result,
                        story_flags
                    )
                    jump finish_story_encounter

                jump next_client


    else:

        'Не удалось определить результат мини-игры.'

        if is_story_encounter:
            jump finish_story_encounter

        jump client_interaction
        

label finish_story_encounter:
    return
