from sqlalchemy.orm import sessionmaker as _sessionmaker

from .database import Fact, Dimension, Column, Base as _Base
from .cube import Cube

def doeund(engine, refresh = False):
    '''
    After assembling your schema with the Fact, Dimension, and
    Column classes from doeund, produce some cubes.

    engine: SQLAlchemy engine, from sqlalchemy.create_engine
    '''
    if refresh:
        for table in _Base.metadata.sorted_tables:
            engine.execute(table.delete())
    _Base.metadata.create_all(engine) 
    session = _sessionmaker(bind=engine)()
    cubes = {name: Cube(session, table) for name, table in \
             _Base.metadata.tables.items() if name.startswith('fact_')}
    return session, cubes
