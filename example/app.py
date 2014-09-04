from vers import BaseApp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class App(BaseApp):
    def setup(self):
        self.db_engine = create_engine(self.config['DATABASE_URI'])
        self.Session = sessionmaker(bind=self.db_engine)