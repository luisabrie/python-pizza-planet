from flask import request
from ..decorators.handle_json_response import handle_json_response


class BaseService:
    def __init__(self, controller):
        self.controller = controller

    @handle_json_response
    def handle_request(self, func_name, *args, **kwargs):
        func = getattr(self.controller, func_name)
        return func(*args, **kwargs)

    def get_all(self):
        return self.handle_request('get_all')

    def get_by_id(self, _id: int):
        return self.handle_request('get_by_id', _id)

    def create(self):
        return self.handle_request('create', request.json)

    def update(self):
        return self.handle_request('update', request.json)
