init python:
    import random
    import math
    
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