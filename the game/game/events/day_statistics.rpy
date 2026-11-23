init python:
    class DayStatistics:

        def __init__(self):
            self.clients_served = 0
            self.clients_refused = 0
            self.money_earned = 0
            self.reputation_earned = 0

        
        def add_served_client(self):
            self.clients_served += 1

        def add_refused_client(self):
            self.clients_refused += 1

        def add_money(self, amount):
            self.money_earned += amount

        def add_reputation(self, amount):
            self.reputation_earned += amount

