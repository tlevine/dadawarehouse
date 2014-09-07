from sqlalchemy.orm import sessionmaker as _sessionmaker
from sqlalchemy.exc import ProgrammingError

from .database import Fact, Dimension, Column, Base as _Base, merge_on_unique
from .query import Cube
from .export import export as _export

def refresh(engine):
    for table in _Base.metadata.sorted_tables:
        try:
            engine.execute(table.delete())
        except ProgrammingError:
            pass

def create(engine):
    _Base.metadata.create_all(engine) 
    return _sessionmaker(bind=engine)()

def query(engine):
    '''
    After assembling your schema with the Fact, Dimension, and
    Column classes from doeund, produce some cubes.

    engine: SQLAlchemy engine, from sqlalchemy.create_engine
    '''
    cubes = {name: Cube(session, table) for name, table in \
             _Base.metadata.tables.items() if name.startswith('fact_')}
    return session, cubes

def export():
    return _export(_Base.metadata.tables)
