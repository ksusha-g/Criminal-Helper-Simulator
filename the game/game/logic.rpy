# game/logic.rpy
init python:
    import math

    class Player:
        def __init__(self, name):
            self.name = name
            self.money = 0
            self.reputation = 0

        def earn(self, amount): #получить деньги
            self.money += amount 

        def change_reputation(self, amount): #смена репутации
            self.reputation += amount


    class Task:
        def __init__(self, minigame_type, payment, reputation, persuade):
            self.minigame_type = minigame_type #тип мини-игры
            self.payment = payment #добавить max_payment
            self.reputation = reputation # добавить max_reputation
            self.persuade = persuade #можно ли отговорить


    class Client:
        def __init__(self, name, phrase, tasks):
            self.name = name #имя клиента
            self.phrase = phrase # речь клиента
            self.tasks = tasks  #список доступных заданий


    class MiniGame:
        """Общий класс. Держит только состояние."""
        def __init__(self, task):
            self.task = task
            self.state = "running"      # running / finished
            self.result = None          # плохо / средне / хорошо

        def finish(self, result):
            self.state = "finished"
            self.result = result

    class CleanWeapon(MiniGame):

        def __init__(self, task, axe_area):
            super().__init__(task)

            self.axe_area = axe_area # область топора
            self.dirty_axe = 1.0
            self.clean_progress = 0.0 # прогресс очистки, 1.0 - полностью чисты
            self.mouse_pressed = False #держит ли тряпку мышкой
            self.clean_amount = 0.005 #на осколько очищается топор за один вызов
            

        @property
        def dirty_alpha(self): #прозрачность грязного топора
            return self.dirty_axe - self.clean_progress

        #вызываем в момент, когда игрок нажал на тряпочку   
        def start_drag(self, drags):
            self.mouse_pressed = True

        #вызываем во время движения мышкой
        def update_drag(self, drags):
    
            #условие: тряпочка находится над топором
            if not self.napkin_over_axe(drags[0]):
                return

            self.clean_progress += self.clean_amount

            if self.clean_progress >= 1:
                self.finish('good')
                return True

            renpy.restart_interaction()
            print(self.clean_progress)
            

        def finish_drag(self, drags, drop):
            self.mouse_pressed = False

        def napkin_over_axe(self, napkin):
            axe_x, axe_y, axe_width, axe_height = self.axe_area

            axe_right = axe_x + axe_width
            axe_bottom = axe_y + axe_height

            return (napkin.x < axe_right
                    and napkin.x > axe_x
                    and napkin.y < axe_bottom
                    and napkin.y > axe_y)




