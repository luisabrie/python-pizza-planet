import logging


class DBSeeder():
    def __init__(self):
        self.start = None
        
    def add_seeder(self, seeder):
        if not self.has_start():
            self.start = seeder
        else:
            self.start.set_next(seeder)
        return seeder
        
    def seed(self):
        if self.has_start():
            self.start.seed()
        else:
            logging.info('No seeders added')

    def drop(self):
        if self.has_start():
            self.start.drop()
        else:
            logging.info('No seeders added')

    def has_start(self):
        return self.start != None