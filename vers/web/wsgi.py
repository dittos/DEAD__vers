from werkzeug.wsgi import responder
from werkzeug.routing import Map, Rule
from werkzeug.utils import import_string
from vers.web import Request


def create_url_map(app):
    handlers = app.config.get('VERS_WEB_HANDLERS', ())
    url_map = Map()
    for path, handler_class in handlers:
        handler_class = import_string(handler_class)
        url_map.add(Rule(path, endpoint=handler_class))
    return url_map


def create_wsgi_app(app):
    url_map = create_url_map(app)
    @responder
    def application(environ, start_response):
        request = Request(environ)
        urls = url_map.bind_to_environ(environ)
        def dispatch(handler_class, path_args):
            request.path_args = path_args
            handler = handler_class(app, request)
            handler.before_request()
            assert handler._base_before_request_called
            try:
                method = getattr(handler, request.method.lower())
                return method()
            finally:
                handler.after_request()
                assert handler._base_after_request_called
        return urls.dispatch(dispatch, catch_http_exceptions=True)
    return application