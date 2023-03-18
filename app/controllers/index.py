from typing import Tuple
from sqlalchemy.exc import SQLAlchemyError

from ..repositories.managers.db_status import DBStatusManager


class IndexController:

    @staticmethod
    def test_connection() -> Tuple[bool, str]:
        try:
            DBStatusManager.test_connection()
            return True, ''
        except (SQLAlchemyError, RuntimeError) as ex:
            return False, str(ex)
