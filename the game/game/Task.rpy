init python:

    class Task:
        def __init__(self, minigame_type, payment, reputation, persuade):
            self.minigame_type = minigame_type #тип мини-игры
            self.payment = payment #добавить max_payment
            self.reputation = reputation # добавить max_reputation
            self.persuade = persuade #можно ли отговорить