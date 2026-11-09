# game/logic.rpy
init python:
    import math
    import json
    import random
    from enum import Enum, auto
    
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

            return True

        def finish_day(self):
            if self.current_day:
                self.current_day.finish()
            
            return True

        def next_day(self):
            self.finish_day()

            if self.can_start_day():
                self.start_day()
            
            return False

        def apply_task_result(self, task, result):
            if result == MiniGameResult.GOOD:
                self.player.earn(task.payment)
                self.player.change_reputation(task.reputation)

            elif result == MiniGameResult.MEDIUM:
                self.player.earn(task.payment // 2)

            elif result == MiniGameResult.BAD:
                self.player.change_reputation(-task.reputation // 2)


    class DayState(Enum): #чтобы логика была корректной, дни не путались
        READY = auto() 
        PLAYING = auto()
        FINISHED = auto()


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
            self.state = DayState.READY

        def start(self):
            if self.state != DayState.READY:
                return False

            self.clients = self.client_generator.generate(
                self.clients_number
            )
            if not self.clients:
                self.finish()
                return False

            self.current_client = self.clients[0]
            self.state = DayState.PLAYING

            print(f'день {self.day_number}, clients: {vars(self.current_client)}')

            return True

        def finish_client(self):
            if self.state != DayState.PLAYING:
                return False
            self.completed_clients += 1
            #мини-игра длится 2 часа игрового времени
            self.current_hour += 2 #мб потом вынести, чтоюы не было магическим числом

            if self.completed_clients >= self.clients_number:
                self.finish()
                return

            self.current_client = self.clients[self.completed_clients]

            return True

        def finish(self):
            if self.state == DayState.FINISHED:
                return False
            
            self.state = DayState.FINISHED
            self.current_client = None

            return True

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


    class MiniGameState(Enum): #применяет Finite State Machine для мини-игр
        READY = auto() #разные состояния мини-игры
        RUNNING = auto()
        FINISHED = auto()


    class MiniGameResult(Enum): #общие состояния выполнения мини-игры
        BAD = auto()
        MEDIUM = auto()
        GOOD = auto()


    class MiniGame:
        """Общий класс. Держит только состояние."""
        def __init__(self, task):
            self.task = task
            self.state = MiniGameState.READY #заменяем состояние на Enum (классы выше)
            self.result = MiniGameResult.BAD

        def finish(self, result):
            self.state = MiniGameState.FINISHED
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
                self.result = MiniGameResult.BAD

            if self.clean_progress >= 0.65 and self.clean_progress < 1:
                self.result = MiniGameResult.MEDIUM

            if self.clean_progress >= 1:
                self.result = MiniGameResult.GOOD

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


    class SharpenWeaponState(Enum):
        READY = auto() #начало/повторно когда неудача/следующий раунд
        DRAWING = auto() #нельзя начать рисовать, если игрок уже рисует
        CHECKING = auto() #нельзя проверять до завершения рисования
        FINISHED = auto() #нельзя менять коордрдинаты, если не DRAWING
        #нельзя начать новый раунд после завершения мини-игры


    class SharpenWeapon(MiniGame):
        def __init__(self, task, weapon_area):
            super().__init__(task)

            self.action_state = SharpenWeaponState.READY

            self.is_drawing = False #новое

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

        def change_state(self, new_state):
            allowed_transitions = {
                SharpenWeaponState.READY: [SharpenWeaponState.DRAWING],
                SharpenWeaponState.DRAWING: [SharpenWeaponState.CHECKING],
                SharpenWeaponState.CHECKING: [
                    SharpenWeaponState.READY,
                    SharpenWeaponState.FINISHED
                ],
                SharpenWeaponState.FINISHED: []
            }

            if new_state not in allowed_transitions[self.action_state]:
                return False

            self.action_state = new_state
            return True

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
            if self.action_state != SharpenWeaponState.READY:
                return #новое, дальше лень писать про новое

            self.state = MiniGameState.RUNNING
            self.change_state(SharpenWeaponState.DRAWING)

            self.is_drawing = True
            self.coordinates = [position]


        #запись координат линии, которую рисует игрок
        def record_coordinates(self, position):
            if self.action_state != SharpenWeaponState.DRAWING:
                return
            
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
            if self.action_state != SharpenWeaponState.DRAWING:
                return

            self.is_drawing = False
            self.change_state(SharpenWeaponState.CHECKING)

            self.finish_attempt()


        #определение ориентации трех точек
        def ccw(self, a, b, c):
            #==0 - точки на одной прямой
            return (c[1] - a[1]) * (b[0] - a[0]) - (b[1] - a[1]) * (c[0] - a[0])

        #находится ли точка b на отрезке ac
        def on_segment(self, a, b, c):
            
            return (
                min(a[0], c[0]) <= b[0] <= max(a[0], c[0])
                and
                min(a[1], c[1]) <= b[1] <= max(a[1], c[1])
            )

        #проверяем пересечение двух отрезков
        def segment_intersects(self, p1, p2, p3, p4):
            d1 = self.ccw(p3, p4, p1)
            d2 = self.ccw(p3, p4, p2)

            d3 = self.ccw(p1, p2, p3)
            d4 = self.ccw(p1, p2, p4)

            #обычное пересечение
            if (
                ((d1>0 and d2<0) or (d1<0 and d2>0))
                and 
                ((d3>0 and d4<0) or (d3<0 and d4>0))
            ):
                return True

            #проверка на коллинеарность
            if d1 == 0 and self.on_segment(p3, p1, p4):
                return True
            if d2 == 0 and self.on_segment(p3, p2, p4):
                return True
            if d3 == 0 and self.on_segment(p1, p3, p2):
                return True
            if d4 == 0 and self.on_segment(p1, p4, p2):
                return True

            return False


        #проверка самопересечения линии
        def check_intersection(self):
            coordinates = self.coordinates

            if len(coordinates) < 4:
                return False

            for i in range(len(coordinates) - 1):
                p1 = coordinates[i]
                p2 = coordinates[i + 1]

                for j in range(i + 1, len(coordinates) - 1):
                    p3 = coordinates[j]
                    p4 = coordinates[j + 1]

                    if j == i + 1:

                        # Проверяем, лежат ли они на одной прямой
                        if self.ccw(p1, p2, p4) == 0:
                            # Проверяем наложение
                            if (
                                self.on_segment(p1, p4, p2)
                                or
                                self.on_segment(p2, p1, p4)
                            ):
                                return True

                        continue

                    if self.segment_intersects(p1, p2, p3, p4):
                        return True
                        print(f"линии")

            return False


        #расстояние от точки до отрезка
        def point_to_segment_distance(self, point, start, end):
            px, py = point
            x1, y1 = start
            x2, y2 = end

            dx = x2 - x1
            dy = y2 - y1

            lenght_squared = dx * dx + dy * dy

            if lenght_squared == 0:
                return math.hypot(px - x1, py - y1)

            t = ((px - x1) * dx + (py - y1) * dy) / lenght_squared
            t = max(0, min(1, t))

            closest_x = x1 + t * dx
            closest_y = y1 + t * dy

            return math.hypot(px - closest_x, py - closest_y)

        #проверка собранных точек
        def check_collected_points(self):
            self.collected_points = 0

            for point in self.points:
                point["collected"] = False

                for i in range(len(self.coordinates) - 1):
                    start = self.coordinates[i]
                    end = self.coordinates[i + 1]

                    distance = self.point_to_segment_distance(
                        (point["x"], point["y"]),
                        start,
                        end
                    )

                    if distance <= 20:
                        point["collected"] = True
                        break

                if point["collected"]:
                        self.collected_points += 1

            return self.collected_points==10

        #завершение попытки
        def finish_attempt(self):
            if self.check_intersection():
                self.reset_attempt()
                self.change_state(SharpenWeaponState.READY)
                return

            if self.check_collected_points():
                self.next_round()
            else:
                self.reset_attempt()
                self.change_state(SharpenWeaponState.READY)

        #сброс попытки
        def reset_attempt(self):
            self.coordinates = []
            self.collected_points = 0
            self.is_drawing = False

            for point in self.points:
                point["collected"] = False

            self.action_state = SharpenWeaponState.READY

        #переход к следующему раунду
        def next_round(self):
            if self.round_number >= self.max_rounds:
                self.change_state(SharpenWeaponState.FINISHED)
                self.finish(self.result)
                return

            self.round_number += 1
            self.generate_points()
            self.coordinates = []
            self.is_drawing = False
            self.collected_points = 0
            self.change_state(SharpenWeaponState.READY)


    class DrawingLine(renpy.Displayable):

        def __init__(self, sharpen_weapon, **kwargs):

            super(DrawingLine, self).__init__(**kwargs)

            self.sharpen_weapon = sharpen_weapon

            # Цвет линии (бирюзовый)
            self.color = (40, 220, 210, 255)

            # Толщина линии
            self.line_width = 4

        def render(self, width, height, st, at):

            # Создаём область для рисования
            render = renpy.Render(width, height)

            canvas = render.canvas()

            coordinates = self.sharpen_weapon.coordinates

            # Рисуем линию между соседними координатами
            for i in range(len(coordinates) - 1):

                start = coordinates[i]
                end = coordinates[i + 1]

                canvas.line(
                    self.color,
                    start,
                    end,
                    self.line_width
                )

            # Обновляем отображение во время рисования
            if self.sharpen_weapon.is_drawing:
                renpy.redraw(self, 0.02)

            return render


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
