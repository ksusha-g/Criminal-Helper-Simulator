screen newspaper_info():

    modal True

    add Solid("#00000099")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 500

        background "#E8DFC9"

        vbox:
            spacing 30
            xalign 0.5
            yalign 0.5

            text "Газета":
                size 45
                color "#302820"
                xalign 0.5

            text "Здесь будут результаты предыдущего дня.":
                size 28
                color "#302820"
                xalign 0.5
                text_align 0.5

            textbutton "Закрыть":
                xalign 0.5
                action Hide("newspaper_info")
