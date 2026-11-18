screen sharpen_weapon_screen(sharpen_weapon):

    modal True

    default weapon_image = sharpen_weapon.select_weapon_image()

    $ image_size = sharpen_weapon.get_image_size(weapon_image)

    add weapon_image:
        zoom image_size['zoom']
        xpos image_size['x']
        ypos image_size['y']

    add DrawingLine(sharpen_weapon)


    text 'Раунд: [sharpen_weapon.round_number] / 3':
        xalign 0.5
        yalign 0.03

    text 'Ошибки: [sharpen_weapon.mistakes]':
        xalign 0.0
        yalign 0.03

    if sharpen_weapon.is_checking:
        timer 0.8 action [
            SetField(sharpen_weapon, "is_checking", False),
            Function(sharpen_weapon.finalize_reset)
        ]

    for point in sharpen_weapon.points:
        
        if point['collected']:
            add Solid("#55dd77"):
                xysize (18, 18)
                xpos point["x"] - 9
                ypos point["y"] - 9

        else:
            add Solid("#ffcc33"):
                xysize (18, 18)
                xpos point["x"] - 9
                ypos point["y"] - 9

    #отпускаем мышку
    key "mouseup_1" action Function(
        sharpen_weapon.stop_drawing
    )

    key "mousedown_1" action Function(
        sharpen_weapon.start_drawing,
        renpy.get_mouse_pos()
    )
    
    #записываем движения мышки, пока игрок рисует
    timer 0.02 repeat True action Function(
        sharpen_weapon.record_coordinates,
        renpy.get_mouse_pos()
    )

    if sharpen_weapon.action_state == SharpenWeaponState.FINISHED:
        timer 0.01 action Return('exit')

    textbutton "?":
        xalign 0.98
        yalign 0.02
        text_size 40
        text_color "#ffcc33"
        text_bold True
        action Show("minigame_help", help_text=game_data.task_data["sharpen_weapon"]["help_text"])