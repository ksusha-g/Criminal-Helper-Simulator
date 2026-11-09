init python:
    
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