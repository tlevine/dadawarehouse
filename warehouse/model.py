import sqlalchemy as s
from doeund import Fact, Dimension, Column as _Column

def Column(*args, **kwargs):
    '''
    Column with good defaults
    '''
    _kwargs = dict(kwargs)
    if 'nullable' not in _kwargs:
        _kwargs['nullable'] = False
    return _Column(*args, **kwargs) 

def IdColumn(*args, **kwargs):
    '''
    Identifier field
    '''
    return Column(s.Integer, *args, **kwargs)

class Date(Dimension):
    '''
    Dates with hierarchies
    '''
    pk = Column(s.Date, primary_key = True)
    year = Column(s.Integer)
    month = Column(s.Integer)
    day = Column(s.Integer)

class Time(Dimension):
    pk = IdColumn(s.Time, primary_key = True) # seconds from midnight
    hour = Column(s.Integer)
    minute = Column(s.Integer)
    second = Column(s.Integer)
