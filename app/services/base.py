from flask import jsonify, request


class BaseService:
    def __init__(self, controller):
        self.controller = controller

    def handle_request(self, func_name, *args, **kwargs):
        func = getattr(self.controller, func_name)
        data, error = func(*args, **kwargs)
        response = data if not error else {'error': error}
        status_code = 200 if data else 404 if not error else 400
        return jsonify(response), status_code

    def get_all(self):
        return self.handle_request('get_all')

    def get_by_id(self, _id: int):
        return self.handle_request('get_by_id', _id)

    def create(self):
        return self.handle_request('create', request.json)

    def update(self):
        return self.handle_request('update', request.json)
