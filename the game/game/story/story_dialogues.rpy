define ofela = Character("Офеля")
define you = "Я"

label ofela_day_1:

    scene background

    show expression "sad_client" as character at client_size
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
            
            $ task = tasks[0]

            jump start_task

        "Отказаться":
            $ ofela_helped = False
            ofela "😭😭😭 (("
            $ game.current_day.statistics.add_refused_client()
            return