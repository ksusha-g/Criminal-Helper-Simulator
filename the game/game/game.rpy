init python:
    class Game:
        def __init__(self, player, clients):
            self.player = player
            self.clients = clients

            self.last_day_report = None

            self.day_number = 0
            self.current_day = None

            self.client_generator = Client_generator(clients)

        def can_start_day(self):
            if self.player.reputation < -5:
                return False
            return True

        def start_day(self):
            if not self.can_start_day():
                return False

            self.day_number += 1

            self.current_day = Day(
                self.day_number,
                self.client_generator
            )

            self.current_day.start()

            return True

        def finish_day(self):
            if self.current_day:
                self.current_day.finish()

                stats = self.current_day.statistics

                self.last_day_report = {
                    "day_number": self.current_day.day_number,
                    "clients_served": stats.clients_served,
                    "clients_refused": stats.clients_refused,
                    "money_earned": stats.money_earned,
                    "reputation_earned": stats.reputation_earned
                }

            return True

        def next_day(self):
            self.finish_day()

            if self.can_start_day():
                self.start_day()
            
            return False

        
        def apply_task_result(self, task, result, count_as_client=True):

            if result == MiniGameResult.GOOD:
                self.player.earn(task.payment)
                self.player.change_reputation(task.reputation)

                self.current_day.statistics.add_money(task.payment)
                self.current_day.statistics.add_reputation(task.reputation)

            elif result == MiniGameResult.MEDIUM:
                self.player.earn(task.payment // 2)

                self.current_day.statistics.add_money(task.payment // 2)

            elif result == MiniGameResult.BAD:
                self.player.change_reputation(-(task.reputation // 2))

                self.current_day.statistics.add_reputation(-(task.reputation // 2))

            if count_as_client:
                self.current_day.statistics.add_served_client()

                
