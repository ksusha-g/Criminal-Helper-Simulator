init python:
    class MiniGame:
        """Общий класс. Держит только состояние."""
        def __init__(self, task):
            self.task = task
            self.state = MiniGameState.READY #заменяем состояние на Enum (классы выше)
            self.result = MiniGameResult.BAD

        def finish(self, result):
            self.state = MiniGameState.FINISHED
            self.result = result