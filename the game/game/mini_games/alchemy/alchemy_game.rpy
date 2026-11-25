screen alchemy_screen(alchemy):
    modal True

    draggroup:
    
        drag:
            drag_name "cauldron"
            draggable False
            droppable True

            xalign 0.3
            yalign 0.8

            add "cauldron.webp":
                zoom 3.0

        if alchemy.ingredients["sagebrush"]["count"] > 0:
            if alchemy.ingredients["sagebrush"]["count"] > 1:
                drag:
                    draggable False
                    droppable False

                    xpos alchemy.ingredients["sagebrush"]["x"]
                    ypos alchemy.ingredients["sagebrush"]["y"]

                    add "sagebrush.webp"

            drag:
                drag_name "sagebrush"
                draggable True
                droppable False
                dragged alchemy.ingredient_dropped

                xpos alchemy.ingredients["sagebrush"]["x"]
                ypos alchemy.ingredients["sagebrush"]["y"]

                add "sagebrush.webp"

        if alchemy.ingredients["mandrake"]["count"] > 0:
            if alchemy.ingredients["mandrake"]["count"] > 1:
                drag:
                    draggable False
                    droppable False

                    xpos alchemy.ingredients["mandrake"]["x"]
                    ypos alchemy.ingredients["mandrake"]["y"]

                    add "mandrake.jpg":
                        xsize 500
                        ysize 500

            drag:
                drag_name "mandrake"
                draggable True
                droppable False
                dragged alchemy.ingredient_dropped

                xpos alchemy.ingredients["mandrake"]["x"]
                ypos alchemy.ingredients["mandrake"]["y"]

                add "mandrake.jpg":
                    xsize 500
                    ysize 500

    text "Полынь: [alchemy.ingredients['sagebrush']['count']]":
        xalign 0.8
        yalign 0.28
        size 25
        color "#ffffff"

    text "Корень мандрагоры: [alchemy.ingredients['mandrake']['count']]":
        xalign 0.85
        yalign 0.38
        size 25
        color "#ffffff"



    textbutton 'Вернуться к прилавку':
        xalign 0.5
        yalign 0.9
        action Return('exit')