from functools import wraps
from flask import jsonify
from ..handlers.error_handlers import default_error_status_handler

def handle_json_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data, error = func(*args, **kwargs)
        response = data if not error else {'error': error}
        status_code = default_error_status_handler(data, error)
        return jsonify(response), status_code
    return wrapper