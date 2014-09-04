from werkzeug.serving import run_simple
from vers.cli import command, option
from vers.web.wsgi import create_wsgi_app


@command
@option('--host', '-h', default='127.0.0.1')
@option('--port', '-p', default=5000)
def serve(app, host, port):
    run_simple(host, port, create_wsgi_app(app), use_debugger=True, use_reloader=True)


if __name__ == '__main__':
    serve()