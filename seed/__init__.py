from app.controllers import BeverageController, IngredientController, SizeController, OrderController


from seed.generic_item_seeder import GenericItemSeeder
from seed.custom_seeders import SizeSeeder, OrderSeeder
from seed.handle_seeding import DBSeeder

db_seeder = DBSeeder()
db_seeder.add_seeder(GenericItemSeeder(IngredientController, "ingredient"))
db_seeder.add_seeder(GenericItemSeeder(BeverageController, "beverage"))
db_seeder.add_seeder(SizeSeeder(SizeController, "size"))
db_seeder.add_seeder(OrderSeeder(OrderController, "order"))
seeder = db_seeder