import sqlalchemy as s
from doeund import Fact as _Fact, Dimension, Column as _Column

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

class Fact(_Fact):
    __abstract__ = True

def add_label(session, record):
    table = record.__table__
    columns = list(filter(lambda column: column.name != 'pk', table.columns))
    if len(columns) != 1:
        raise ValueError('The record must be for a table with a "pk" column and a label column.')
    elif not columns[0].unique:
        raise ValueError('The label column must be unique.')

    column = columns[0]
    value = getattr(record, column.name)
    print(value)
    exists = session.query(table).filter(column == value).count() > 0
    if not exists:
        session.add(record)
