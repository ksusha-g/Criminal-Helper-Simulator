# Вы можете расположить сценарий своей игры в этом файле.
# Определение персонажей игры.
define e = Character('Заказчик', color="#0f00b0")
image character = "character.png"
image background = im.Scale("background.webp", 1920, 1080)

label start:

    $ player = Player("Герой")

    scene background
    show character
    
    e 'Мне нужно почистить оружие, поможешь?'

    menu:
        "ok":
            jump clean_game
        "no":
            e 'ну и ладно!'

label clean_game:
    hide character
    hide background

    $ clean_weapon_task = Task(
        "clean_weapon",
        100,
        5,
        False
    )

    $ clean_weapon = CleanWeapon(clean_weapon_task, (400, 200, 450, 500))
    call screen clean_weapon_screen(clean_weapon)

    menu:
        "Вернуться":
            jump start
            


    return