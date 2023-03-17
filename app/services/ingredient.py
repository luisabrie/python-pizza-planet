from app.common.http_methods import GET, POST, PUT
from flask import Blueprint
from app.services.base import BaseService

from ..controllers import IngredientController

ingredient = Blueprint('ingredient', __name__)
baseService = BaseService(IngredientController)

@ingredient.route('/', methods=GET)
def get_ingredients():
    return baseService.get_all()

@ingredient.route('/id/<_id>', methods=GET)
def get_ingredient_by_id(_id: int):
    return baseService.get_by_id(_id)

@ingredient.route('/', methods=POST)
def create_ingredient():
    return baseService.create()

@ingredient.route('/', methods=PUT)
def update_ingredient():
    return baseService.update()




