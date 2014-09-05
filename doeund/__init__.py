from sqlalchemy.orm import sessionmaker as _sessionmaker
from sqlalchemy.exc import ProgrammingError

from .database import Fact, Dimension, Column, Base as _Base, merge_on_unique
from .cube import Cube

def doeund(engine, refresh = False):
    '''
    After assembling your schema with the Fact, Dimension, and
    Column classes from doeund, produce some cubes.

    engine: SQLAlchemy engine, from sqlalchemy.create_engine
    '''
    if refresh:
        for table in _Base.metadata.sorted_tables:
            try:
                engine.execute(table.delete())
            except ProgrammingError:
                pass
    _Base.metadata.create_all(engine) 
    session = _sessionmaker(bind=engine)()
    cubes = {name: Cube(session, table) for name, table in \
             _Base.metadata.tables.items() if name.startswith('fact_')}
    return session, cubes
