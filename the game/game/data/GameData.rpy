init python:
    import json
    
    class GameData():
        def __init__(self):
            self.tasks = {}
            self.clients = []

        def load(self):
            task_data = load_json("data/json_files/tasks.json")
            client_data = load_json("data/json_files/clients.json")

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