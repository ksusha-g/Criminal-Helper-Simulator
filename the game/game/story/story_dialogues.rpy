define ofela = Character("Офеля",
    screen='dialogs')
define you = "Я"


label ofela_day_1:

    # Указываем, что сейчас идёт сюжетная встреча
    $ is_story_encounter = True

    # Получаем сюжетного персонажа из StoryManager
    $ current_interaction_character = story_manager.characters["ofela"]

    scene background

    show expression current_interaction_character.image as character at client_size
    show table

    show screen newspaper_screen
    show screen states

    ofela "Привет..."
    ofela "Я кое-что натворил...("

    menu:
        "Что случилось?":
            ofela "Ну..."
            ofela "Я нес топорик домой... Ну в смысле к себе..."
            ofela "И там, ну, так вышло..."
            ofela "Ты не поверишь."
            ofela "Я подскользнулся."
            ofela "И я- точнее топор- ну, там кто-то стоял..."
            ofela "И там, ну, так вышло..."
            ofela "Ты не поверишь."
            you "Понятно."
            ofela "Ты мне поможешь? Что мне делать?"

        "Ты кто?":
            ofela "Я Офеля."
            ofela "Помоги пожалуйста."

    jump ofela_help_choice


label ofela_help_choice:

    menu:

        "Помочь":
            you "Умойся. Я очищу твой топор."
            ofela "Спасибо!!!"

            # Получаем настоящий объект Task из GameData
            $ task = game_data.tasks["clean_weapon"]

            jump start_task

        "Отказаться":
            $ ofela_helped = False
            ofela "😭😭😭 (("

            jump finish_story_encounter
