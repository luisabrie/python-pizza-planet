from .base import BaseManager
from ..models import Ingredient, IngredientDetail, Order, db

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
