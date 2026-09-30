screen clean_weapon_screen(clean_weapon):
    
    text 'Очищено на [int(clean_weapon.clean_progress * 100)]%':
        xalign 0.5 
        yalign 0.03

    add 'clean_axe.png':
        xpos 100
        ypos 100

    add 'dirty_axe.png':
        alpha clean_weapon.dirty_alpha
        
        xpos 100
        ypos 100
    
    draggroup:

        drag:
            add 'napkin.png'

            drag_name 'napkin'

            draggable True

            xpos 1300
            ypos 600
            
            activated clean_weapon.start_drag
            dragging clean_weapon.update_drag
            dragged clean_weapon.finish_drag

    textbutton 'Вернуться к прилавку':
        xalign 0.5
        yalign 0.9
        action Return('exit')