from .base import BaseManager
from ..models import Ingredient, Beverage, Order, IngredientDetail, BeverageDetail
from ..serializers import OrderSerializer

from sqlalchemy import column, text
from typing import List

class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        cls.session.add_all((IngredientDetail(
            order_id=new_order._id,
            ingredient_id=ingredient._id,
            ingredient_price=ingredient.price)
            for ingredient in ingredients))
        cls.session.add_all((BeverageDetail(order_id=new_order._id, beverage_id=beverage._id, beverage_price=beverage.price)
                             for beverage in beverages))
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f'Method not suported for {cls.__name__}')

    @classmethod
    def drop_all(cls):
        cls.session.query(IngredientDetail).delete()
        cls.session.query(BeverageDetail).delete()
        super().drop_all()

