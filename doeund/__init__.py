from sqlalchemy.orm import sessionmaker as _sessionmaker
from sqlalchemy.exc import ProgrammingError

from .database import Fact, Dimension, Column, Base as _Base, merge_on_unique
from .export import export as _export

def create(engine):
    _Base.metadata.create_all(engine) 
    session = _sessionmaker(bind=engine)()
    model = _export(_Base.metadata.tables)
    return session, model
