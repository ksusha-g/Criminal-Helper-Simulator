init python:

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