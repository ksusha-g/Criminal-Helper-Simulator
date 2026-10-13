screen states():

    add 'states.png':
        xalign 0.01

    text [game.current_day.get_time()]:
        size 100
        xalign 0.99
        ypos 20

    text [player.get_money()]:
        size 100
        xalign 0.1
        ypos 35
    
    text [player.get_reputation()]:
        size 100
        xalign 0.1
        ypos 170