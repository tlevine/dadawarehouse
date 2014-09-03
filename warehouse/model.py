import sqlalchemy as s
from doeund import Fact, Dimension, Column as _Column

def Column(*args, **kwargs):
    'Column with good defaults'
    _kwargs = dict(kwargs)
    if 'nullable' not in _kwargs:
        _kwargs['nullable'] = False
    return _Column(*args, **kwargs) 

def FkColumn(column, *args, **kwargs):
    'Foreign key field'
    return Column(s.Integer, s.ForeignKey(column), *args, **kwargs)

def PkColumn(*args, **kwargs):
    'Primary key field'
    return Column(s.Integer, primary_key = True, *args, **kwargs)

def LabelColumn(*args, **kwargs):
    'A unique string column, for values in a two-column lookup table'
    return Column(s.String, unique = True, *args, **kwargs)

def DateColumn(*args, **kwargs):
    'A date column with magic hierarchies'
    return Column(s.Date, s.ForeignKey('dim_date.pk'), *args, **kwargs)

def TimeColumn(*args, **kwargs):
    return Column(s.Time, s.ForeignKey('dim_time.pk'), *args, **kwargs)
            
class Date(Dimension):
    '''
    Dates with hierarchies
    '''
    pk = Column(s.Date, primary_key = True)
    year = Column(s.Integer)
    month = Column(s.Integer)
    day = Column(s.Integer)

class Time(Dimension):
    pk = Column(s.Time, primary_key = True) # seconds from midnight
    hour = Column(s.Integer)
    minute = Column(s.Integer)
    second = Column(s.Integer)

def add_label(session, record):
    for column in record.__table__.columns:
        if column.unique and session.query(record.__table__).count(column) > 0
            break
    else:
        session.add(record)
