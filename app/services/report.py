from ..common.http_methods import GET
from ..decorators.handle_json_response import handle_json_response
from ..controllers import ReportController

from flask import Blueprint

report = Blueprint('report', __name__)

@handle_json_response
@report.route('/', methods=GET)
def get_reports():
    return ReportController.get_reports()