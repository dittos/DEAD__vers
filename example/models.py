from sqlalchemy import Column, types
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    id = Column(types.Integer, primary_key=True)
    title = Column(types.String, nullable=False)