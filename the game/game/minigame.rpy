screen clean_weapon_screen(clean_weapon):
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