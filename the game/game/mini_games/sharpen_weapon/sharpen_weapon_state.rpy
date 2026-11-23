init python:
    from enum import Enum, auto
    
    class SharpenWeaponState(Enum):
        READY = auto() #начало/повторно когда неудача/следующий раунд
        DRAWING = auto() #нельзя начать рисовать, если игрок уже рисует
        CHECKING = auto() #нельзя проверять до завершения рисования
        FINISHED = auto() #нельзя менять коордрдинаты, если не DRAWING
        #нельзя начать новый раунд после завершения мини-игры