# game/logic.rpy
init python:
    import math
    import json
    import random
    
    def load_json(file_path):

        with renpy.open_file(file_path) as file:
            return json.load(file)

    class Game:
        
        def __init__(self, player, clients):
            self.player = player
            self.clients = clients

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

        def finish_day(self):
            if self.current_day:
                self.current_day.finish()

        def next_day(self):
            self.finish_day()

            if self.can_start_day():
                self.start_day()
            
            return False

        def apply_task_result(self, task, result):
            
            if result == 'good':
                self.player.earn(task.payment)
                self.player.change_reputation(task.reputation)
            elif result == 'medium':
                self.player.earn(task.payment//2)
            elif result == 'bad':
                self.player.change_reputation(-task.reputation//2)

    class Day:

        def __init__(self, day_number, client_generator, start_hour=8):
            self.day_number = day_number

            self.start_hour = start_hour
            self.current_hour = start_hour
            self.clients_number = 6

            self.clients = []
            self.current_client = None
            self.completed_clients = 0

            #отвечает за создание клиентов
            self.client_generator = client_generator
            self.is_finished = False


        def start(self):
            self.clients = self.client_generator.generate(
                self.clients_number
            )

            self.current_client = self.clients[0]

            print(f'день {self.day_number}, clients: {vars(self.current_client)}')

        def finish_client(self):
            self.completed_clients += 1
            #мини-игра длится 2 часа игрового времени
            self.current_hour += 2

            if self.completed_clients >= self.clients_number:
                self.finish()
                return

            self.current_client = self.clients[self.completed_clients]

        def finish(self):
            self.is_finished = True
            self.current_client = None

        def get_time(self):
            return f'{self.current_hour}:00'


    class Client_generator():

        def __init__(self, clients):
            self.clients = clients

        def generate(self, number):
            result = []

            for i in range(number):
                client = random.choice(self.clients)
                result.append(client)

            return result

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


    class Task:
        def __init__(self, minigame_type, payment, reputation, persuade):
            self.minigame_type = minigame_type #тип мини-игры
            self.payment = payment #добавить max_payment
            self.reputation = reputation # добавить max_reputation
            self.persuade = persuade #можно ли отговорить


    class Client:
        def __init__(self, name, image, phrase, reject, comments, tasks):
            self.name = name #имя клиента
            self.image = image #картинка клиента
            self.phrase = phrase # речь клиента
            self.reject = reject #речь клиента при отказе выполнения задания
            self.comments = comments # комментарии к выполнению задания
            self.tasks = tasks  #список доступных заданий

        def get_comment(self, result):
            return self.comments.get(result, '')



    class MiniGame:
        """Общий класс. Держит только состояние."""
        def __init__(self, task):
            self.task = task
            self.state = "running"      # running / finished
            self.result = 'bad'         # плохо (по умолчанию)/ средне / хорошо

        def finish(self, result):
            self.state = "finished"
            self.result = result


    class CleanWeapon(MiniGame):

        def __init__(self, task, weapon_area):
            super().__init__(task)

            self.weapon_area = weapon_area # область оружия
            self.dirty_weapon = 1.0 #полностью грязное оружие
            self.clean_progress = 0.0 # прогресс очистки, 1.0 - полностью чисты
            self.mouse_pressed = False #держит ли тряпку мышкой
            self.clean_amount = 0.002 #очистка за один вызов (в илеале 0.0008)

            self.axe_image = Image("dirty_axe.png")
            self.weapon_width, self.weapon_height = renpy.image_size(
                self.axe_image
            )
            

        @property
        def dirty_alpha(self): #прозрачность грязного оружия
            return self.dirty_weapon - self.clean_progress


        #вызываем в момент, когда игрок нажал на тряпочку   
        def start_drag(self, drags):
            self.mouse_pressed = True


        #вызываем во время движения мышкой
        def update_drag(self, drags):
            napkin = drags[0]

            #на всякий случай проверяем нажатие
            if not self.mouse_pressed:
                return

            #условие: тряпочка находится над оружием
            if not self.napkin_over_weapon(napkin):
                return
            
            if self.clean_progress <= 1.0:
                self.clean_progress += self.clean_amount

            if self.clean_progress < 0.65:
                self.result = 'bad'

            if self.clean_progress >= 0.65 and self.clean_progress < 1:
                self.result = 'medium'

            if self.clean_progress >= 1:
                self.result = 'good'

            renpy.restart_interaction()
            

        def finish_drag(self, drags, drop):
            self.mouse_pressed = False

        
        #проверяет находится ли тряпочка над непрозрачными 
        #пикселями оружия
        def napkin_over_weapon(self, napkin):
            weapon_x, weapon_y, weapon_width, weapon_height = self.weapon_area

            if renpy.is_pixel_opaque(
                self.axe_image,
                self.weapon_width,
                self.weapon_height,
                0.0,
                0.0,
                napkin.x,
                napkin.y
            ): 
                return True


    class SharpenWeapon(MiniGame):
        def __init__(self, task, weapon_area):
            super().__init__(task)

            self.weapon_area = weapon_area # область оружия

            self.round_number = 1
            self.max_rounds = 3

            #координаты линии
            self.coordinates = []

            # минимальное расстояние между координатами
            self.min_point_distance = 5

            # точки на оружии
            self.points = []
            self.collected_points = 0

            self.point_radius = 10
            self.generate_points()

        #выбор оружия
        def select_weapon_image(self):
            images = ['not_sharpen_axe', 'not_sharpen_sword']
            return random.choice(images)

        def get_image_size(self, image):
            if 'axe' in image:
                return {"x": -650, "y": 100, "zoom": 2.3}
            if 'sword' in image:
                return {"x": -1200, "y": -2500, "zoom": 4}

        #генерация точек на оружии
        def generate_points(self):
            self.points = []
            self.collected_points = 0

            x, y, width, height = self.weapon_area

            for i in range(10):

                self.points.append({
                    "x": random.randint(0, width),
                    "y": random.randint(0, height),
                    "collected": False
                })


        def start_drawing(self, position):
            self.is_drawing = True
            self.coordinates = [position]

        #запись координат линии, которую рисует игрок
        def record_coordinates(self, position):
            if not self.is_drawing:
                return

            last_position = self.coordinates[-1]

            distance = math.hypot(
                position[0] - last_position[0],
                position[1] - last_position[1]
            )

            if distance < self.min_point_distance:
                return

            self.coordinates.append(position)

        #блок геометрических проверок, напишу потом, пока ниче не понятно
        def stop_drawing(self):
            if not self.is_drawing: return

            self.is_drawing = False
            self.finish_attempt()


        def orientation(self, a, b, c):
            pass


        def on_segment(self, a, b, c):
            pass


        def segment_intersects(self, p1, q1, p2, q2):
            pass

        #проверка самопересечения линии
        def check_intersection(self):
            pass

        #расстояние от точки до отрезка
        def point_to_segment_distance(self, point, start, end):
            pass

        #проверка собранных точек
        def check_collected_points(self):
            pass

        #завершение попытки
        def finish_attempt(self):

            #проверяем самопересечение линии
            if self.check_intersection():
                self.reset_attempt()
                return

            #проверяем собранные точки
            if self.check_collected_points():
                self.next_round()
            else:
                self.reset_attempt()

        #сброс попытки
        def reset_attempt(self):
            self.coordinates = []
            self.collected_points = 0

            for point in self.points:
                point["collected"] = False

        #переход к следующему раунду
        def next_round(self):

            if self.round_number>= self.max_rounds:
                self.finish('good')
                return

            self.round_number += 1
            self.reset_attempt()
            self.generate_points()


    class GameData():

        def __init__(self):
            self.tasks = {}
            self.clients = []


        def load(self):

            task_data = load_json("data/tasks.json")
            client_data = load_json("data/clients.json")

            self.load_tasks(task_data)
            self.load_clients(client_data)


        def load_tasks(self, data):

            for task_id, task_data in data.items():

                self.tasks[task_id] = Task(
                    task_data["minigame_type"],
                    task_data["payment"],
                    task_data["reputation"],
                    task_data["persuade"]
                )

        def load_clients(self, data):

            for client_data in data:

                client_tasks = []

                for task_id in client_data["tasks"]:
                    client_tasks.append(self.tasks[task_id])

                client = Client(
                    name = client_data["name"],
                    image = client_data["image"],
                    phrase = client_data["phrase"],
                    comments = client_data["comments"],
                    reject = client_data["reject"],
                    tasks = client_tasks
                )

                self.clients.append(client)

    CLEAN_WEAPON_AREA = (400, 250, 450, 500) # область оружия
    SHARPEN_WEAPON_AREA = (400, 250, 450, 500) # область оружия

    class MiniGameFactory:

        @staticmethod
        def create_minigame(task):
            if task.minigame_type == "clean_weapon":
                return CleanWeapon(task, CLEAN_WEAPON_AREA)
            elif task.minigame_type == "sharpen_weapon":
                return SharpenWeapon(task, SHARPEN_WEAPON_AREA)
            return None
