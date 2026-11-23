screen minigame_help(game):
    modal True
    zorder 100

    add Solid("#000000cc")

    frame:
        xalign 0.5
        yalign 0.5
        xpadding 40
        ypadding 30
        background Solid("#ffffff")

        vbox:
            spacing 20
            xalign 0.5

            text "Как играть":
                size 30
                bold True
                color "#222222"
                xalign 0.5

            text '[game.get_help_text()]':
                size 20
                color "#030303"
                xmaximum 500
                text_align 0.5
                xalign 0.5

            textbutton "OK":
                xalign 0.5
                text_size 24
                action Hide("minigame_help")