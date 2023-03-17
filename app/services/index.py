from ..common.http_methods import GET
from ..controllers import IndexController
from ..decorators.handle_json_response import handle_json_response

from flask import Blueprint

index = Blueprint('index', __name__)

@handle_json_response
@index.route('/', methods=GET)
def get_index():
    is_database_up, error = IndexController.test_connection()
    return {'version': '0.0.2', 'status': 'up' if is_database_up else 'down', 'error': error}
