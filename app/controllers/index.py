from typing import Tuple
from sqlalchemy.exc import SQLAlchemyError

from ..repositories.managers.db_status import DBStatusManager

import logging
class IndexController:

    @staticmethod
    def test_connection() -> Tuple[bool, str]:
        try:
            DBStatusManager.test_connection()
            return True, ''
        except (SQLAlchemyError, RuntimeError) as ex:
            logging.error(ex)
            return False, str(ex)
