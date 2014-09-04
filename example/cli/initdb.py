from vers.cli import command
from . import models


@command
def initdb(app):
    models.Base.metadata.create_all(bind=app.db_engine)


if __name__ == '__main__':
    initdb()