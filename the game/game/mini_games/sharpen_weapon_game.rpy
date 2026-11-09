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


    for point in sharpen_weapon.points:
        
        if point['collected']:
            add Solid("#55dd77"):
                xysize (18, 18)
                xpos point["x"]
                ypos point["y"]

        else:
            add Solid("#ffcc33"):
                xysize (18, 18)
                xpos point["x"]
                ypos point["y"]

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
        timer 0.01 action Return('good')