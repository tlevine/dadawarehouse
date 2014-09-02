from sqlalchemy.orm import sessionmaker

from .components import Fact, Dimension, Column, Base as _Base
from .provider import _DoeundProvider

def doeund(engine, fact_tables, dimension_tables):
    '''
    After assembling your schema with the Fact, Dimension, and
    Column classes from doeund, produce a database session and
    a cubes model provider.

    engine: SQLAlchemy engine, from sqlalchemy.create_engine
    '''
    class DoeundProvider(_DoeundProvider):
        def __init__(self, metadata = None):
            super(_DoeundProvider, self).__init__(metadata = metadata,
                declarative_base = _Base, fact_tables = fact_tables,
                dimension_tables = dimension_tables)

    _Base.metadata.create_all(engine) 
    session = sessionmaker(bind=engine)()
    return session, DoeundProvider
