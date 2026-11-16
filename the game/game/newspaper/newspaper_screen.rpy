screen newspaper_screen():

    #зображение газеты.
    add "newspaper.png"

    #oбласть нажатия поверх изображения.
    button:
        xpos 232
        ypos 773
        xsize 315
        ysize 157

        background None
        hover_background None

        action Show("newspaper_info")
