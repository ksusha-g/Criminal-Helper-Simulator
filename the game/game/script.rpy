# Вы можете расположить сценарий своей игры в этом файле.
# Определение персонажей игры.
define e = Character('Заказчик', color="#0f00b0")
image bloody_axe = "bloody axe.png"
image cleaned_axe = "cleaned_axe.png"
image character = "character.png"
image background = im.Scale("background.webp", 1920, 1080)

screen clean_game_screen():
    default cleaning_progress = 0.1
    # bloody_axe всегда виден
    add "bloody_axe"
    add "cleaned_axe":
        alpha cleaning_progress

    draggroup:
        drag: 
            drag_name "napkin"
            child "napkin.png"
            draggable True
            droppable False
            xalign 0.75
            yalign 0.25
        
        drag:
            drag_name "bloody_axe"
            child "bloody axe.png"
            draggable False
            droppable False

            # Логика: если тащим, проверяем координаты
            # dragged dragged_napkin

# init python:
    # def dragged_napkin(drags, drop):
    #     # Координаты топора (где-то посередине экрана)
    #     axe_x = 960 # примерные координаты центра
    #     axe_y = 540
        
    #     # Берем текущие координаты тряпки
    #     napkin = drags[0]
        
    #     # Расстояние между тряпкой и топором
    #     import math
    #     dist = math.hypot(napkin.x - axe_x, napkin.y - axe_y)
        
    #     # Если тряпка близко к топору (радиус 200 пикселей)
    #     if dist < 100000:
    #         # Увеличиваем прогресс очистки, если двигаем мышкой
    #         # (Ren'Py обновляет это при каждом движении)
    #         current = renpy.get_screen("clean_game_screen").scope["cleaning_progress"]
    #         if current < 1.0:
    #             renpy.get_screen("clean_game_screen").scope["cleaning_progress"] += 0.05
    #             renpy.restart_interaction()


label start:

    scene background
    show character
    
    e 'Мне нужно почистить оружие, поможешь?'

    menu:
        "ok":
            jump clean_game


label clean_game:
    hide character
    hide background
    call screen clean_game_screen
    return