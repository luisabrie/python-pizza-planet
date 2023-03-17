from .base import BaseManager

from sqlalchemy import column, text


class DBStatusManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column('1')).from_statement(text('SELECT 1')).all()