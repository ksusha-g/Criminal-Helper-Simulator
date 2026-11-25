init python:
    class Alchemy(MiniGame):
        def __init__(self, task):
            super().__init__(task)

            self.ingredients = {
                "sagebrush": { #полынь
                    "count": 6,
                    "x": 1400,
                    "y": 100
                },
                "mandrake": { #мандрагора
                    "count": 3,
                    "x": 1100,
                    "y": 500
                } 
            } 

            self.cauldron = {
                "sagebrush": 0,
                "mandrake": 0
            }

        def add_to_cauldron(self, ingredient):
            if ingredient not in self.ingredients:
                return False

            if self.ingredients[ingredient]['count'] <= 0:
                return False

            self.ingredients[ingredient]['count'] -= 1
            self.cauldron[ingredient] += 1

            return True

        def ingredient_dropped(self, drags, drop):
            if not drags:
                return

            ingredient = drags[0].drag_name

            if drop is not None and drop.drag_name == "cauldron":
                self.add_to_cauldron(ingredient)

            x = self.ingredients[ingredient]["x"]
            y = self.ingredients[ingredient]["y"]
            drags[0].snap(x, y)
            renpy.restart_interaction()