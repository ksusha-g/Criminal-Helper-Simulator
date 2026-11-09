init python:
    import json
    
    def load_json(file_path):
        with renpy.open_file(file_path) as file:
            return json.load(file)