from werkzeug.utils import import_string


class BaseApp(object):
    def __init__(self, config):
        '''
        :param config: dict[str, T]
        '''
        self.config = config

    def setup(self):
        pass


def read_config(path):
    config = {}
    execfile(path, globals(), config)
    return config


def create_app(config_path):
    config = read_config(config_path)
    app_class = config.get('VERS_APP_CLASS')
    if app_class is None:
        app_class = BaseApp
    else:
        app_class = import_string(app_class)
    app = app_class(config)
    app.setup()
    return app