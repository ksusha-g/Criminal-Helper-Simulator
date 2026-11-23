
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
            spacing 25
            xalign 0.5
            yalign 0.5

            text "Газета":
                size 45
                color "#302820"
                xalign 0.5

            if game.last_day_report is None:

                text "Пока нет результатов предыдущего дня.":
                    size 25
                    color "#302820"
                    xalign 0.5
                    text_align 0.5

            else:

                text "Итоги дня [game.last_day_report['day_number']]":
                    size 32
                    color "#302820"
                    xalign 0.5

                null height 10

                text "Обслужено клиентов: [game.last_day_report['clients_served']]":
                    size 24
                    color "#302820"

                text "Отказано клиентам: [game.last_day_report['clients_refused']]":
                    size 24
                    color "#302820"

                text "Заработано денег: [game.last_day_report['money_earned']]":
                    size 24
                    color "#302820"

                text "Изменение репутации: [game.last_day_report['reputation_earned']]":
                    size 24
                    color "#302820"

            null height 10

            textbutton "Закрыть":
                xalign 0.5
                action Hide("newspaper_info")
