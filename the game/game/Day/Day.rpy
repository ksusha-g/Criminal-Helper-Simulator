init python:
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