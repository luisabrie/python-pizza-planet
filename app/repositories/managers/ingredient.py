from ..models import Ingredient
from ..serializers import IngredientSerializer
from .base import BaseManager

from typing import Sequence


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set([int(id) for id in ids]))).all() or []
