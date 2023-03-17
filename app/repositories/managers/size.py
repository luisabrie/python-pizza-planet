from ..models import Size
from ..serializers import SizeSerializer
from ..managers.base import BaseManager


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer