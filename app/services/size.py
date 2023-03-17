from ..common.http_methods import GET, POST, PUT
from ..services.base import BaseService
from ..controllers import SizeController

from flask import Blueprint

size = Blueprint('size', __name__)
baseService = BaseService(SizeController)

@size.route('/', methods=GET)
def get_sizes():
    return baseService.get_all()

@size.route('/id/<_id>', methods=GET)
def get_size_by_id(_id: int):
    return baseService.get_by_id(_id)

@size.route('/', methods=POST)
def create_size():
    return baseService.create()

@size.route('/', methods=PUT)
def update_size():
    return baseService.update()


