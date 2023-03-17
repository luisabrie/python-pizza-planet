from ..common.http_methods import GET, POST
from ..controllers import OrderController
from .base import BaseService

from flask import Blueprint


order = Blueprint('order', __name__)
baseService = BaseService(OrderController)

@order.route('/', methods=GET)
def get_orders():
    return baseService.get_all()

@order.route('/id/<_id>', methods=GET)
def get_order_by_id(_id: int):
   return baseService.get_by_id(_id)

@order.route('/', methods=POST)
def create_order():
    return baseService.create()

