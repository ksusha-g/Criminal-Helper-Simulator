init python:
    import random

    class Client_generator():
        def __init__(self, clients):
            self.clients = clients

        def generate(self, number):
            result = []

            for i in range(number):
                client = random.choice(self.clients)
                result.append(client)

            return result









