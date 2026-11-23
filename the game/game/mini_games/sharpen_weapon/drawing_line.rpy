init python:
    class DrawingLine(renpy.Displayable):

        def __init__(self, sharpen_weapon, **kwargs):

            super(DrawingLine, self).__init__(**kwargs)

            self.sharpen_weapon = sharpen_weapon

            # Цвет линии (бирюзовый)
            self.color = (40, 220, 210, 255)

            # Толщина линии
            self.line_width = 4

        def render(self, width, height, st, at):

            # Создаём область для рисования
            render = renpy.Render(width, height)

            canvas = render.canvas()

            coordinates = self.sharpen_weapon.coordinates

            # Рисуем линию между соседними координатами
            for i in range(len(coordinates) - 1):

                start = coordinates[i]
                end = coordinates[i + 1]

                canvas.line(
                    self.color,
                    start,
                    end,
                    self.line_width
                )

            # Обновляем отображение во время рисования
            if self.sharpen_weapon.is_drawing:
                renpy.redraw(self, 0.02)

            return render