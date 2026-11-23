init python:

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