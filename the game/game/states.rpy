screen states():

    add 'states.png':
        xalign 0.01
        zoom 0.7

    text [game.current_day.get_time()]:
        size 70
        xalign 0.99
        ypos 5

    text [player.get_money()]:
        size 70
        xpos 125
        ypos 25
    
    text [player.get_reputation()]:
        size 70
        xpos 125
        ypos 130