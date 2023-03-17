from app.common.http_methods import GET, POST, PUT
from flask import Blueprint
from app.services.base import BaseService

from ..controllers import BeverageController

beverage = Blueprint('beverage', __name__)
baseService = BaseService(BeverageController)

@beverage.route('/', methods=GET)
def get_beverages():
    return baseService.get_all()

@beverage.route('/id/<_id>', methods=GET)
def get_beverage_by_id(_id: int):
    return baseService.get_by_id(_id)

@beverage.route('/', methods=POST)
def create_beverage():
    return baseService.create()

@beverage.route('/', methods=PUT)
def update_beverage():
    return baseService.update()




