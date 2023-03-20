from ..models import Beverage
from ..serializers import BeverageSerializer
from .base import BaseManager

from typing import Sequence


class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set([int(id) for id in ids]))).all() or []
