from ..repositories.managers.size import SizeManager
from .base import BaseController


class SizeController(BaseController):
    manager = SizeManager
