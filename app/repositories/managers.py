from typing import Any, List, Optional, Sequence

from sqlalchemy.sql import text, column

from .models import Ingredient, Beverage, Order, IngredientDetail, BeverageDetail, Size, db
from .serializers import (IngredientSerializer, OrderSerializer, BeverageSerializer,
                          SizeSerializer, ma)


class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)
    
    @classmethod
    def drop_all(cls):
        cls.session.query(cls.model).delete()
        cls.session.commit()


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer

class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []

class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


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


class IndexManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column('1')).from_statement(text('SELECT 1')).all()

class ReportManager(BaseManager):

    @classmethod
    def get_all_reports(cls):
        return {
            'most_requested_ingredient': cls.get_most_requested_ingredient(),
            'month_with_most_revenue': cls.get_month_with_most_revenue(),
            'top_three_customers': cls.get_top_three_customers(),
        }
    
    @classmethod
    def get_most_requested_ingredient(cls):
        most_requested_ingredient = cls.session.query(Ingredient.name,
            db.func.count(IngredientDetail.ingredient_id).label('total'))\
            .join(IngredientDetail, IngredientDetail.ingredient_id == Ingredient._id)\
            .group_by(Ingredient.name)\
            .order_by(db.desc('total'))\
            .limit(1)\
            .first()
        return {
                 'name': most_requested_ingredient.name if most_requested_ingredient else '',
                 'total': most_requested_ingredient.total if most_requested_ingredient else 0
                }
    @classmethod
    def get_month_with_most_revenue(cls):
        months = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
        month_with_most_revenue = cls.session.query(
            db.func.extract('month', Order.date).label('month'),
            db.func.sum(Order.total_price).label('total'))\
            .group_by(db.func.extract('month', Order.date))\
            .order_by(db.desc('total'))\
            .limit(1)\
            .first()
        return {
                'month': months[int(month_with_most_revenue.month) - 1] if month_with_most_revenue else '',
                'total': month_with_most_revenue.total if month_with_most_revenue else 0
                }
    @classmethod
    def get_top_three_customers(cls):
        top_three_customers = cls.session.query(Order.client_name,
            db.func.count(Order.client_dni).label('total'))\
            .group_by(Order.client_dni)\
            .order_by(db.desc('total'))\
            .limit(3)\
            .all()
        return [{
                'name': customer.client_name,
                'total': customer.total
                } for customer in top_three_customers]
