init python:
    class MiniGameState(Enum): #применяет Finite State Machine для мини-игр
        READY = auto() #разные состояния мини-игры
        RUNNING = auto()
        FINISHED = auto()