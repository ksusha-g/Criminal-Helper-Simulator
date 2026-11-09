init python:

    class Player:
        def __init__(self, name):
            self.name = name
            self.money = 0
            self.reputation = 0

        def earn(self, amount): #получить деньги
            self.money += amount 

        def change_reputation(self, amount): #смена репутации
            self.reputation += amount

        def get_money(self):
            return f'{self.money}'

        def get_reputation(self):
            return f'{self.reputation}'