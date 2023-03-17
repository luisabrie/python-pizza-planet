from app.repositories.managers.ingredient import IngredientManager
from .base import BaseController


class IngredientController(BaseController):
    manager = IngredientManager
