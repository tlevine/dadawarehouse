from sqlalchemy.orm import sessionmaker

from .components import Fact, Dimension, Column, Base as _Base
from .provider import model

def doeund(engine,
    '''
    engine: SQLAlchemy engine, from sqlalchemy.create_engine

    '''
    _Base.metadata.create_all(engine) 
    session = sessionmaker(bind=engine)()
