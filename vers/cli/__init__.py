import functools
import click
from vers import create_app

option = click.option


def command(f):
    @click.command()
    @click.option('--config', '-c', default='config.py', envvar='VERS_CONFIG')
    @functools.wraps(f)
    def wrapped(config, *args, **kwargs):
        app = create_app(config)
        kwargs['app'] = app
        return f(*args, **kwargs)
    return wrapped