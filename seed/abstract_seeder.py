import logging

class Handler():
    def __init__(self):
        self.next_handler = None
        self.context = {}

    def has_next(self):
        return self.next_handler is not None

    def get_from_context(self, key):
        return self.context[key]
    
    def set_to_context(self, key, value):
        self.context[key] = value

    def set_next(self, handler):
        if self.has_next():
            self.next_handler.set_next(handler)
            return self

        self.next_handler = handler
        self.next_handler.context = self.context
        
        return handler
    
    def handle(self, method):
        if self.has_next():
            getattr(self.next_handler, method)()
    
class AbstractSeeder(Handler):
    def __init__(self, controller, controller_name):
        super().__init__()
        self.controller = controller
        self.controller_name = controller_name
        
        self.objects = []
        self.seed_count = 10
    
    def seed(self):
        logging.info(f'Seeding {self.controller_name}')

        for _ in range(self.seed_count):
            self.objects.append(self.create())

        self.set_to_context(self.controller_name, self.objects)
        self.handle('seed')
    
    def drop(self):
        self.handle('drop')
            
        logging.info(f'Dropping {self.controller_name}')
        self.controller.manager.drop_all()
    
    def create(self):
        raise NotImplementedError