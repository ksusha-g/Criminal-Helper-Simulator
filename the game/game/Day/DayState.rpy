init python:
    from enum import Enum, auto
    
    class DayState(Enum): #чтобы логика была корректной, дни не путались
        READY = auto() 
        PLAYING = auto()
        FINISHED = auto()