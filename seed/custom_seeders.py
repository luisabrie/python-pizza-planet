from faker import Faker

from seed.abstract_seeder import AbstractSeeder
from seed.utils import extract_ids

fake = Faker()

class SizeSeeder(AbstractSeeder):
    def __init__(self, controller, controller_name):
        super().__init__(controller, controller_name)
        self.default_sizes = [
            {'name': 'extra large', 'price': 23},
            {'name': 'large', 'price': 20},
            {'name': 'medium', 'price': 15},
            {'name': 'small', 'price': 10},
            {'name': 'extra small', 'price': 8},
        ]
        self.seed_count = len(self.default_sizes)
    def create(self):
        size, err = self.controller.create(self.default_sizes.pop())
        if err:
            raise Exception(err)
        return size
            
class OrderSeeder(AbstractSeeder):

    def __init__(self, controller, controller_name):
        super().__init__(controller, controller_name)
        self.seed_count = 100
    
    def generate_clients(self, count):
        self.clients = [
            {
                'client_name': fake.name(),
                'client_address': fake.address(),
                'client_phone': fake.phone_number(),
                'client_dni': fake.ssn(),
            }
            for _ in range(count)
        ]
    def generate_orders(self, count):
        self.orders = [
            {
                **fake.random_element(elements=self.clients),
                'date': fake.date_time_between(start_date='-1y', end_date='now'),
                'size_id': fake.random_element(elements=self.get_from_context('size'))['_id'],
            }
            for _ in range(count)
        ]

    def create(self):
        if not hasattr(self, 'clients'):
            self.generate_clients(self.seed_count//4)
        if not hasattr(self, 'orders'):
            self.generate_orders(self.seed_count)
        complete_order = {
            **self.orders.pop(),
            'beverages': extract_ids(fake.random_elements(
                elements=self.get_from_context('beverage'),
                length=fake.pyint(min_value=1, max_value=5), 
                unique=True)),
            'ingredients': extract_ids(fake.random_elements(
                elements=self.get_from_context('ingredient'),
                length=fake.pyint(min_value=1, max_value=5), 
                unique=True)),
        }
        order, err = self.controller.create(complete_order)
        if err:
            raise Exception(err)
        return order

        