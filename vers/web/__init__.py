from werkzeug.wrappers import Request, Response
from .decorators import path_arg, query_arg, form_arg, respond_with


class BaseHandler(object):
    def __init__(self, app, request):
        self.app = app
        self.request = request
        self._base_before_request_called = False
        self._base_after_request_called = False

    def before_request(self):
        self._base_before_request_called = True

    def after_request(self):
        self._base_after_request_called = True

    def get(self):
        raise NotImplemented

    def post(self):
        raise NotImplemented

    def put(self):
        raise NotImplemented

    def delete(self):
        raise NotImplemented