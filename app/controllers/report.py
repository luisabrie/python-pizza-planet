from ..repositories.managers.report import ReportManager
from sqlalchemy.exc import SQLAlchemyError

import logging


class ReportController:
    manager = ReportManager

    @classmethod
    def get_reports(cls):
        try:
            return cls.manager.get_all_reports(), None
        except (SQLAlchemyError, RuntimeError) as ex:
            logging.error(ex)
            return None, str(ex)