from sqlalchemy.orm import sessionmaker as _sessionmaker

from .database import Fact, Dimension, Column, Base as _Base, merge_on_unique
from .export import export as _export

def database(engine):
    _Base.metadata.create_all(engine) 
    return _sessionmaker(bind=engine)()

def model():
    return _export(_Base.metadata.tables)
