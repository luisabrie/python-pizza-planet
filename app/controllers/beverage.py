from ..repositories.managers.beverage import BeverageManager
from .base import BaseController


class BeverageController(BaseController):
    manager = BeverageManager
