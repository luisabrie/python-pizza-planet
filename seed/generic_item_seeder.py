from faker import Faker

from .abstract_seeder import AbstractSeeder


fake = Faker()

class GenericItemSeeder(AbstractSeeder):

    def create(self):
        beverage, err = self.controller.create({
            'name': fake.name(),
            'price': fake.pyint(min_value=1, max_value=10)
        })
        if err:
            raise Exception(err)
        return beverage